import argparse
from pathlib import Path
import sys

# Creamos el parseador y definimos los argumentos
def main():
    # 1. Creamos el "parceador" como objeto
    parser = argparse.ArgumentParser(description="Organizador de archivos por extensión")

    # 2. Definimos qué argumento queremos recibir (el camino a la carpeta)
    parser.add_argument("path", help="Ruta de  la carpeta que quieres organizar")

    # 3. Leemos los argumentos
    args = parser.parse_args()

    #Convertimos el string recibido a un objeto Path
    folder = Path(args.path)

    #5. Verificamos si la ruta es válida y si es una carpeta
    if folder.exists() and folder.is_dir():
        print(f"Organizando archivos en: {folder.resolve()}")
        
        # Leemos el contenido de la carpeta
        files_by_extension = read_folder_contents(folder)
        
        # Mostramos el resultado
        for ext, files in files_by_extension.items():
            # Mostrar la extensión y la cantidad de archivos
            print(f"Extension: {ext}, Files: {len(files)}")
            
            # Creamos la carpeta para la extensión si no existe
            ruta = folder / ext
            ruta.mkdir(exist_ok=True)

            # Movemos los archivos a la carpeta correspondiente
            for archivo in files:
                if not archivo.name.startswith('.'):  # Ignorar archivos ocultos
                    print(f"Procesando archivo: {archivo.name}")
                    destino = ruta / archivo.name
                    if not destino.exists():
                        archivo.rename(destino)
                        print(f"Movido: {archivo.name} -> {destino}")
                
                    # Si el archivo ya existe en el destino, no lo movemos, lo renombramos
                    else:
                        counter = 1
                        new_name = f"{archivo.stem} ({counter}){archivo.suffix}"
                        new_destino = ruta / new_name
                        while new_destino.exists():
                            counter += 1
                            new_name = f"{archivo.stem} ({counter}){archivo.suffix}"
                            new_destino = ruta / new_name
                        archivo.rename(new_destino)
                        print(f"Renombrado y movido: {archivo.name} -> {new_destino}")
                else:
                    print(f"Ignorado archivo oculto: {archivo.name}")
    else:
        print(f"La ruta {folder.resolve()} no es una carpeta válida.")
        sys.exit(1)

def read_folder_contents(folder: Path):
    files_by_extension = {}
    for item in folder.iterdir():
        if item.is_file():
            key = item.suffix.lower() if item.suffix.lower() else 'no_extension'
            files_by_extension.setdefault(key, []).append(item)
    return files_by_extension
            

if __name__ == "__main__":
    main()
