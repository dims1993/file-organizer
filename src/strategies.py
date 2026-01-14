from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def organize_by_extension(files_by_extension, folder, dry_run):
    """
    Organiza archivos por extensión.

    :param files_by_extension: dict con extensión -> lista de archivos Path
    :param folder: carpeta raíz donde se organiza
    :param dry_run: si True, no mueve archivos
    :return: dict con estadísticas de ejecución
    """

    stats = {
        "total": 0,
        "moved": 0,
        "ignored": 0,
        "renamed": 0
    }
     
    for ext, files in files_by_extension.items():
    
        target_folder = folder / ext.lstrip('.')
        logger.info(f"Extensión {ext} a carpeta {target_folder.name}/")
        for archivo in files:
            stats["total"] += 1
            if archivo.name.startswith('.'):
                stats["ignored"] += 1
                logger.debug(f"Ignorado archivo oculto: {archivo.name}")
                continue

            destino = target_folder / archivo.name

            renamed = False

            if destino.exists():
                renamed = True
                counter = 1
                while True:
                    new_destino = target_folder / f"{archivo.stem}_{counter}{archivo.suffix}"
                    if not new_destino.exists():
                        destino = new_destino
                        break
                    counter += 1

            try:
                if dry_run:
                    logger.info(f"[DRY RUN] {archivo.name} a {destino}")

                else:
                    target_folder.mkdir(exist_ok=True)
                    archivo.rename(destino)
                    stats["moved"] += 1
                    logger.info(f"Movido: {archivo.name} a {destino}")

                    if renamed:
                        stats["renamed"] += 1

            except Exception as e:
                logger.error(f"Error al mover {archivo.name} a {destino}: {e}")

            
    return stats

def organize_by_date(files_by_date, folder, dry_run):
    """
    Organiza archivos por fecha de modificación (año/mes).

    :param files_by_date: lista de archivos Path
    :param folder: carpeta raíz donde se organiza
    :param dry_run: si True, no mueve archivos
    :return: dict con estadísticas de ejecución
    """

    stats = {
        "total": 0,
        "moved": 0,
        "ignored": 0,
        "renamed": 0
    }

    for archivo in files_by_date:
        stats["total"] += 1
        if archivo.name.startswith('.'):
            stats["ignored"] += 1
            logger.debug(f"Ignorado archivo oculto: {archivo.name}")
            continue

        try:
            timestamp = archivo.stat().st_mtime
        except PermissionError as e:
            logger.warning(f"No se puede leer metadata de {archivo}: {e}")
            stats["ignored"] += 1
            continue
        except FileNotFoundError:
            stats["ignored"] += 1
            logger.warning(f"Archivo no encontrado (posiblemente movido o eliminado): {archivo}")
            continue

        date = datetime.fromtimestamp(timestamp)

        year = str(date.year)
        month = f"{date.month:02d}"

        
        target_folder = folder / year / month
        destino = target_folder / archivo.name
        renamed = False

        if destino.exists():
            renamed = True
            counter = 1
            while True:
                new_destino = target_folder / f"{archivo.stem}_{counter}{archivo.suffix}"
                if not new_destino.exists():
                    destino = new_destino
                    break
                counter += 1
            

        try:
            if dry_run:
                logger.info(f"[DRY RUN] {archivo.name} a {destino}")
            else:
                target_folder.mkdir(parents=True, exist_ok=True)
                archivo.rename(destino)
                stats["moved"] += 1
                logger.info(f"Movido: {archivo.name} a {destino}")
                if renamed:
                    stats["renamed"] += 1
        except Exception as e:
            logger.error(f"Error moviendo {archivo.name}: {e}")

    return stats