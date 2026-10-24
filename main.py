from __future__ import annotations

import argparse
import os
import sys
from collections import Counter
from pathlib import Path


class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"
    WHITE = "\033[37m"


def enable_windows_ansi() -> None:
    if sys.platform != "win32":
        return
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        kernel32.SetConsoleMode(handle, mode.value | 0x0004)
    except Exception:
        pass


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
        print(f"{C.YELLOW}Skipping {path.name}: cannot inspect file ({exc}){C.RESET}", file=sys.stderr)
        return True
    return (skip_hidden and bool(attributes & HIDDEN_ATTRIBUTE)) or (
        skip_system and bool(attributes & SYSTEM_ATTRIBUTE)
    )


def choose_destination(folder: Path, filename: str, reserved: set[Path]) -> Path:
    source_name = Path(filename)
    candidate = folder / filename
    number = 1
    while candidate.exists() or candidate in reserved:
        candidate = folder / f"{source_name.stem}_{number}{source_name.suffix}"
        number += 1
    reserved.add(candidate)
    return candidate


def print_banner() -> None:
    print(f"""
{C.CYAN}{C.BOLD}╔══════════════════════════════════════════╗
║          FILE ORGANIZER  v1.2            ║
║     Sort your chaos into neat folders    ║
║    Created by @whos.matthew on Discord!  ║
╚══════════════════════════════════════════╝{C.RESET}
""")


def organize(
    folder: Path, *, dry_run: bool = False, skip_hidden: bool = False, skip_system: bool = False
) -> int:
    if not folder.exists():
        print(f"{C.RED}Error: folder does not exist: {folder}{C.RESET}", file=sys.stderr)
        return 1
    if not folder.is_dir():
        print(f"{C.RED}Error: path is not a folder: {folder}{C.RESET}", file=sys.stderr)
        return 1

    try:
        entries = list(folder.iterdir())
    except OSError as exc:
        print(f"{C.RED}Error: cannot read folder {folder}: {exc}{C.RESET}", file=sys.stderr)
        return 1

    mode = f"{C.YELLOW}DRY RUN{C.RESET}" if dry_run else f"{C.GREEN}LIVE{C.RESET}"
    print(f"\n  Target : {C.BOLD}{folder}{C.RESET}")
    print(f"  Mode   : {mode}\n")

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
                print(f"  {C.DIM}[DRY]{C.RESET}  {source.name}  →  {C.CYAN}{category}/{destination.name}{C.RESET}")
            else:
                destination_folder.mkdir(exist_ok=True)
                source.rename(destination)
                print(f"  {C.GREEN}✓{C.RESET}  {source.name}  →  {C.CYAN}{category}/{destination.name}{C.RESET}")
            counts[category] += 1
        except OSError as exc:
            failures += 1
            print(f"  {C.RED}✗{C.RESET}  Could not organize {source.name}: {exc}", file=sys.stderr)

    action = "planned" if dry_run else "moved"
    print(f"\n{C.BOLD}Summary ({action}):{C.RESET}")
    if counts:
        for category in sorted(counts):
            print(f"  {C.MAGENTA}{category:<14}{C.RESET} {counts[category]}")
        total = sum(counts.values())
        print(f"  {C.DIM}{'─' * 20}{C.RESET}")
        print(f"  {C.BOLD}Total{C.RESET}          {total}")
    else:
        print(f"  {C.DIM}No files to organize.{C.RESET}")
    if failures:
        print(f"  {C.RED}Failed: {failures}{C.RESET}")
    return 1 if failures else 0


def show_help() -> None:
    print(f"""
{C.BOLD}How it works{C.RESET}
  Files in the chosen folder are moved into subfolders by type:
  Images, Videos, Audio, Documents, Archives, Code, Executables, Others.

{C.BOLD}Menu options{C.RESET}
  {C.CYAN}1  Start{C.RESET}              Organize the current folder (asks first)
  {C.CYAN}2  What to organize{C.RESET}   Choose or change the target folder
  {C.CYAN}3  Help{C.RESET}               Show this help
  {C.CYAN}4  Exit{C.RESET}               Quit

{C.BOLD}Tips{C.RESET}
  • You can also drag a folder onto the script.
  • From a terminal you can still use:
      python organize.py "C:\\Users\\You\\Downloads"
      python organize.py . --dry-run
""")


def ask_folder(current: Path) -> Path:
    print(f"\n  Current folder: {C.BOLD}{current}{C.RESET}")
    print(f"  {C.DIM}Press Enter to keep it, or type a new path:{C.RESET}")
    raw = input(f"  {C.CYAN}> {C.RESET}").strip().strip('"')
    if not raw:
        return current
    path = Path(raw).expanduser()
    try:
        path = path.resolve()
    except OSError:
        pass
    if not path.exists() or not path.is_dir():
        print(f"  {C.RED}That path isn't a valid folder. Keeping the previous one.{C.RESET}")
        return current
    print(f"  {C.GREEN}Folder set to:{C.RESET} {path}")
    return path


def confirm(prompt: str) -> bool:
    answer = input(f"  {prompt} {C.DIM}[y/N]{C.RESET} ").strip().lower()
    return answer in ("y", "yes")


def interactive_menu() -> int:
    folder = (Path.home() / "Downloads").resolve()
    dry_run = False

    while True:
        print(f"""
{C.BOLD}  What do you want to do?{C.RESET}

  {C.GREEN}[1]{C.RESET}  Start              Organize files
  {C.CYAN}[2]{C.RESET}  What to organize   Choose folder  {C.DIM}(now: {folder}){C.RESET}
  {C.YELLOW}[3]{C.RESET}  Help
  {C.RED}[4]{C.RESET}  Exit
""")
        choice = input(f"  {C.CYAN}Command > {C.RESET}").strip().lower()

        if choice in ("1", "start", "s"):
            print(f"\n  Folder : {C.BOLD}{folder}{C.RESET}")
            mode_label = "preview only (dry-run)" if dry_run else "move files for real"
            print(f"  Mode   : {mode_label}")
            if not confirm("Proceed?"):
                print(f"  {C.DIM}Cancelled.{C.RESET}")
                continue
            # Quick dry-run option right before starting
            if not dry_run and confirm("Want a dry-run preview first?"):
                organize(folder, dry_run=True)
                if not confirm("Looks good — organize for real now?"):
                    print(f"  {C.DIM}Cancelled.{C.RESET}")
                    continue
            organize(folder, dry_run=False)
            input(f"\n  {C.DIM}Press Enter to return to menu...{C.RESET}")

        elif choice in ("2", "what", "w", "folder", "organize"):
            folder = ask_folder(folder)

        elif choice in ("3", "help", "h", "?"):
            show_help()
            input(f"\n  {C.DIM}Press Enter to return to menu...{C.RESET}")

        elif choice in ("4", "exit", "quit", "q"):
            print(f"\n  {C.DIM}Bye!{C.RESET}\n")
            return 0

        else:
            print(f"  {C.YELLOW}Unknown command. Type 1, 2, 3, or 4 (or Start / Help / Exit).{C.RESET}")


def main() -> int:
    enable_windows_ansi()
    print_banner()

    default_folder = Path.home() / "Downloads"
    parser = argparse.ArgumentParser(
        description="Sort files into folders by file type.",
        add_help=True,
    )
    parser.add_argument(
        "folder",
        nargs="?",
        type=Path,
        default=None,
        help=f"folder to organize (example: {default_folder})",
    )
    parser.add_argument("--dry-run", action="store_true", help="show planned moves without moving files")
    parser.add_argument("--skip-hidden", action="store_true", help="skip hidden files")
    parser.add_argument("--skip-system", action="store_true", help="skip system files")
    parser.add_argument("--menu", action="store_true", help="force interactive menu")

    args = parser.parse_args()

    if args.folder is None or args.menu:
        return interactive_menu()

    return organize(
        args.folder.expanduser().resolve(),
        dry_run=args.dry_run,
        skip_hidden=args.skip_hidden,
        skip_system=args.skip_system,
    )


if __name__ == "__main__":
    raise SystemExit(main())
