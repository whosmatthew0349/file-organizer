# File Organizer

Sort your chaos into neat folders.

A lightweight Python script that organizes files in a folder by type — Images, Videos, Audio, Documents, Archives, Code, Executables, and Others.

![Version](https://img.shields.io/badge/version-1.2-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Features

- **Automatic sorting** by file extension into category folders
- **Interactive menu** — beginner-friendly, no terminal knowledge required
- **CLI mode** — scriptable and automation-friendly
- **Dry-run mode** — preview moves before committing
- **Conflict handling** — renames duplicates (`file_1.jpg`, `file_2.jpg`, …)
- **Skip options** — ignore hidden and/or system files
- **Colored terminal output** with Windows ANSI support
- **Zero dependencies** — pure Python standard library

---

## Categories

| Category       | Extensions                                      |
|----------------|-------------------------------------------------|
| **Images**     | `.jpg` `.jpeg` `.png` `.gif` `.webp` `.bmp` `.svg` `.heic` |
| **Videos**     | `.mp4` `.mkv` `.avi` `.mov` `.wmv` `.flv`       |
| **Audio**      | `.mp3` `.wav` `.flac` `.aac` `.ogg` `.m4a`      |
| **Documents**  | `.pdf` `.doc` `.docx` `.txt` `.rtf` `.odt` `.xls` `.xlsx` `.ppt` `.pptx` `.csv` |
| **Archives**   | `.zip` `.rar` `.7z` `.tar` `.gz`                |
| **Code**       | `.py` `.js` `.html` `.css` `.java` `.cpp` `.c` `.ts` `.json` `.xml` |
| **Executables**| `.exe` `.msi` `.dmg` `.app` `.bat` `.sh`        |
| **Others**     | Everything else                                 |

---

## Requirements

- Python 3.8+
- No external packages needed

---

## Installation

```bash
git clone https://github.com/whosmatthew0349/file-organizer.git
cd file-organizer
