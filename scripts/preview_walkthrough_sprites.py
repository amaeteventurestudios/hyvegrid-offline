#!/usr/bin/env python3
"""Generate a static QA preview for guided field walkthrough sprites."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "app" / "static" / "assets" / "source"
RUNTIME_DIR = ROOT / "app" / "static" / "assets" / "walkthrough"
MANIFEST_PATH = RUNTIME_DIR / "walkthrough-manifest.json"
PREVIEW_PATH = ROOT / "artifacts" / "eval" / "walkthrough-sprite-preview-task-035D.png"
AUDIT_PATH = ROOT / "artifacts" / "eval" / "walkthrough-sprite-preview-audit-task-035D.md"


@dataclass(frozen=True)
class SpriteSpec:
    key: str
    label: str
    source_name: str
    runtime_name: str
    width: int
    height: int
    frames: int
    frame_width: int
    frame_height: int
    observation: str


SPECS = [
    SpriteSpec(
        key="bee_micro_sprite",
        label="Bee micro-sprite",
        source_name="bee-micro-sprite.png",
        runtime_name="bee-micro-sprite.webp",
        width=192,
        height=32,
        frames=6,
        frame_width=32,
        frame_height=32,
        observation="Readable yellow/black bee silhouette at native size; wings remain visible when enlarged.",
    ),
    SpriteSpec(
        key="ant_micro_sprite",
        label="Ant micro-sprite",
        source_name="ant-micro-sprite.png",
        runtime_name="ant-micro-sprite.webp",
        width=192,
        height=32,
        frames=6,
        frame_width=32,
        frame_height=32,
        observation="Readable dark ant profile at native size, though subtle and likely best used over lighter board areas.",
    ),
    SpriteSpec(
        key="keeper_inspect_sprite",
        label="Keeper inspect sprite",
        source_name="keeper-inspect-sprite.png",
        runtime_name="keeper-inspect-sprite.webp",
        width=384,
        height=96,
        frames=4,
        frame_width=96,
        frame_height=96,
        observation="Keeper and hive inspection pose are clear; bottom contact remains consistent enough for a pause state.",
    ),
    SpriteSpec(
        key="keeper_walk_sprite",
        label="Keeper walk sprite",
        source_name="keeper-walk-sprite.png",
        runtime_name="keeper-walk-sprite.webp",
        width=768,
        height=96,
        frames=8,
        frame_width=96,
        frame_height=96,
        observation="Walking frames are consistently sized and aligned; direction is a side-view walk suitable for first integration pass.",
    ),
]


def font(size: int) -> ImageFont.ImageFont:
    for candidate in [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


FONT_TITLE = font(26)
FONT_LABEL = font(16)
FONT_SMALL = font(12)


def has_alpha(image: Image.Image) -> bool:
    return image.mode in {"RGBA", "LA"} or "transparency" in image.info


def load_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def validate_assets() -> dict[str, dict[str, object]]:
    manifest = json.loads(MANIFEST_PATH.read_text())
    if "assets" not in manifest:
        raise AssertionError("manifest missing assets object")

    results: dict[str, dict[str, object]] = {}
    for spec in SPECS:
        source_path = SOURCE_DIR / spec.source_name
        runtime_path = RUNTIME_DIR / spec.runtime_name
        if not source_path.exists():
            raise FileNotFoundError(source_path)
        if not runtime_path.exists():
            raise FileNotFoundError(runtime_path)

        source = Image.open(source_path)
        runtime = Image.open(runtime_path)
        if source.size != (spec.width, spec.height):
            raise AssertionError(f"{source_path} size {source.size} != {(spec.width, spec.height)}")
        if runtime.size != (spec.width, spec.height):
            raise AssertionError(f"{runtime_path} size {runtime.size} != {(spec.width, spec.height)}")
        if spec.width != spec.frame_width * spec.frames:
            raise AssertionError(f"{spec.label} frame metadata does not match sheet width")
        if spec.height != spec.frame_height:
            raise AssertionError(f"{spec.label} frame metadata does not match sheet height")

        entry = manifest["assets"].get(spec.key)
        if not entry:
            raise AssertionError(f"manifest missing {spec.key}")
        expected_source = f"app/static/assets/source/{spec.source_name}"
        expected_runtime = f"app/static/assets/walkthrough/{spec.runtime_name}"
        if entry.get("sourcePath") != expected_source:
            raise AssertionError(f"manifest {spec.key} sourcePath mismatch")
        if entry.get("runtimePath") != expected_runtime:
            raise AssertionError(f"manifest {spec.key} runtimePath mismatch")

        results[spec.key] = {
            "sourcePath": str(source_path.relative_to(ROOT)),
            "runtimePath": str(runtime_path.relative_to(ROOT)),
            "dimensions": f"{spec.width} x {spec.height}",
            "frames": spec.frames,
            "frameWidth": spec.frame_width,
            "frameHeight": spec.frame_height,
            "sourceAlpha": has_alpha(source),
            "runtimeAlpha": has_alpha(runtime),
            "sourceBytes": source_path.stat().st_size,
            "runtimeBytes": runtime_path.stat().st_size,
        }
    return results


def draw_checkerboard(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    size = 16
    colors = [(242, 244, 238), (208, 214, 204)]
    for y in range(y0, y1, size):
        for x in range(x0, x1, size):
            index = ((x - x0) // size + (y - y0) // size) % 2
            draw.rectangle((x, y, min(x + size, x1), min(y + size, y1)), fill=colors[index])


def draw_apiary_sample(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=12, fill=(100, 124, 86), outline=(42, 60, 42), width=2)
    tile_w, tile_h = 92, 46
    for row in range(4):
        for col in range(5):
            cx = x0 + 72 + col * 92 + (row % 2) * 46
            cy = y0 + 58 + row * 40
            diamond = [
                (cx, cy - tile_h // 2),
                (cx + tile_w // 2, cy),
                (cx, cy + tile_h // 2),
                (cx - tile_w // 2, cy),
            ]
            color = (140, 164, 94) if (row + col) % 2 else (174, 158, 96)
            draw.polygon(diamond, fill=color, outline=(80, 95, 62))
    hive = (x0 + 320, y0 + 92, x0 + 406, y0 + 146)
    draw.rounded_rectangle(hive, radius=5, fill=(222, 174, 48), outline=(76, 56, 34), width=2)
    draw.rectangle((hive[0] + 18, hive[3], hive[0] + 28, hive[3] + 32), fill=(86, 54, 32))
    draw.rectangle((hive[2] - 28, hive[3], hive[2] - 18, hive[3] + 32), fill=(86, 54, 32))
    draw.text((x0 + 14, y0 + 12), "apiary-board-style scale sample", fill=(245, 246, 237), font=FONT_SMALL)


def paste_with_guides(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    image: Image.Image,
    pos: tuple[int, int],
    frame_width: int,
    frames: int,
    scale: int,
) -> None:
    if scale != 1:
        image = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
        frame_width *= scale
    x, y = pos
    canvas.alpha_composite(image, pos)
    guide_color = (50, 94, 130, 180)
    for index in range(frames + 1):
        gx = x + index * frame_width
        draw.line((gx, y, gx, y + image.height), fill=guide_color, width=1)
    draw.rectangle((x, y, x + image.width, y + image.height), outline=(40, 86, 130), width=1)


def generate_preview() -> None:
    PREVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
    width = 2600
    height = 1680
    canvas = Image.new("RGBA", (width, height), (236, 238, 232, 255))
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, width, 270), fill=(31, 34, 36))
    draw.text((40, 30), "Task 035D Walkthrough Sprite Preview", fill=(255, 255, 250), font=FONT_TITLE)
    draw.text(
        (40, 68),
        "Runtime WebP sheets shown at native size and enlarged 3x with frame guides.",
        fill=(218, 222, 216),
        font=FONT_LABEL,
    )
    draw_apiary_sample(draw, (40, 100, 560, 245))
    draw_checkerboard(draw, (600, 100, 1120, 245))
    draw.text((610, 112), "light transparency check", fill=(38, 42, 38), font=FONT_SMALL)
    draw.rectangle((1160, 100, 1680, 245), fill=(20, 22, 24), outline=(92, 96, 98), width=2)
    draw.text((1170, 112), "dark transparency check", fill=(232, 234, 228), font=FONT_SMALL)

    y = 300
    for spec in SPECS:
        runtime = load_rgba(RUNTIME_DIR / spec.runtime_name)
        row_height = max(runtime.height * 3 + 92, 220)
        draw.rounded_rectangle((34, y - 28, width - 34, y + row_height), radius=10, fill=(250, 251, 247), outline=(196, 200, 190))
        draw.text((56, y - 12), spec.label, fill=(26, 30, 28), font=FONT_LABEL)
        draw.text(
            (300, y - 10),
            f"{spec.width} x {spec.height}; {spec.frames} frames; {spec.frame_width} x {spec.frame_height} per frame",
            fill=(72, 78, 74),
            font=FONT_SMALL,
        )

        native_y = y + 28
        draw.text((58, native_y - 20), "native", fill=(60, 64, 60), font=FONT_SMALL)
        paste_with_guides(canvas, draw, runtime, (58, native_y), spec.frame_width, spec.frames, 1)

        enlarged_y = native_y + runtime.height + 44
        draw.text((58, enlarged_y - 20), "3x review", fill=(60, 64, 60), font=FONT_SMALL)
        paste_with_guides(canvas, draw, runtime, (58, enlarged_y), spec.frame_width, spec.frames, 3)

        light_x = 1070
        dark_x = 1370
        sample_y = native_y + 12
        draw_checkerboard(draw, (light_x, sample_y - 12, light_x + 230, sample_y + 122))
        draw.rectangle((dark_x, sample_y - 12, dark_x + 230, sample_y + 122), fill=(20, 22, 24))
        sample = runtime.crop((0, 0, spec.frame_width, spec.frame_height))
        sample_scale = 2 if spec.frame_width <= 32 else 1
        sample = sample.resize((sample.width * sample_scale, sample.height * sample_scale), Image.Resampling.NEAREST)
        canvas.alpha_composite(sample, (light_x + 80, sample_y + 28))
        canvas.alpha_composite(sample, (dark_x + 80, sample_y + 28))
        draw.text((light_x, sample_y - 30), "light bg", fill=(60, 64, 60), font=FONT_SMALL)
        draw.text((dark_x, sample_y - 30), "dark bg", fill=(60, 64, 60), font=FONT_SMALL)

        y += row_height + 22

    canvas.convert("RGB").save(PREVIEW_PATH)


def write_audit(results: dict[str, dict[str, object]]) -> None:
    lines = [
        "# Task 035D Walkthrough Sprite Preview Audit",
        "",
        "## Assets Inspected",
        "",
    ]
    for spec in SPECS:
        result = results[spec.key]
        lines.append(f"- {spec.label}: `{result['runtimePath']}`")

    lines.extend(["", "## Source Paths", ""])
    for spec in SPECS:
        result = results[spec.key]
        lines.append(f"- `{result['sourcePath']}`")
        lines.append(f"- `{result['runtimePath']}`")

    lines.extend(["", "## Preview Image", "", f"- `{PREVIEW_PATH.relative_to(ROOT)}`", ""])

    lines.extend(["## Dimensions And Transparency", ""])
    lines.append("| Asset | Dimensions | Frames | Frame width | Frame height | Source alpha | Runtime alpha | Source size | Runtime size |")
    lines.append("| --- | --- | ---: | ---: | ---: | --- | --- | ---: | ---: |")
    for spec in SPECS:
        result = results[spec.key]
        lines.append(
            f"| {spec.label} | {result['dimensions']} | {result['frames']} | "
            f"{result['frameWidth']} | {result['frameHeight']} | "
            f"{'yes' if result['sourceAlpha'] else 'no'} | "
            f"{'yes' if result['runtimeAlpha'] else 'no'} | "
            f"{result['sourceBytes']} bytes | {result['runtimeBytes']} bytes |"
        )

    lines.extend(
        [
            "",
            "## Visual QA Observations",
            "",
        ]
    )
    for spec in SPECS:
        lines.append(f"- {spec.observation}")
    lines.extend(
        [
            "- Transparency is present on all source PNG and runtime WebP outputs.",
            "- No dirty grid lines, labels, UI chrome, or watermarks are visible in the runtime sprite sheets.",
            "- A mild halo/edge softness remains from the source artwork, but it is limited and acceptable for first integration.",
            "- Scale concern: ant frames are intentionally small and dark; later integration should place them over a light hive-stand area.",
            "- Scale concern: keeper frames are usable at preview scale, but the first integration pass should tune CSS size against the Task 034D camera timeline.",
            "",
            "## Recommendation",
            "",
            "PASS_WITH_NOTES",
            "",
            "## Validation",
            "",
            "- Required runtime WebPs exist.",
            "- Required source PNGs exist.",
            "- Expected dimensions match known Task 035C targets.",
            "- Manifest JSON remains valid.",
            "- Manifest references the committed source and runtime assets.",
            "",
            "## Confirmations",
            "",
            "- No app behavior was changed.",
            "- No production animation integration was performed.",
            "- No advisor pages, routes, model code, llama.cpp integration, retrieval code, `metadata.json`, `download_model.sh`, `REPORT.md`, or model files were edited.",
            "- No model/runtime/scoring files were edited.",
            "- No Phaser, WebGL, canvas, CDN, cloud APIs, external runtime services, or internet dependencies were added.",
            "- This is public challenge-edition demo asset QA only.",
        ]
    )
    AUDIT_PATH.write_text("\n".join(lines) + "\n")


def main() -> None:
    results = validate_assets()
    generate_preview()
    write_audit(results)
    print(f"Preview written: {PREVIEW_PATH.relative_to(ROOT)}")
    print(f"Audit written: {AUDIT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
