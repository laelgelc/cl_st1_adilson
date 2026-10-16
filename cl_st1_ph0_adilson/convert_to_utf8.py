#!/usr/bin/env python3
"""
Recursively convert text files from one character encoding to another.

By default, this programme reads files encoded as Windows-1252 and writes them
as UTF-8. It walks through every file in the source directory, preserves the
relative directory structure, and writes the converted files into the target
directory.

The source and target directories must be different. Existing files in the
target directory may be overwritten if they have the same relative path as a
converted source file.

Usage:
    python convert_to_utf8.py SOURCE_DIR TARGET_DIR

Example:
    python convert_to_utf8.py input_files converted_files

This reads all files under the directory named "input_files" as Windows-1252
and writes UTF-8 versions of them under the directory named "converted_files".

Optional arguments:
    --source-encoding ENCODING
        Encoding used to read the source files.
        Default: windows-1252

    --target-encoding ENCODING
        Encoding used to write the target files.
        Default: utf-8

Example with explicit encodings:
    python convert_to_utf8.py input_files converted_files \
        --source-encoding windows-1252 \
        --target-encoding utf-8

Files that cannot be decoded using the source encoding are skipped and reported
on the command line.
"""

import argparse
from pathlib import Path


def convert_file(source_path: Path, target_path: Path, source_encoding: str, target_encoding: str) -> None:
    text = source_path.read_text(encoding=source_encoding)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(text, encoding=target_encoding)


def convert_directory(source_dir: Path, target_dir: Path, source_encoding: str, target_encoding: str) -> None:
    for source_path in source_dir.rglob("*"):
        if not source_path.is_file():
            continue

        relative_path = source_path.relative_to(source_dir)
        target_path = target_dir / relative_path

        try:
            convert_file(source_path, target_path, source_encoding, target_encoding)
            print(f"Converted: {source_path} -> {target_path}")
        except UnicodeDecodeError as error:
            print(f"Skipped, could not decode as {source_encoding}: {source_path} ({error})")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recursively convert text files from Windows-1252 to UTF-8."
    )

    parser.add_argument(
        "source_dir",
        type=Path,
        help="Directory containing the Windows-1252 files.",
    )

    parser.add_argument(
        "target_dir",
        type=Path,
        help="Directory where UTF-8 files will be written.",
    )

    parser.add_argument(
        "--source-encoding",
        default="windows-1252",
        help="Source file encoding. Default: windows-1252.",
    )

    parser.add_argument(
        "--target-encoding",
        default="utf-8",
        help="Target file encoding. Default: utf-8.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    source_dir = args.source_dir
    target_dir = args.target_dir

    if not source_dir.exists():
        raise SystemExit(f"Source directory does not exist: {source_dir}")

    if not source_dir.is_dir():
        raise SystemExit(f"Source path is not a directory: {source_dir}")

    if source_dir.resolve() == target_dir.resolve():
        raise SystemExit("Source and target directories must be different.")

    convert_directory(
        source_dir=source_dir,
        target_dir=target_dir,
        source_encoding=args.source_encoding,
        target_encoding=args.target_encoding,
    )


if __name__ == "__main__":
    main()