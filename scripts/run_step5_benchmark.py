#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


LOG_LINE_RE = re.compile(r"^\d+\.\d+\.\d+\.\d+\s+[IWE]\s+")


def parse_model_arg(value: str):
    if "=" not in value:
        raise argparse.ArgumentTypeError("Use name=/path/to/model.gguf")
    name, path = value.split("=", 1)
    return name.strip(), Path(path.strip())


def read_prompts(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def clean_llama_output(stdout: str) -> str:
    """
    llama-completion may force interactive mode when a chat template is present.
    We pipe /exit to close it. This function removes logs, interactive shell text,
    and the extra /exit response from the review output.
    """
    if not stdout:
        return ""

    # Cut off the forced /exit section.
    stdout = stdout.split("> /exit", 1)[0]

    cleaned_lines = []
    skip_prefixes = (
        "build      :",
        "model      :",
        "modalities :",
        "available commands:",
        "/exit or Ctrl+C",
        "/regen",
        "/clear",
        "/read ",
        "/glob ",
        "== Running in interactive mode. ==",
        "- Press Ctrl+C",
        "- Press Return",
        "- To return control",
        "- If you want",
        "- Not using system message",
    )

    for raw_line in stdout.splitlines():
        line = raw_line.rstrip()

        if not line.strip():
            cleaned_lines.append("")
            continue

        if LOG_LINE_RE.match(line):
            continue

        if line.strip().startswith(skip_prefixes):
            continue

        if line.strip() in {">", "EOF by user"}:
            continue

        # Remove llama ASCII logo block crudely by skipping obvious block characters.
        if set(line.strip()) <= set("▄█▀ ██"):
            continue

        cleaned_lines.append(line)

    answer = "\n".join(cleaned_lines).strip()

    # Remove excessive leading blank/log leftovers.
    answer = re.sub(r"\n{3,}", "\n\n", answer)

    return answer.strip()


def run_one(llama_binary, model_name, model_path, prompt_row, args):
    prompt = prompt_row["prompt"]

    cmd = [
        llama_binary,
        "-m", str(model_path),
        "-p", prompt,
        "-n", str(args.max_tokens),
        "-c", str(args.ctx),
        "--temp", str(args.temp),
        "--top-p", str(args.top_p),
        "--repeat-penalty", str(args.repeat_penalty),
        "--threads", str(args.threads),
        "--no-display-prompt",
    ]

    started = time.time()

    try:
        proc = subprocess.run(
            cmd,
            input="/exit\n",
            text=True,
            capture_output=True,
            timeout=args.timeout,
        )
    except subprocess.TimeoutExpired as exc:
        class TimeoutResult:
            returncode = 124
            stdout = exc.stdout or ""
            stderr = (exc.stderr or "") + "\nTIMEOUT: process exceeded timeout."

        proc = TimeoutResult()

    elapsed = time.time() - started

    clean_output = clean_llama_output(proc.stdout)

    return {
        "model": model_name,
        "model_path": str(model_path),
        "prompt_id": prompt_row["id"],
        "category": prompt_row.get("category", ""),
        "prompt": prompt,
        "command": cmd,
        "returncode": proc.returncode,
        "elapsed_seconds": round(elapsed, 2),
        "stdout": proc.stdout.strip(),
        "clean_output": clean_output,
        "stderr": proc.stderr.strip(),
    }


def main():
    parser = argparse.ArgumentParser(description="Run Step 5 HyveGrid model accuracy benchmark.")
    parser.add_argument("--llama-cli", default="llama-completion")
    parser.add_argument("--prompts", default="tests/benchmark/step5_prompts.jsonl")
    parser.add_argument("--model", action="append", type=parse_model_arg, required=True)
    parser.add_argument("--outdir", default=None)
    parser.add_argument("--ctx", type=int, default=1024)
    parser.add_argument("--max-tokens", type=int, default=180)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--temp", type=float, default=0.2)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--repeat-penalty", type=float, default=1.05)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--no-display-prompt", action="store_true")
    args = parser.parse_args()

    prompts_path = Path(args.prompts)
    prompts = read_prompts(prompts_path)

    if args.outdir:
        outdir = Path(args.outdir)
    else:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        outdir = Path("artifacts") / "step5" / stamp

    outdir.mkdir(parents=True, exist_ok=True)

    results_path = outdir / "raw_outputs.jsonl"
    review_path = outdir / "review_pack.md"

    all_results = []

    for model_name, model_path in args.model:
        if not model_path.exists():
            print(f"Missing model path: {model_path}", file=sys.stderr)
            sys.exit(1)

        for prompt_row in prompts:
            print(f"Running {model_name} on {prompt_row['id']}...")
            result = run_one(args.llama_cli, model_name, model_path, prompt_row, args)
            all_results.append(result)

            with results_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")

    with review_path.open("w", encoding="utf-8") as f:
        f.write("# HyveGrid Offline Step 5 Review Pack\n\n")
        f.write("Manual scoring required. Score each response from 0 to 5 against the Step 5 scoring file and model matrix.\n\n")

        for result in all_results:
            f.write(f"## {result['model']} - {result['prompt_id']}\n\n")
            f.write(f"**Category:** {result['category']}\n\n")
            f.write("**Prompt:**\n\n")
            f.write(result["prompt"] + "\n\n")
            f.write("**Clean output for scoring:**\n\n")
            f.write("```text\n")
            f.write(result["clean_output"] + "\n")
            f.write("```\n\n")

            f.write(f"**Elapsed seconds:** {result['elapsed_seconds']}\n\n")

            if result["returncode"] != 0:
                f.write(f"**Return code:** {result['returncode']}\n\n")

            if result["stderr"]:
                f.write("**stderr:**\n\n")
                f.write("```text\n")
                f.write(result["stderr"][:2500] + "\n")
                f.write("```\n\n")

            f.write("**Manual score:** ___ / 5\n\n")
            f.write("**Notes:**\n\n")
            f.write("- \n\n")

    print(f"\nSaved raw outputs to: {results_path}")
    print(f"Saved review pack to: {review_path}")


if __name__ == "__main__":
    main()
