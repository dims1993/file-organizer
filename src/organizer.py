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
    else:
        print(f"La ruta {folder.resolve()} no es una carpeta válida.")
        sys.exit(1)

if __name__ == "__main__":
    main()
