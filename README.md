# File Organizer CLI (Python)

A simple command-line tool written in Python to organize files in a folder by their extensions.

It automatically creates folders, moves files safely, handles duplicate filenames, and ignores hidden system files.

---

## Features

- Organizes files by extension (e.g. `.pdf`, `.txt`, `.jpg`)
- Automatically creates folders for each extension
- Safely handles duplicate filenames by renaming them
- Ignores hidden system files (e.g. `.DS_Store`)
- Works from the command line using arguments
- Uses modern Python tools (`pathlib`, `argparse`)

---

## Usage

From the project root, run:

```bash
python src/organizer.py /path/to/your/folder

Example:

python src/organizer.py ~/Downloads
```

## Technologies Used

- Python 3
- argparse
- pathlib
- Git & GitHub

## What I Learned

1. Working with the file system in Python

2. Writing command-line interfaces (CLI)

3. Using dictionaries to organize data

4. Handling edge cases safely (duplicate files, hidden files)

5. Structuring a real, usable Python script

6. Using Git properly (commits and .gitignore)

## Notes

This project is part of my learning journey as a Python developer and will continue to evolve with new features and improvements.
