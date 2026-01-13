import logging
import argparse
from pathlib import Path
import sys
from strategies import organize_by_extension, organize_by_date

logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def init_stats():
    return {
        "total": 0,
        "moved": 0,
        "ignored": 0,
        "renamed": 0
    }


def main():
    stats = init_stats()

    parser = argparse.ArgumentParser(description="Organizador de archivos por extensión o fecha")

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
        logger.error(f"La ruta {folder.resolve()} no es una carpeta válida.")
        sys.exit(1)

    logger.info("Programa iniciado")
    logger.info(f"Carpeta objetivo: {folder}")
    logger.info(f"Modo: {mode}")
    logger.info(f"Dry run: {dry_run}")

    if dry_run:
        logger.info("Modo Dry Run activado: no se moverán archivos.")

    files_by_extension = read_folder_contents(folder)

    if mode == "date":
        all_files = []
        for files in files_by_extension.values():
            all_files.extend(files)

        organize_by_date(all_files, folder, dry_run, stats)
        
    else:
        organize_by_extension(files_by_extension, folder, dry_run, stats)

    logger.info("Resumen de ejecución:")
    logger.info(f"Archivos analizados: {stats['total']}")
    logger.info(f"Archivos movidos: {stats['moved']}")
    logger.info(f"Archivos ignorados: {stats['ignored']}")
    logger.info(f"Renombrados por colisión: {stats['renamed']}")

    print("\nResumen:")
    for key, value in stats.items():
        print(f"- {key}: {value}")


def read_folder_contents(folder: Path):
    files_by_extension = {}

    try:
         items = folder.iterdir()
    except PermissionError as e:
        logger.error(f"No se pueden leer los contenidos de la carpeta {folder}: {e}")
        return files_by_extension
    except Exception as e:
        logger.error(f"Error leyendo la carpeta {folder}: {e}")
        return files_by_extension
    for item in items:
        try:
             if item.is_file():
                 key = item.suffix.lower() if item.suffix else "no_extension"
                 files_by_extension.setdefault(key, []).append(item)
        except PermissionError as e:
             logger.warning(f"No se puede acceder al archivo {item}: {e}")
        except Exception as e:
            logger.error(f"Error procesando el archivo {item}: {e}")

    return files_by_extension


if __name__ == "__main__":
    main()
