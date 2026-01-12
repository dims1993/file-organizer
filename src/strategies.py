from datetime import datetime
import logging

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
            logging.info(f"Movido: {archivo} -> {destino}")