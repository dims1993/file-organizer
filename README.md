# File Organizer CLI (Python)

A simple command-line tool written in Python to organize files in a folder by **extension** or **modification date**.  
It supports **dry-run simulation**, generates **execution statistics**, and logs all actions to a file.

The tool automatically creates folders, safely moves files, handles duplicate filenames, and ignores hidden system files.

---

## Features

- Organize files by extension (e.g. `.pdf`, `.txt`, `.jpg`)
- Organize files by modification date (Year / Month)
- Dry-run mode (simulates actions without moving files)
- Logging to a file (`organizer.log`)
- Error handling (permissions, missing files, name collisions)
- Execution statistics summary
- Professional CLI using `argparse`

---

## Project Structure

```
file-organizer/
│
├── src/
│ ├── organizer.py # CLI entry point
│ └── strategies.py # Organization logic
│
├── organizer.log # Execution log
├── README.md
└── .gitignore
```

---

# Usage

## 1 Organization by extension (default mode)

From the project root, run:

```bash
python src/organizer.py /path/to/your/folder
```

Example:

```bash
python src/organizer.py ~/Downloads
```

## 2 Organization by date

```bash
python3 src/organizer.py /ruta/a/la/carpeta --mode date
```

## 3 Simulation mode (dry-run)

Simulates the organization without moving any files:

```bash
python src/organizer.py /path/to/your/folder --dry-run
```

## Execution Statistics

At the end of each run, the tool provides a terminal summary:

```Plaintext
Total files analyzed
Files moved
Files ignored
Files renamed due to name collisions
```

Example:

```bash
Resumen:
- total: 42
- moved: 35
- ignored: 5
- renamed: 2
```

---

## Logging

This project uses Python’s built-in logging module.

- Log file: organizer.log

- Includes:

Format: YYYY-MM-DD HH:MM:SS - LEVEL - Message

It records:

Program start and parameters used.

Source and destination of every file moved.

Warnings (collisions) and Errors (permissions).

---

## Technologies Used

- Python 3.x

- argparse: Professional CLI argument parsing.

- pathlib: Object-oriented filesystem paths.

- logging: Industrial-grade event tracking.

- Git & GitHub: Version control.

## Skills Demonstrated

This project showcases my proficiency in:

Filesystem Operations: Working with paths, directories, and file metadata.

CLI Design: Creating intuitive tools for technical users.

Defensive Programming: Anticipating errors and protecting user data.

Clean Code: Separation of concerns (logic vs. interface) and maintainable structure.

## Security Recommendation

Always use the --dry-run flag before executing the script on important directories to verify the expected outcome.

## Project Status

Finished

This project is considered stable and closed.
No new features are planned at this time.

## Author

David Muñoz Salinas Aspiring Junior Python Developer

## License

Free for educational and personal use.
