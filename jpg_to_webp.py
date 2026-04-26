#!/usr/bin/env python3
"""
folder_to_webp.py
Convert all JPG/JPEG images in a folder to WebP format.
Usage:
    python folder_to_webp.py <input_folder> [output_folder] [quality]
Examples:
    python folder_to_webp.py ./photos
    python folder_to_webp.py ./photos ./webp_output
    python folder_to_webp.py ./photos ./webp_output 90
Arguments:
    input_folder:  Folder containing JPG/JPEG images.
    output_folder: Folder to save .webp files (optional).
                   Defaults to a 'webp' subfolder inside input_folder.
    quality:       Compression quality 1–100 (optional, default: 85).
"""

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("❌  Pillow is not installed. Run:  pip install Pillow")
    sys.exit(1)


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg"}


def convert_image(image_file: Path, output_file: Path, quality: int) -> tuple[float, float]:
    """Convert a single JPG/JPEG file to WebP. Returns (original_kb, new_kb)."""
    with Image.open(image_file) as img:
        exif_data = img.info.get("exif", b"")
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        save_kwargs = {"quality": quality, "method": 6}
        if exif_data:
            save_kwargs["exif"] = exif_data

        img.save(output_file, "WEBP", **save_kwargs)

    original_kb = image_file.stat().st_size / 1024
    new_kb = output_file.stat().st_size / 1024
    return original_kb, new_kb


def convert_folder(input_folder: str, output_folder: str = None, quality: int = 85) -> None:
    """
    Convert all JPG/JPEG images in a folder to WebP.

    Args:
        input_folder:  Path to the folder with JPG/JPEG images.
        output_folder: Path to save WebP files (optional).
        quality:       WebP quality 1–100 (default 85).
    """
    input_dir = Path(input_folder)

    if not input_dir.exists():
        raise FileNotFoundError(f"Input folder not found: {input_folder}")
    if not input_dir.is_dir():
        raise ValueError(f"Not a folder: {input_folder}")
    if not (1 <= quality <= 100):
        raise ValueError(f"Quality must be between 1 and 100, got: {quality}")

    # --- Resolve output folder ---
    if output_folder is None:
        output_dir = input_dir / "webp"
    else:
        output_dir = Path(output_folder)
    output_dir.mkdir(parents=True, exist_ok=True)

    # --- Find all JPG/JPEG files (non-recursive) ---
    image_files = sorted(
        f for f in input_dir.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not image_files:
        print(f"⚠️   No JPG/JPEG images found in: {input_dir}")
        return

    print(f"📂  Input  : {input_dir.resolve()}")
    print(f"📂  Output : {output_dir.resolve()}")
    print(f"🎚️   Quality: {quality}")
    print(f"🔍  Found  : {len(image_files)} image(s)\n")
    print(f"{'File':<35} {'Original':>10} {'WebP':>10} {'Saving':>10}")
    print("─" * 70)

    total_original = 0.0
    total_new = 0.0
    success = 0
    failed = 0

    for image_file in image_files:
        output_file = output_dir / (image_file.stem + ".webp")
        try:
            original_kb, new_kb = convert_image(image_file, output_file, quality)
            saving = (1 - new_kb / original_kb) * 100 if original_kb > 0 else 0
            total_original += original_kb
            total_new += new_kb
            success += 1

            name = image_file.name
            if len(name) > 33:
                name = name[:30] + "..."
            print(f"  ✅ {name:<33} {original_kb:>8.1f} KB {new_kb:>8.1f} KB {saving:>+8.1f}%")

        except Exception as e:
            failed += 1
            print(f"  ❌ {image_file.name:<33} ERROR: {e}")

    # --- Summary ---
    print("─" * 70)
    total_saving = (1 - total_new / total_original) * 100 if total_original > 0 else 0
    print(f"\n{'Summary':}")
    print(f"  Converted : {success} file(s)" + (f"  |  Failed: {failed}" if failed else ""))
    print(f"  Original  : {total_original:.1f} KB  ({total_original / 1024:.2f} MB)")
    print(f"  WebP total: {total_new:.1f} KB  ({total_new / 1024:.2f} MB)")
    print(f"  Saved     : {total_original - total_new:.1f} KB  ({total_saving:.1f}% smaller)")
    print(f"\n  Output folder: {output_dir.resolve()}")


def main():
    input_folder = '/Users/Grace/photos/'
    output_folder = '/Users/Grace/photos/webp/'
    quality = int(sys.argv[3]) if len(sys.argv) > 3 else 85

    try:
        convert_folder(input_folder, output_folder, quality)
    except (FileNotFoundError, ValueError) as e:
        print(f"❌  Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()