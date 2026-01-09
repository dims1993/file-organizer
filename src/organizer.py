import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description="Organizador de archivos por extensión")
    parser.add_argument("path", help="Ruta de la carpeta que quieres organizar")
    parser.add_argument("--dry-run", action="store_true", help="Simula la organización sin mover archivos")

    args = parser.parse_args()
    folder = Path(args.path)
    dry_run = args.dry_run

    if not folder.exists() or not folder.is_dir():
        print(f"La ruta {folder.resolve()} no es una carpeta válida.")
        sys.exit(1)

    print(f"Organizando archivos en: {folder.resolve()}")
    if dry_run:
        print("Modo Dry Run activado: no se moverán archivos.")

    files_by_extension = read_folder_contents(folder)

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


def read_folder_contents(folder: Path):
    files_by_extension = {}
    for item in folder.iterdir():
        if item.is_file():
            key = item.suffix.lower() if item.suffix else "no_extension"
            files_by_extension.setdefault(key, []).append(item)
    return files_by_extension


if __name__ == "__main__":
    main()
