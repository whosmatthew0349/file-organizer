from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path


CATEGORIES: dict[str, set[str]] = {
	"Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".heic"},
	"Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"},
	"Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
	"Documents": {
		".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx",
		".ppt", ".pptx", ".csv",
	},
	"Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
	"Code": {".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".ts", ".json", ".xml"},
	"Executables": {".exe", ".msi", ".dmg", ".app", ".bat", ".sh"},
}

HIDDEN_ATTRIBUTE = 0x2
SYSTEM_ATTRIBUTE = 0x4


def category_for(path: Path) -> str:
	"""Return the matching category, or Others for an unknown extension."""
	extension = path.suffix.lower()
	for category, extensions in CATEGORIES.items():
		if extension in extensions:
			return category
	return "Others"


def should_skip(path: Path, *, skip_hidden: bool, skip_system: bool) -> bool:
	if skip_hidden and path.name.startswith("."):
		return True
	try:
		attributes = getattr(path.stat(), "st_file_attributes", 0)
	except OSError as exc:
		print(f"Skipping {path.name}: cannot inspect file ({exc})", file=sys.stderr)
		return True
	return (skip_hidden and bool(attributes & HIDDEN_ATTRIBUTE)) or (
		skip_system and bool(attributes & SYSTEM_ATTRIBUTE)
	)


def choose_destination(folder: Path, filename: str, reserved: set[Path]) -> Path:
	"""Return a destination that does not conflict with an existing or planned file."""
	source_name = Path(filename)
	candidate = folder / filename
	number = 1
	while candidate.exists() or candidate in reserved:
		candidate = folder / f"{source_name.stem}_{number}{source_name.suffix}"
		number += 1
	reserved.add(candidate)
	return candidate


def organize(
	folder: Path, *, dry_run: bool, skip_hidden: bool, skip_system: bool
) -> int:
	if not folder.exists():
		print(f"Error: folder does not exist: {folder}", file=sys.stderr)
		return 1
	if not folder.is_dir():
		print(f"Error: path is not a folder: {folder}", file=sys.stderr)
		return 1

	try:
		entries = list(folder.iterdir())
	except OSError as exc:
		print(f"Error: cannot read folder {folder}: {exc}", file=sys.stderr)
		return 1

	counts: Counter[str] = Counter()
	reserved: set[Path] = set()
	failures = 0
	for source in entries:
		try:
			if not source.is_file() or should_skip(
				source, skip_hidden=skip_hidden, skip_system=skip_system
			):
				continue

			category = category_for(source)
			destination_folder = folder / category
			destination = choose_destination(destination_folder, source.name, reserved)
			if dry_run:
				print(f"[DRY RUN] {source.name} -> {category}/{destination.name}")
			else:
				# Create category directories only when a file needs to go there.
				destination_folder.mkdir(exist_ok=True)
				source.rename(destination)
				print(f"Moved {source.name} -> {category}/{destination.name}")
			counts[category] += 1
		except OSError as exc:
			failures += 1
			print(f"Could not organize {source.name}: {exc}", file=sys.stderr)

	action = "planned" if dry_run else "moved"
	print(f"\nSummary ({action}):")
	if counts:
		for category in sorted(counts):
			print(f"  {category}: {counts[category]}")
	else:
		print("  No files to organize.")
	if failures:
		print(f"  Failed: {failures}")
	return 1 if failures else 0


def main() -> int:
	default_folder = Path.home() / "Downloads"
	parser = argparse.ArgumentParser(description="Sort files into folders by file type.")
	parser.add_argument(
		"folder", nargs="?", type=Path, default=default_folder,
		help=f"folder to organize (default: {default_folder})",
	)
	parser.add_argument("--dry-run", action="store_true", help="show planned moves without moving files")
	parser.add_argument("--skip-hidden", action="store_true", help="skip hidden files")
	parser.add_argument("--skip-system", action="store_true", help="skip system files")
	args = parser.parse_args()
	return organize(
		args.folder.expanduser(), dry_run=args.dry_run,
		skip_hidden=args.skip_hidden, skip_system=args.skip_system,
	)


if __name__ == "__main__":
	raise SystemExit(main())
