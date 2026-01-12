import logging
import argparse
from pathlib import Path
import sys
from datetime import datetime
from src.strategies import organize_by_extension, organize_by_date

logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():

    parser = argparse.ArgumentParser(description="Organizador de archivos por extensión")

    parser.add_argument("path", 
                        help="Ruta de la carpeta que quieres organizar")
    
    parser.add_argument("--dry-run", 
                        action="store_true", 
                        help="Simula la organización sin mover archivos")
    
    parser.add_argument("--mode", 
                        choices=["extension", "date"], 
                        default="extension", 
                        help="Criterio de organización"
)


    args = parser.parse_args()
    folder = Path(args.path)
    dry_run = args.dry_run
    mode = args.mode

    if not folder.exists() or not folder.is_dir():
        print(f"La ruta {folder.resolve()} no es una carpeta válida.")
        sys.exit(1)

    print(f"Organizando archivos en: {folder.resolve()}")
    logging.info(f"Inicio de organización en {folder.resolve()} | modo={mode} | dry_run={dry_run}")

    
    if dry_run:
        print("Modo Dry Run activado: no se moverán archivos.")

    files_by_extension = read_folder_contents(folder)

    if mode == "date":
        all_files = []
        for files in files_by_extension.values():
            all_files.extend(files)

        organize_by_date(all_files, folder, dry_run)
        
    else:
        organize_by_extension(files_by_extension, folder, dry_run)


def read_folder_contents(folder: Path):
    files_by_extension = {}
    for item in folder.iterdir():
        if item.is_file():
            key = item.suffix.lower() if item.suffix else "no_extension"
            files_by_extension.setdefault(key, []).append(item)
    return files_by_extension


if __name__ == "__main__":
    main()
