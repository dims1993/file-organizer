import argparse
from pathlib import Path
import sys
from datetime import datetime


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

    
def organize_by_extension(files_by_extension, folder, dry_run):
    for ext, files in files_by_extension.items():
        target_folder = folder / ext.lstrip('.')
        print(f"\nExtensión {ext} → carpeta {target_folder.name}/")
        for archivo in files:
            if archivo.name.startswith('.'):
                print(f"Ignorado archivo oculto: {archivo.name}")
                continue
            destino = target_folder / archivo.name

            if destino.exists():
                counter = 1
                while True:
                    new_destino = target_folder / f"{archivo.stem}_{counter}{archivo.suffix}"
                    if not new_destino.exists():
                        destino = new_destino
                        break
                    counter += 1

            if dry_run:
                print(f"[DRY RUN] {archivo.name} → {destino}")
            else:
                target_folder.mkdir(exist_ok=True)
                archivo.rename(destino)
                print(f"Movido: {archivo.name} → {destino}")


def organize_by_date(files_by_date, folder, dry_run):
    for archivo in files_by_date:
        if archivo.name.startswith('.'):
            print(f"Ignorado archivo oculto: {archivo.name}")
            continue
        timestamp = archivo.stat().st_mtime
        date = datetime.fromtimestamp(timestamp)

        year = str(date.year)
        month = f"{date.month:02d}"

        target_folder = folder / year / month
        destino = target_folder / archivo.name

        if destino.exists():
            counter = 1
            while True:
                new_destino = target_folder / f"{archivo.stem}_{counter}{archivo.suffix}"
                if not new_destino.exists():
                    destino = new_destino
                    break
                counter += 1

        if dry_run:
            print(f"[DRY RUN] {archivo.name} → {destino}")
        else:
            target_folder.mkdir(parents=True, exist_ok=True)
            archivo.rename(destino)
            print(f"Movido: {archivo.name} → {destino}")


def read_folder_contents(folder: Path):
    files_by_extension = {}
    for item in folder.iterdir():
        if item.is_file():
            key = item.suffix.lower() if item.suffix else "no_extension"
            files_by_extension.setdefault(key, []).append(item)
    return files_by_extension


if __name__ == "__main__":
    main()
