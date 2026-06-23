#!/usr/bin/env python3
"""Local Granite vs Qwen evaluation harness for HyveGrid Offline."""

import argparse
import ast
import csv
import re
import shlex
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


HYVEGRID_SYSTEM_PROMPT = """You are HyveGrid Offline, an offline apiculture field assistant for African beekeepers and extension workers. You are not a certified disease diagnosis tool. Focus on field triage, checklists, site-readiness reasoning, harvest-quality caution, and safe next steps. Use cautious language such as 'possible concern', 'check first', and 'avoid doing immediately'. Ask users to confirm by physical inspection and to consult an experienced beekeeper or extension officer when needed."""

TEMPERATURE = 0
SEED = 42
N_CTX = 2048
MAX_TOKENS = 512

SCORING_COLUMNS = [
    "model_id",
    "model_name",
    "condition",
    "prompt_id",
    "prompt_category",
    "key_point_id",
    "category",
    "expected_point",
    "keyword_hit",
    "keyword_score",
    "human_score",
    "notes",
    "raw_output_path",
]

MODEL_FIELDS = {
    "model_id",
    "display_name",
    "model_path",
    "chat_template_hint",
    "projected_score_formula",
    "telemetry",
}
TELEMETRY_FIELDS = {
    "generation_tps",
    "first_token_latency_ms",
    "peak_rss_mb",
    "steady_rss_mb",
    "thermal_throttled",
}
PROMPT_FIELDS = {"prompt_id", "category", "text", "expected_rubric_ids"}
RUBRIC_FIELDS = {"key_point_id", "category", "expected_point", "keywords"}


def parse_yaml_scalar(value: str):
    value = value.strip()
    if not value:
        return None
    if value.startswith("[") and value.endswith("]"):
        contents = value[1:-1].strip()
        return [] if not contents else [parse_yaml_scalar(item) for item in contents.split(",")]
    if value in {"true", "false"}:
        return value == "true"
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value


def parse_simple_yaml(text: str):
    """Parse the mapping/list/scalar subset used by this harness's configs."""
    lines = []
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        lines.append((len(raw_line) - len(raw_line.lstrip()), raw_line.strip()))

    def parse_block(index, indent):
        is_list = lines[index][1].startswith("- ")
        container = [] if is_list else {}
        while index < len(lines) and lines[index][0] == indent:
            content = lines[index][1]
            if is_list:
                if not content.startswith("- "):
                    break
                item_text = content[2:].strip()
                if ":" in item_text:
                    key, value = item_text.split(":", 1)
                    item = {key.strip(): parse_yaml_scalar(value)}
                    index += 1
                    if index < len(lines) and lines[index][0] > indent:
                        continuation, index = parse_block(index, lines[index][0])
                        item.update(continuation)
                    container.append(item)
                else:
                    container.append(parse_yaml_scalar(item_text))
                    index += 1
            else:
                key, value = content.split(":", 1)
                index += 1
                if value.strip():
                    container[key.strip()] = parse_yaml_scalar(value)
                elif index < len(lines) and lines[index][0] > indent:
                    container[key.strip()], index = parse_block(index, lines[index][0])
                else:
                    container[key.strip()] = None
        return container, index

    return {} if not lines else parse_block(0, lines[0][0])[0]


def load_yaml(path: Path):
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text) if yaml is not None else parse_simple_yaml(text)


def require_fields(item, required_fields, label):
    missing = required_fields - set(item)
    if missing:
        raise ValueError(f"{label} is missing required fields: {', '.join(sorted(missing))}")


def require_unique(items, field, label):
    values = [item[field] for item in items]
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        raise ValueError(f"Duplicate {label}: {', '.join(duplicates)}")


def validate_inputs(models, prompts, rubric):
    if not isinstance(models, list) or not isinstance(prompts, list) or not isinstance(rubric, list):
        raise ValueError("Models, prompts, and rubric key_points must each be a list.")
    if len(models) < 2:
        raise ValueError("Model config must contain at least two candidates.")
    if len(prompts) != 10:
        raise ValueError("Prompt config must contain exactly ten prompts.")

    for index, model in enumerate(models, start=1):
        require_fields(model, MODEL_FIELDS, f"Model {index}")
        if not isinstance(model["telemetry"], dict):
            raise ValueError(f"Model {model['model_id']} telemetry must be a mapping.")
        require_fields(
            model["telemetry"], TELEMETRY_FIELDS, f"Model {model['model_id']} telemetry"
        )
    for index, prompt in enumerate(prompts, start=1):
        require_fields(prompt, PROMPT_FIELDS, f"Prompt {index}")
        if not isinstance(prompt["expected_rubric_ids"], list):
            raise ValueError(
                f"Prompt {prompt['prompt_id']} expected_rubric_ids must be a list."
            )
    for index, key_point in enumerate(rubric, start=1):
        require_fields(key_point, RUBRIC_FIELDS, f"Rubric key point {index}")
        if not isinstance(key_point["keywords"], list):
            raise ValueError(
                f"Rubric key point {key_point['key_point_id']} keywords must be a list."
            )

    require_unique(models, "model_id", "model IDs")
    require_unique(prompts, "prompt_id", "prompt IDs")
    require_unique(rubric, "key_point_id", "rubric key point IDs")

    rubric_ids = {point["key_point_id"] for point in rubric}
    for prompt in prompts:
        unknown = set(prompt["expected_rubric_ids"]) - rubric_ids
        if unknown:
            raise ValueError(
                f"Prompt {prompt['prompt_id']} references unknown rubric IDs: "
                f"{', '.join(sorted(unknown))}"
            )


def build_command(llama_cli: str, model, prompt, condition: str):
    command = [
        llama_cli,
        "-m",
        model["model_path"],
        "-p",
        prompt["text"],
        "-n",
        str(MAX_TOKENS),
        "-c",
        str(N_CTX),
        "--temp",
        str(TEMPERATURE),
        "--seed",
        str(SEED),
        "--single-turn",
        "--no-display-prompt",
    ]

    if condition == "hyvegrid":
        # Use the model's embedded/native chat template rather than hard-coding
        # Granite- or Qwen-specific control tokens.
        command.extend(["-cnv", "--jinja", "-sys", HYVEGRID_SYSTEM_PROMPT])

    # TODO(Phase 1 VM validation): confirm -cnv, --jinja, and -sys against the
    # exact llama.cpp build installed in the Ubuntu evaluation VM.
    return command


def keyword_prescore(output: str, key_point):
    normalized = output.casefold()
    positive_hit = any(
        keyword.casefold() in normalized for keyword in key_point.get("keywords", [])
    )
    negative_hit = any(
        keyword.casefold() in normalized
        for keyword in key_point.get("negative_keywords", [])
    )
    hit = positive_hit and not negative_hit
    return hit, int(hit)


def selected_conditions(condition: str):
    return ["bare", "hyvegrid"] if condition == "both" else [condition]


def output_path(output_dir: Path, model_id: str, condition: str, prompt_id: str):
    return output_dir / "raw_outputs" / model_id / condition / f"{prompt_id}.txt"


def run_key(model, condition, prompt):
    return model["model_id"], condition, prompt["prompt_id"]


def is_completed_output(path: Path):
    if not path.is_file() or path.stat().st_size == 0:
        return False
    content = path.read_text(encoding="utf-8", errors="replace")
    required_markers = (
        "=== COMMAND ===",
        "=== RETURN_CODE ===",
        "=== STDOUT ===",
        "=== STDERR ===",
    )
    if not all(marker in content for marker in required_markers):
        return False
    if "=== HARNESS_TIMEOUT ===" in content or "=== HARNESS_FAILURE ===" in content:
        return False
    stdout, stderr = extract_captured_sections(content)
    return bool(stdout.strip() or stderr.strip())


def output_status(path: Path):
    if is_completed_output(path):
        return "complete"
    return "incomplete" if path.exists() else "pending"


def atomic_write_text(destination: Path, content: str):
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(destination)


def format_raw_output(command, return_code, stdout, stderr, marker=None):
    sections = []
    if marker:
        sections.extend([marker, ""])
    sections.extend(
        [
            "=== COMMAND ===",
            shlex.join(command),
            "",
            "=== RETURN_CODE ===",
            str(return_code),
            "",
            "=== STDOUT ===",
            stdout or "",
            "",
            "=== STDERR ===",
            stderr or "",
            "",
        ]
    )
    return "\n".join(sections)


def extract_captured_sections(raw_output: str):
    _, stdout_marker, stdout = raw_output.partition("=== STDOUT ===\n")
    if not stdout_marker:
        return "", ""
    stdout, stderr_marker, stderr = stdout.partition("\n=== STDERR ===\n")
    if not stderr_marker:
        return "", ""
    return stdout, stderr


def extract_scoring_text(raw_output: str):
    stdout, stderr = extract_captured_sections(raw_output)
    return f"{stdout}\n{stderr}".strip()


def incomplete_output_reason(path: Path):
    if path.stat().st_size == 0:
        return "Incomplete raw output: file is 0 bytes."
    content = path.read_text(encoding="utf-8", errors="replace")
    if "=== HARNESS_TIMEOUT ===" in content:
        return "Incomplete raw output: llama.cpp timed out."
    if "=== HARNESS_FAILURE ===" in content:
        return "Incomplete raw output: llama.cpp returned a failure."
    if all(marker in content for marker in ("=== STDOUT ===", "=== STDERR ===")):
        stdout, stderr = extract_captured_sections(content)
        if not stdout.strip() and not stderr.strip():
            return "Incomplete raw output: stdout and stderr captures are empty."
    return "Incomplete raw output: required harness markers are missing."


def load_existing_outputs(models, prompts, conditions, output_dir):
    outputs = {}
    failures = {}
    for model in models:
        for condition in conditions:
            for prompt in prompts:
                key = run_key(model, condition, prompt)
                path = output_path(output_dir, *key)
                if is_completed_output(path):
                    content = path.read_text(encoding="utf-8", errors="replace")
                    outputs[key] = extract_scoring_text(content)
                elif not path.exists():
                    continue
                else:
                    failures[key] = incomplete_output_reason(path)
    return outputs, failures


def run_or_plan(
    command,
    destination: Path,
    dry_run: bool,
    timeout_seconds: int,
    stream_output: bool,
):
    print(f"{'PLAN' if dry_run else 'RUN '}: {shlex.join(command)}")
    if dry_run:
        return None, None

    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        completed = subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            check=False,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        error = f"ERROR: llama.cpp timed out after {timeout_seconds} seconds."
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        stderr = f"{stderr.rstrip()}\n{error}".lstrip()
        raw_output = format_raw_output(
            command,
            "timeout",
            stdout,
            stderr,
            marker="=== HARNESS_TIMEOUT ===",
        )
        atomic_write_text(destination, raw_output)
        print(f"RETURN CODE: timeout")
        print(f"STDOUT CHARACTERS: {len(stdout)}")
        print(f"STDERR CHARACTERS: {len(stderr)}")
        print(f"{error} Continuing to the next run.", file=sys.stderr)
        return None, error

    empty_capture = not completed.stdout.strip() and not completed.stderr.strip()
    marker = None
    if completed.returncode != 0:
        marker = "=== HARNESS_FAILURE ==="
    elif empty_capture:
        marker = "=== HARNESS_FAILURE ===\nempty stdout/stderr capture"
    raw_output = format_raw_output(
        command,
        completed.returncode,
        completed.stdout,
        completed.stderr,
        marker=marker,
    )
    atomic_write_text(destination, raw_output)
    print(f"RETURN CODE: {completed.returncode}")
    print(f"STDOUT CHARACTERS: {len(completed.stdout)}")
    print(f"STDERR CHARACTERS: {len(completed.stderr)}")
    if stream_output:
        if completed.stdout:
            print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
        if completed.stderr:
            print(
                completed.stderr,
                end="" if completed.stderr.endswith("\n") else "\n",
                file=sys.stderr,
            )
    if completed.returncode != 0:
        error = f"ERROR: llama.cpp exited with code {completed.returncode}."
        print(
            f"{error} Saved captured output and continuing to the next run.",
            file=sys.stderr,
        )
        return None, error
    if empty_capture:
        error = "ERROR: llama.cpp returned empty stdout/stderr capture."
        print(f"{error} Continuing to the next run.", file=sys.stderr)
        return None, error
    return extract_scoring_text(raw_output), None


def build_scoring_rows(
    models, prompts, rubric_by_id, conditions, output_dir, outputs, failures
):
    rows = []
    for model in models:
        for condition in conditions:
            for prompt in prompts:
                raw_path = output_path(
                    output_dir, model["model_id"], condition, prompt["prompt_id"]
                )
                output = outputs.get(
                    (model["model_id"], condition, prompt["prompt_id"])
                )
                failure = failures.get(
                    (model["model_id"], condition, prompt["prompt_id"])
                )
                for key_point_id in prompt["expected_rubric_ids"]:
                    key_point = rubric_by_id[key_point_id]
                    hit, score = ("", "")
                    notes = "Manual review required before final model lock."
                    if output is not None:
                        hit, score = keyword_prescore(output, key_point)
                    elif failure:
                        notes = f"{failure} Manual review required."
                    else:
                        notes = "Pending model run; manual review required."
                    rows.append(
                        {
                            "model_id": model["model_id"],
                            "model_name": model["display_name"],
                            "condition": condition,
                            "prompt_id": prompt["prompt_id"],
                            "prompt_category": prompt["category"],
                            "key_point_id": key_point_id,
                            "category": key_point["category"],
                            "expected_point": key_point["expected_point"],
                            "keyword_hit": hit,
                            "keyword_score": score,
                            "human_score": "",
                            "notes": notes,
                            "raw_output_path": str(raw_path),
                        }
                    )
    return rows


def write_scoring_sheet(path: Path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCORING_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def score_summary(rows, grouping):
    grouped = defaultdict(list)
    for row in rows:
        if row["keyword_score"] != "":
            grouped[tuple(row[field] for field in grouping)].append(
                int(row["keyword_score"])
            )
    return {
        key: 100 * sum(scores) / len(scores) for key, scores in grouped.items() if scores
    }


def projected_score(model, answer_score):
    if model["model_id"] == "granite-3.3-2b-instruct-q4-k-m":
        return 0.5 * answer_score + 33.5
    if model["model_id"] == "qwen2.5-1.5b-instruct-q4-k-m":
        return 0.5 * answer_score + 45.2
    return None


def markdown_table(summary, headers):
    if not summary:
        return "_Pending model runs and human review._\n"
    lines = [
        "| " + " | ".join(headers + ["Keyword pre-score"]) + " |",
        "| " + " | ".join(["---"] * (len(headers) + 1)) + " |",
    ]
    for key, score in sorted(summary.items()):
        lines.append("| " + " | ".join([*key, f"{score:.1f}%"]) + " |")
    return "\n".join(lines) + "\n"


def write_comparison_report(
    path: Path, models, conditions, rows, failures, missing_outputs
):
    model_scores = score_summary(rows, ["model_id", "condition"])
    prompt_scores = score_summary(rows, ["model_id", "condition", "prompt_id"])
    category_scores = score_summary(rows, ["model_id", "condition", "category"])

    projected_lines = []
    for model in models:
        available = [
            value for key, value in model_scores.items() if key[0] == model["model_id"]
        ]
        if available:
            answer_score = sum(available) / len(available)
            projected = projected_score(model, answer_score)
            if projected is None:
                projected_lines.append(
                    f"- {model['display_name']}: pending "
                    f"(answer score {answer_score:.1f})"
                )
            else:
                projected_lines.append(
                    f"- {model['display_name']}: {projected:.2f} "
                    f"(answer score {answer_score:.1f})"
                )
        else:
            projected_lines.append(
                f"- {model['display_name']}: pending; formula "
                f"`{model['projected_score_formula']}`"
            )

    decision_note_lines = []
    if failures:
        decision_note_lines.extend(
            f"- Incomplete: `{model_id}` / `{condition}` / `{prompt_id}`: {error}"
            for (model_id, condition, prompt_id), error in sorted(failures.items())
        )
    decision_note_lines.extend(
        f"- Missing: `{model_id}` / `{condition}` / `{prompt_id}`"
        for model_id, condition, prompt_id in missing_outputs
        if (model_id, condition, prompt_id) not in failures
    )
    decision_notes = (
        "\n".join(decision_note_lines)
        if decision_note_lines
        else "_No missing outputs or run failures._"
    )

    status = "PARTIAL" if missing_outputs or failures else "COMPLETE"
    summary = (
        f"**{status}:** {len(missing_outputs)} output(s) missing or incomplete; "
        f"{len(failures)} incomplete output(s) recorded."
    )

    report = f"""# Granite vs Qwen Comparison

## Summary

{summary}

## Models compared

{chr(10).join(f"- {model['display_name']} (`{model['model_id']}`)" for model in models)}

## Conditions compared

{chr(10).join(f"- `{condition}`" for condition in conditions)}

## Per-model answer-quality score

{markdown_table(model_scores, ['Model', 'Condition'])}
## Per-prompt score

{markdown_table(prompt_scores, ['Model', 'Condition', 'Prompt'])}
## Per-category score

{markdown_table(category_scores, ['Model', 'Condition', 'Category'])}
## Bare vs HyveGrid prompt comparison

_Compare condition-level human scores after both conditions have been reviewed._

## Projected automated score

{chr(10).join(projected_lines)}

## Decision notes

{decision_notes}

## Manual review needed

Keyword matching is only a first pass. A human reviewer must score every key point and check safety, correctness, omissions, and misleading advice before final model lock.
"""
    path.write_text(report, encoding="utf-8")


def apply_backspaces(text: str):
    cleaned = []
    for character in text:
        if character == "\b":
            if cleaned and cleaned[-1] != "\n":
                cleaned.pop()
        elif character == "\r":
            continue
        else:
            cleaned.append(character)
    return "".join(cleaned)


def clean_generated_answer(output: str, prompt_text: str):
    cleaned = apply_backspaces(output)
    prompt_marker = f"> {prompt_text}"
    if prompt_marker in cleaned:
        cleaned = cleaned.split(prompt_marker, 1)[1]
    cleaned = re.sub(
        r"^\s*\[\s*Prompt:.*?Generation:.*?\]\s*$",
        "",
        cleaned,
        flags=re.MULTILINE,
    )
    cleaned = re.sub(r"^\s*Exiting\.\.\.\s*$", "", cleaned, flags=re.MULTILINE)
    return cleaned.strip()


def keyword_review_summary(rows):
    scored = [row for row in rows if row["keyword_score"] != ""]
    hits = sum(int(row["keyword_score"]) for row in scored)
    percentage = 100 * hits / len(scored)
    lines = [f"{hits}/{len(scored)} key points ({percentage:.1f}%)"]
    for row in scored:
        result = "hit" if int(row["keyword_score"]) else "miss"
        lines.append(
            f"- [{result}] `{row['key_point_id']}` — {row['expected_point']}"
        )
    return "\n".join(lines), len(scored)


def write_human_review(path: Path, models, prompts, rows, outputs):
    model_scores = score_summary(rows, ["model_id", "condition"])
    scores = {
        model["model_id"]: model_scores[(model["model_id"], "bare")]
        for model in models
    }
    projected = {
        model["model_id"]: projected_score(model, scores[model["model_id"]])
        for model in models
    }
    granite_id = "granite-3.3-2b-instruct-q4-k-m"
    qwen_id = "qwen2.5-1.5b-instruct-q4-k-m"
    gap = projected[qwen_id] - projected[granite_id]
    rows_by_run = defaultdict(list)
    for row in rows:
        rows_by_run[(row["model_id"], row["condition"], row["prompt_id"])].append(row)

    sections = [
        "# HyveGrid Offline Bare Model Human Review",
        "",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "## Model comparison summary",
        "",
        f"- Granite bare score: {scores[granite_id]:.1f}%",
        f"- Qwen bare score: {scores[qwen_id]:.1f}%",
        f"- Granite projected score: {projected[granite_id]:.2f}",
        f"- Qwen projected score: {projected[qwen_id]:.2f}",
        f"- Projected score gap (Qwen minus Granite): {gap:.2f}",
        "",
        "## Review reminder",
        "",
        "- Keyword scoring is only a first pass.",
        "- The human reviewer should correct missed synonyms or false keyword hits.",
        "- The bare condition is closest to the ADTC scored model path.",
    ]

    model_labels = ((granite_id, "Granite"), (qwen_id, "Qwen"))
    for prompt in prompts:
        prompt_id = prompt["prompt_id"]
        sections.extend(
            [
                "",
                f"## Prompt: {prompt_id}",
                "",
                "### Prompt text",
                "",
                prompt["text"],
            ]
        )
        for model_id, label in model_labels:
            key = (model_id, "bare", prompt_id)
            summary, maximum = keyword_review_summary(rows_by_run[key])
            sections.extend(
                [
                    "",
                    f"### {label} raw answer",
                    "",
                    clean_generated_answer(outputs[key], prompt["text"]),
                    "",
                    f"### Keyword score summary for {label}",
                    "",
                    summary,
                    "",
                    f"**Human score for {label}:** ____ / {maximum}",
                ]
            )
        sections.extend(["", "### Notes", "", "______________________________"])

    atomic_write_text(path, "\n".join(sections) + "\n")


def write_artifacts(output_dir, models, prompts, rubric_by_id, conditions, outputs, failures):
    expected_keys = [
        run_key(model, condition, prompt)
        for model in models
        for condition in conditions
        for prompt in prompts
    ]
    missing_outputs = sorted(
        key for key in expected_keys if key not in outputs
    )
    rows = build_scoring_rows(
        models, prompts, rubric_by_id, conditions, output_dir, outputs, failures
    )
    write_scoring_sheet(output_dir / "scoring_sheet.csv", rows)
    write_comparison_report(
        output_dir / "comparison.md", models, conditions, rows, failures, missing_outputs
    )
    return missing_outputs


def filter_by_ids(items, field, requested_ids, label):
    if not requested_ids:
        return items
    available = {item[field] for item in items}
    unknown = sorted(set(requested_ids) - available)
    if unknown:
        raise ValueError(f"Unknown {label}: {', '.join(unknown)}")
    requested = set(requested_ids)
    return [item for item in items if item[field] in requested]


def build_jobs(models, prompts, conditions, output_dir):
    return [
        {
            "model": model,
            "condition": condition,
            "prompt": prompt,
            "key": run_key(model, condition, prompt),
            "destination": output_path(
                output_dir, model["model_id"], condition, prompt["prompt_id"]
            ),
        }
        for model in models
        for condition in conditions
        for prompt in prompts
    ]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models-config", default="tests/model_candidates.yaml")
    parser.add_argument("--prompts", default="tests/eval_prompts.yaml")
    parser.add_argument("--rubric", default="tests/eval_rubric.yaml")
    parser.add_argument("--output-dir", default="artifacts/eval")
    parser.add_argument(
        "--llama-cli-path", default="./llama.cpp/build/bin/llama-cli"
    )
    parser.add_argument("--condition", choices=["bare", "hyvegrid", "both"], default="both")
    parser.add_argument(
        "--model-id",
        action="append",
        help="Run only the selected model ID; may be supplied more than once.",
    )
    parser.add_argument(
        "--prompt-id",
        action="append",
        help="Run only the selected prompt ID; may be supplied more than once.",
    )
    parser.add_argument(
        "--max-runs",
        type=int,
        help="Run at most the first N pending combinations after filtering.",
    )
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument(
        "--list-jobs",
        action="store_true",
        help="List filtered job paths and completion status without running inference.",
    )
    parser.add_argument(
        "--score-existing-only",
        action="store_true",
        help="Generate reports from existing raw outputs without running llama.cpp.",
    )
    parser.add_argument(
        "--write-human-review",
        action="store_true",
        help="Write a complete bare-condition human-review package without inference.",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--stream-output",
        action="store_true",
        help="Display captured llama.cpp output in the terminal after saving it.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=180,
        help="Maximum seconds allowed for each llama.cpp run (default: 180).",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate configuration files without planning or running inference.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    models = load_yaml(Path(args.models_config))["models"]
    prompts = load_yaml(Path(args.prompts))["prompts"]
    rubric = load_yaml(Path(args.rubric))["key_points"]
    validate_inputs(models, prompts, rubric)

    if args.validate_only:
        print(
            f"Validation successful: {len(models)} models, {len(prompts)} prompts, "
            f"and {len(rubric)} rubric key points."
        )
        return

    if args.max_runs is not None and args.max_runs < 0:
        raise ValueError("--max-runs must be zero or greater.")

    models = filter_by_ids(models, "model_id", args.model_id, "model IDs")
    prompts = filter_by_ids(prompts, "prompt_id", args.prompt_id, "prompt IDs")

    if args.write_human_review and (
        args.condition != "bare" or args.model_id or args.prompt_id
    ):
        raise ValueError(
            "--write-human-review requires --condition bare with all models and prompts."
        )

    output_dir = Path(args.output_dir)
    conditions = selected_conditions(args.condition)
    jobs = build_jobs(models, prompts, conditions, output_dir)

    if args.list_jobs:
        for job in jobs:
            print(
                f"model_id: {job['model']['model_id']} | "
                f"condition: {job['condition']} | "
                f"prompt_id: {job['prompt']['prompt_id']} | "
                f"raw_output_path: {job['destination']} | "
                f"status: {output_status(job['destination'])}"
            )
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    rubric_by_id = {point["key_point_id"]: point for point in rubric}
    outputs, failures = load_existing_outputs(
        models, prompts, conditions, output_dir
    )
    if args.write_human_review:
        expected_keys = {
            run_key(model, "bare", prompt)
            for model in models
            for prompt in prompts
        }
        missing_outputs = sorted(expected_keys - set(outputs))
        if missing_outputs or failures:
            raise ValueError(
                "Cannot write human review: bare condition is incomplete "
                f"({len(missing_outputs)} missing or incomplete output(s))."
            )
        rows = build_scoring_rows(
            models, prompts, rubric_by_id, conditions, output_dir, outputs, failures
        )
        review_path = output_dir / "bare-human-review.md"
        write_human_review(review_path, models, prompts, rows, outputs)
        print(f"Wrote {review_path}")
        print("Human-review export complete; llama.cpp was not executed.")
        return
    interrupted = False

    selected_jobs = []
    if not args.score_existing_only:
        for job in jobs:
            if args.skip_existing and is_completed_output(job["destination"]):
                print(f"SKIP: completed output: {job['destination']}")
                continue
            selected_jobs.append(job)
        if args.max_runs is not None:
            selected_jobs = selected_jobs[: args.max_runs]

    try:
        for job in selected_jobs:
            key = job["key"]
            destination = job["destination"]
            status = output_status(destination)
            print(
                f"DESTINATION: {destination} | "
                f"exists: {'yes' if destination.exists() else 'no'} | "
                f"status: {status}"
            )
            command = build_command(
                args.llama_cli_path,
                job["model"],
                job["prompt"],
                job["condition"],
            )
            output, failure = run_or_plan(
                command,
                destination,
                args.dry_run,
                args.timeout_seconds,
                args.stream_output,
            )
            if output is not None:
                outputs[key] = output
                failures.pop(key, None)
            if failure is not None:
                failures[key] = failure
                outputs.pop(key, None)
            if output is not None or failure is not None:
                write_artifacts(
                    output_dir,
                    models,
                    prompts,
                    rubric_by_id,
                    conditions,
                    outputs,
                    failures,
                )
    except KeyboardInterrupt:
        interrupted = True

    missing_outputs = write_artifacts(
        output_dir,
        models,
        prompts,
        rubric_by_id,
        conditions,
        outputs,
        failures,
    )
    print(f"Wrote {output_dir / 'scoring_sheet.csv'}")
    print(f"Wrote {output_dir / 'comparison.md'}")
    print(f"Missing outputs: {len(missing_outputs)}")
    if args.dry_run:
        print("Dry run complete; llama.cpp was not executed.")
    if args.score_existing_only:
        print("Existing-output scoring complete; llama.cpp was not executed.")
    if interrupted:
        print(
            "Run interrupted; partial reports were written. Resume with --skip-existing.",
            file=sys.stderr,
        )
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
