from pathlib import Path

from PIL import Image

FRAME_DIR = Path("assets/demo-frames")
OUTPUT = Path("assets/demo/safe-agent-demo.gif")
TARGET_WIDTH = 640
DURATIONS_MS = [900, 1150, 1150, 1400, 1400]

frame_paths = sorted(FRAME_DIR.glob("frame-*.png"))
if len(frame_paths) != 5:
    raise SystemExit(f"expected 5 demo frames, found {len(frame_paths)}")

frames: list[Image.Image] = []
for frame_path in frame_paths:
    with Image.open(frame_path) as source:
        image = source.convert("RGB")
        height = round(image.height * TARGET_WIDTH / image.width)
        image = image.resize((TARGET_WIDTH, height), Image.Resampling.LANCZOS)
        frames.append(
            image.convert(
                "P",
                palette=Image.Palette.ADAPTIVE,
                colors=64,
            )
        )

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=DURATIONS_MS,
    loop=0,
    optimize=True,
    disposal=2,
)

if OUTPUT.stat().st_size == 0:
    raise SystemExit("generated GIF is empty")

print(f"DEMO_GIF={OUTPUT} bytes={OUTPUT.stat().st_size}")
