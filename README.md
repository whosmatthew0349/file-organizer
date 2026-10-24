# M_File_Helper

> ⚠️ **Warning:** This has not been tested and may contain bugs.

A simple Python script that organizes files in a folder by moving them into subfolders based on their file type.

By default, it works on your **Downloads** folder.

---

## How It Works

1. Looks at every file in the chosen folder.
2. Checks the file extension (e.g. `.jpg`, `.pdf`, `.mp3`).
3. Places the file into the matching category:

| Category     | Extensions                                      |
|--------------|--------------------------------------------------|
| **Images**   | `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp`, `.svg`, `.heic` |
| **Videos**   | `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`  |
| **Audio**    | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.m4a` |
| **Documents**| `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.csv` |
| **Archives** | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`            |
| **Code**     | `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`, `.c`, `.ts`, `.json`, `.xml` |
| **Executables** | `.exe`, `.msi`, `.dmg`, `.app`, `.bat`, `.sh` |
| **Others**   | Everything else                                  |

4. Creates the category subfolder if it doesn’t already exist.
5. Moves the file into that subfolder.
6. If a file with the same name already exists, it adds a number (`photo_1.jpg`, `photo_2.jpg`, etc.) so nothing gets overwritten.

---

## Options

| Flag              | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `--dry-run`       | Shows what the script would do without actually moving any files            |
| `--skip-hidden`   | Ignores hidden files (names starting with `.` or Windows hidden attribute)  |
| `--skip-system`   | Ignores system files on Windows                                             |

---

## How to Use

```bash
# Organize your Downloads folder
python m_file_helper.py

# Organize a different folder
python m_file_helper.py /path/to/folder

# Preview the moves without changing anything
python m_file_helper.py --dry-run

# Skip hidden and system files
python m_file_helper.py --skip-hidden --skip-system
