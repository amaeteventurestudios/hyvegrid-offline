#!/usr/bin/env python3
"""Process guided field walkthrough raw sprite sources into runtime sheets."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "artifacts" / "source" / "walkthrough-raw"
SOURCE_DIR = ROOT / "app" / "static" / "assets" / "source"
RUNTIME_DIR = ROOT / "app" / "static" / "assets" / "walkthrough"
MANIFEST_PATH = RUNTIME_DIR / "walkthrough-manifest.json"
AUDIT_PATH = ROOT / "artifacts" / "eval" / "walkthrough-asset-processing-task-035C.md"

ALPHA_CROP_THRESHOLD = 200
ALPHA_CLEAN_THRESHOLD = 36


@dataclass(frozen=True)
class AssetSpec:
    key: str
    raw_name: str
    source_name: str
    runtime_name: str
    frames: int
    frame_width: int
    frame_height: int
    type: str
    intended_use: str
    anchor: str | None = None


SPECS = [
    AssetSpec(
        key="bee_micro_sprite",
        raw_name="bee_micro_raw.png",
        source_name="bee-micro-sprite.png",
        runtime_name="bee-micro-sprite.webp",
        frames=6,
        frame_width=32,
        frame_height=32,
        type="micro-sprite",
        intended_use="scripted hover near hive entrance",
    ),
    AssetSpec(
        key="ant_micro_sprite",
        raw_name="ant_micro_raw.png",
        source_name="ant-micro-sprite.png",
        runtime_name="ant-micro-sprite.webp",
        frames=6,
        frame_width=32,
        frame_height=32,
        type="micro-sprite",
        intended_use="scripted march near hive stand",
    ),
    AssetSpec(
        key="keeper_inspect_sprite",
        raw_name="keeper_inspect_raw.png",
        source_name="keeper-inspect-sprite.png",
        runtime_name="keeper-inspect-sprite.webp",
        frames=4,
        frame_width=96,
        frame_height=96,
        type="keeper-inspect",
        intended_use="scripted inspection pause",
        anchor="bottom-center-foot-contact",
    ),
    AssetSpec(
        key="keeper_walk_sprite",
        raw_name="keeper_walk_raw.png",
        source_name="keeper-walk-sprite.png",
        runtime_name="keeper-walk-sprite.webp",
        frames=8,
        frame_width=96,
        frame_height=96,
        type="keeper-walk",
        intended_use="scripted route walking loop",
        anchor="bottom-center-foot-contact",
    ),
]


def alpha_mask(image: Image.Image, threshold: int) -> Image.Image:
    return image.getchannel("A").point(lambda value: 255 if value > threshold else 0)


def x_runs(mask: Image.Image) -> list[tuple[int, int]]:
    pixels = mask.load()
    width, height = mask.size
    runs: list[tuple[int, int]] = []
    in_run = False
    start = 0

    for x in range(width):
        has_pixel = any(pixels[x, y] for y in range(height))
        if has_pixel and not in_run:
            start = x
            in_run = True
        elif not has_pixel and in_run:
            runs.append((start, x))
            in_run = False

    if in_run:
        runs.append((start, width))

    merged: list[tuple[int, int]] = []
    for run in runs:
        if merged and run[0] - merged[-1][1] < 10:
            merged[-1] = (merged[-1][0], run[1])
        else:
            merged.append(run)
    return merged


def clean_alpha(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    red, green, blue, alpha = image.split()
    alpha = alpha.point(lambda value: 0 if value < ALPHA_CLEAN_THRESHOLD else value)
    return Image.merge("RGBA", (red, green, blue, alpha))


def crop_frame(image: Image.Image, run: tuple[int, int]) -> Image.Image:
    x0, x1 = run
    mask = alpha_mask(image, ALPHA_CROP_THRESHOLD)
    frame_mask = mask.crop((x0, 0, x1, image.height))
    bbox = frame_mask.getbbox()
    if not bbox:
        raise ValueError(f"No opaque frame content found for x-run {run}")

    left = max(x0 + bbox[0] - 10, 0)
    top = max(bbox[1] - 10, 0)
    right = min(x0 + bbox[2] + 10, image.width)
    bottom = min(bbox[3] + 10, image.height)
    return clean_alpha(image.crop((left, top, right, bottom)))


def fit_to_frame(frame: Image.Image, width: int, height: int) -> Image.Image:
    bbox = alpha_mask(frame, ALPHA_CLEAN_THRESHOLD).getbbox()
    if bbox:
        frame = frame.crop(bbox)

    scale = min(width / frame.width, height / frame.height)
    resized_size = (
        max(1, round(frame.width * scale)),
        max(1, round(frame.height * scale)),
    )
    frame = frame.resize(resized_size, Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    x = (width - frame.width) // 2
    y = height - frame.height
    canvas.alpha_composite(frame, (x, y))
    return canvas


def process_asset(spec: AssetSpec) -> dict[str, object]:
    raw_path = RAW_DIR / spec.raw_name
    if not raw_path.exists():
        raise FileNotFoundError(raw_path)

    image = Image.open(raw_path).convert("RGBA")
    runs = x_runs(alpha_mask(image, ALPHA_CROP_THRESHOLD))
    if len(runs) < spec.frames:
        raise ValueError(
            f"{spec.raw_name} has {len(runs)} detected frames; {spec.frames} required"
        )

    selected_runs = runs[: spec.frames]
    sheet = Image.new(
        "RGBA",
        (spec.frame_width * spec.frames, spec.frame_height),
        (0, 0, 0, 0),
    )
    for index, run in enumerate(selected_runs):
        frame = fit_to_frame(crop_frame(image, run), spec.frame_width, spec.frame_height)
        sheet.alpha_composite(frame, (index * spec.frame_width, 0))

    source_path = SOURCE_DIR / spec.source_name
    runtime_path = RUNTIME_DIR / spec.runtime_name
    source_path.parent.mkdir(parents=True, exist_ok=True)
    runtime_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(source_path)
    sheet.save(runtime_path, format="WEBP", lossless=True, method=6)

    return {
        "rawPath": str(raw_path.relative_to(ROOT)),
        "sourcePath": str(source_path.relative_to(ROOT)),
        "runtimePath": str(runtime_path.relative_to(ROOT)),
        "detectedSourceFrames": len(runs),
        "selectedFrames": spec.frames,
        "frameWidth": spec.frame_width,
        "frameHeight": spec.frame_height,
        "sheetWidth": sheet.width,
        "sheetHeight": sheet.height,
        "hasAlpha": "A" in sheet.getbands(),
        "sourceBytes": source_path.stat().st_size,
        "runtimeBytes": runtime_path.stat().st_size,
    }


def image_info(path: Path, frames: int) -> dict[str, object]:
    image = Image.open(path)
    return {
        "path": str(path.relative_to(ROOT)),
        "dimensions": f"{image.width} x {image.height}",
        "frameCount": frames,
        "frameWidth": image.width // frames,
        "frameHeight": image.height,
        "hasAlpha": image.mode in {"RGBA", "LA"} or "transparency" in image.info,
        "fileSize": path.stat().st_size,
    }


def update_manifest(results: dict[str, dict[str, object]]) -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())
    assets = manifest.setdefault("assets", {})

    for spec in SPECS:
        result = results[spec.key]
        entry = {
            "type": spec.type,
            "sourcePath": result["sourcePath"],
            "runtimePath": result["runtimePath"],
            "frameWidth": result["frameWidth"],
            "frameHeight": result["frameHeight"],
            "frameCount": result["selectedFrames"],
            "sheetWidth": result["sheetWidth"],
            "sheetHeight": result["sheetHeight"],
            "intendedUse": spec.intended_use,
        }
        if spec.anchor:
            entry["anchor"] = spec.anchor
        assets[spec.key] = entry

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n")


def write_audit(results: dict[str, dict[str, object]]) -> None:
    lines = [
        "# Task 035C Walkthrough Asset Processing Audit",
        "",
        "## Task Summary",
        "",
        "Task 035C cleaned local raw source images into transparent source PNG and",
        "runtime WebP sprite sheets for the guided field walkthrough. No app",
        "behavior, routes, templates, advisor pages, model/runtime/scoring files,",
        "retrieval code, metadata, report files, or model files were changed.",
        "",
        "## Raw Input Files Found",
        "",
    ]

    for spec in SPECS:
        raw_path = RAW_DIR / spec.raw_name
        lines.append(f"- `{raw_path.relative_to(ROOT)}`")
    reference = RAW_DIR / "combined_reference_do_not_import.png"
    if reference.exists():
        lines.append(f"- `{reference.relative_to(ROOT)}` present but not imported")

    lines.extend(["", "## Output Files Created", ""])
    for spec in SPECS:
        result = results[spec.key]
        lines.append(f"- `{result['sourcePath']}`")
        lines.append(f"- `{result['runtimePath']}`")

    lines.extend(["", "## Asset Measurements", ""])
    lines.append("| Output | Dimensions | Frames | Frame width | Frame height | Alpha | File size |")
    lines.append("| --- | --- | ---: | ---: | ---: | --- | ---: |")
    for spec in SPECS:
        for path in [SOURCE_DIR / spec.source_name, RUNTIME_DIR / spec.runtime_name]:
            info = image_info(path, spec.frames)
            lines.append(
                f"| `{info['path']}` | {info['dimensions']} | {info['frameCount']} | "
                f"{info['frameWidth']} | {info['frameHeight']} | "
                f"{'yes' if info['hasAlpha'] else 'no'} | {info['fileSize']} bytes |"
            )

    lines.extend(
        [
            "",
            "## Asset Quality Notes",
            "",
            "- Raw bee and ant sheets contained seven detected poses; the processor used",
            "  the first six to match the required six-frame targets.",
            "- Raw keeper inspect sheet contained five detected poses; the processor used",
            "  the first four to match the required four-frame target.",
            "- Raw keeper walk sheet contained eight detected poses and all eight were",
            "  used.",
            "- Low-alpha background speckles and glow were removed using the alpha channel;",
            "  black artwork pixels were not globally converted to transparency.",
            "- The combined reference image was not copied into `app/static/assets`.",
            "",
            "## Confirmations",
            "",
            "- No app behavior was changed.",
            "- No animation was integrated into the UI.",
            "- No model/runtime/scoring files were changed.",
            "- No routes, templates, advisor pages, retrieval code, `metadata.json`,",
            "  `download_model.sh`, `REPORT.md`, or model files were changed.",
            "- No Phaser, WebGL, canvas, CDN, cloud APIs, external runtime services, or",
            "  internet dependencies were added.",
            "- Combined/reference images were not imported.",
        ]
    )
    AUDIT_PATH.write_text("\n".join(lines) + "\n")


def main() -> None:
    results: dict[str, dict[str, object]] = {}
    for spec in SPECS:
        results[spec.key] = process_asset(spec)
    update_manifest(results)
    write_audit(results)

    print("Processed walkthrough assets:")
    for key, result in results.items():
        print(
            f"- {key}: {result['sheetWidth']}x{result['sheetHeight']} "
            f"({result['selectedFrames']} frames)"
        )


if __name__ == "__main__":
    main()
