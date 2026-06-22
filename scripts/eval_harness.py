#!/usr/bin/env python3
"""Local Granite vs Qwen evaluation harness for HyveGrid Offline."""

import argparse
import ast
import csv
import shlex
import subprocess
import sys
from collections import defaultdict
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
    if len(models) != 2:
        raise ValueError("Model config must contain exactly two candidates.")
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


def run_or_plan(command, destination: Path, dry_run: bool):
    print(f"{'PLAN' if dry_run else 'RUN '}: {shlex.join(command)}")
    if dry_run:
        return None

    destination.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    destination.write_text(completed.stdout, encoding="utf-8")
    if completed.returncode != 0:
        print(completed.stderr, file=sys.stderr)
        raise RuntimeError(
            f"llama.cpp failed with exit code {completed.returncode}: {destination}"
        )
    return completed.stdout


def build_scoring_rows(models, prompts, rubric_by_id, conditions, output_dir, outputs):
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
                for key_point_id in prompt["expected_rubric_ids"]:
                    key_point = rubric_by_id[key_point_id]
                    hit, score = ("", "")
                    notes = "Manual review required before final model lock."
                    if output is not None:
                        hit, score = keyword_prescore(output, key_point)
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


def write_comparison_report(path: Path, models, conditions, rows):
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
            if model["model_id"] == "granite-3.3-2b-instruct-q4-k-m":
                projected = 0.5 * answer_score + 33.5
            else:
                projected = 0.5 * answer_score + 45.2
            projected_lines.append(
                f"- {model['display_name']}: {projected:.2f} "
                f"(answer score {answer_score:.1f})"
            )
        else:
            projected_lines.append(
                f"- {model['display_name']}: pending; formula "
                f"`{model['projected_score_formula']}`"
            )

    report = f"""# Granite vs Qwen Comparison

## Summary

Evaluation scaffold created. Results remain pending until model runs and human review are complete.

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

_Pending completed model runs and reviewer notes._

## Manual review needed

Keyword matching is only a first pass. A human reviewer must score every key point and check safety, correctness, omissions, and misleading advice before final model lock.
"""
    path.write_text(report, encoding="utf-8")


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
    parser.add_argument("--dry-run", action="store_true")
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

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    conditions = selected_conditions(args.condition)
    rubric_by_id = {point["key_point_id"]: point for point in rubric}
    outputs = {}

    for model in models:
        for condition in conditions:
            for prompt in prompts:
                destination = output_path(
                    output_dir, model["model_id"], condition, prompt["prompt_id"]
                )
                destination.parent.mkdir(parents=True, exist_ok=True)
                command = build_command(args.llama_cli_path, model, prompt, condition)
                output = run_or_plan(command, destination, args.dry_run)
                if output is not None:
                    outputs[(model["model_id"], condition, prompt["prompt_id"])] = output

    rows = build_scoring_rows(
        models, prompts, rubric_by_id, conditions, output_dir, outputs
    )
    write_scoring_sheet(output_dir / "scoring_sheet.csv", rows)
    write_comparison_report(output_dir / "comparison.md", models, conditions, rows)
    print(f"Wrote {output_dir / 'scoring_sheet.csv'}")
    print(f"Wrote {output_dir / 'comparison.md'}")
    if args.dry_run:
        print("Dry run complete; llama.cpp was not executed.")


if __name__ == "__main__":
    main()
