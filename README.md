# M_File_Helper
====================================================
THIS HAS NOT BEEN TESTED! MAY HAVE BUGS!
====================================================
This Python script organizes files in a folder by moving them into subfolders based on their file type.By default it works on your Downloads folder.HOW IT WORKSIt looks at every file in the chosen folder.
It checks the file extension (for example .jpg, .pdf, .mp3).
It decides which category the file belongs to:Images (.jpg, .png, .gif, etc.)
Videos (.mp4, .mkv, .mov, etc.)
Audio (.mp3, .wav, .flac, etc.)
Documents (.pdf, .docx, .txt, etc.)
Archives (.zip, .rar, .7z, etc.)
Code (.py, .js, .html, etc.)
Executables (.exe, .bat, .sh, etc.)
Anything else goes into "Others"

It creates a subfolder for that category (if it does not already exist).
It moves the file into that subfolder.
If a file with the same name already exists, it adds a number (photo_1.jpg, photo_2.jpg, etc.) so nothing gets overwritten.

OPTIONS--dry-run
Shows what the script would do without actually moving any files.--skip-hidden
Ignores hidden files (files that start with a dot or have the hidden attribute on Windows).--skip-system
Ignores system files on Windows.HOW TO USEpython script_name.py
→ Organizes your Downloads folderpython script_name.py /path/to/folder
→ Organizes a different folderpython script_name.py --dry-run
→ Preview the moves without changing anythingpython script_name.py --skip-hidden --skip-system
→ Skip hidden and system filesEXAMPLEBefore:
Downloads/
  photo.jpg
  report.pdf
  song.mp3
  photo.jpgAfter:
Downloads/
  Images/
    photo.jpg
    photo_1.jpg
  Documents/
    report.pdf
  Audio/
    song.mp3
    
  # The script only moves files. It does not touch folders or files it cannot read.

