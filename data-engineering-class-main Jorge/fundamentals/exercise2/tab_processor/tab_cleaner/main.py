# Importamos las bibliotecas necesarias
import os
import re
import logging as log
import datetime
from utils.string_mapping import MAPPING  

# -- Configuration ---
# Usamos os.path.normpath para normalizar los separadores de ruta 
INPUT_DIRECTORY = os.path.normpath("./files/")
CATALOG_DIRECTORY = os.path.join(INPUT_DIRECTORY, "catalogs")
LOGS_DIRECTORY = os.path.normpath("./logs/")

OUTPUT_DIRECTORY = os.path.join(INPUT_DIRECTORY, "cleaned")
ROOT = "https://acordes.lacuerda.net"
URL_ARTIST_INDEX = "https://acordes.lacuerda.net/tabs/"
MIN_LINES = 5
SONG_VERSION = 0
INDEX = "abcdefghijklmnopqrstuvwxyz#"

dir_list = list()

# --- Logging config---
logger = log.getLogger(__name__)

# Asegurarse de que el directorio de logs exista
if not os.path.exists(LOGS_DIRECTORY):
    os.makedirs(LOGS_DIRECTORY, exist_ok=True)

log.basicConfig(
    filename=os.path.join(LOGS_DIRECTORY, "cleaner.log"),
    filemode="w",
    encoding="utf-8",
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=log.INFO,
)

# --- Logic---


def list_files_recursive(path="."):
    """
    Rellena recursivamente la lista global `dir_list` con rutas de archivos.
    """
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            list_files_recursive(full_path)
        else:
            dir_list.append(full_path)

    return dir_list


def remove_email_sentences(text: str):
    """
    Elimina frases que contienen direcciones de email.
    """
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    # Patrón mejorado para capturar frases que pueden no terminar con puntuación estándar
    sentence_pattern = r"[^\n.!?]*" + email_pattern + r"[^\n.!?]*"
    
    # Reemplaza líneas enteras si contienen un email
    lines = text.split('\n')
    cleaned_lines = [line for line in lines if not re.search(email_pattern, line)]
    return '\n'.join(cleaned_lines)


def apply_format_rules(text: str):
    """
    Aplica varias reglas de formato y limpieza al texto.
    """
    # Empezar con el texto original
    formatted_text = text

    formatted_text = remove_email_sentences(formatted_text)
    
    
    if MAPPING:
        for key, value in MAPPING.items():
            formatted_text = re.sub(
                key, value, formatted_text, flags=re.DOTALL | re.IGNORECASE
            )
    else:
        log.warning("El diccionario MAPPING está vacío o no se ha cargado.")
        
    return formatted_text


def main():

    # Start time tracking
    start_time = datetime.datetime.now()
    log.info(f"Cleaner started at {start_time}")
    print("Starting cleaner...")

    cleaned = 0
    
    # Normalizar rutas de E/S para reemplazo correcto
    norm_input_dir = os.path.normpath(INPUT_DIRECTORY)
    norm_output_dir = os.path.normpath(OUTPUT_DIRECTORY)

    # Obtener todas las rutas de archivos recursivamente
    all_files = list_files_recursive(norm_input_dir)
    log.info(f"Found {len(all_files)} files to process.")

    for file_path in all_files:
        # CORRECCIÓN para evitar rutas duplicadas 
        if norm_output_dir in file_path or CATALOG_DIRECTORY in file_path:
            log.info(f"Skipping non-song/already processed file: {file_path}")
            continue

        log.info(f"Processing file -> {file_path}")
        
        # Inicializar como string vacío
        text = ""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
        except Exception as e:
            log.error(f"Could not read file {file_path}: {e}")
            continue
            
        if text.count("\n") < MIN_LINES:
            log.info(f"Empty or too small tab. Skipping: {file_path}")
            continue
            

        formatted_text = apply_format_rules(text)

        # Crear la ruta de salida reemplazando la base de entrada por la de salida
        output_file = file_path.replace(norm_input_dir, norm_output_dir, 1)
        
        # Corregido para que funcione en windows
        file_name = os.path.basename(output_file)
        

        # Creates the path if not exists
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)        
            log.info(f"Directory CREATED!! -> {dir}")
            

        cleaned += 1
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(formatted_text)
            print(f"{cleaned} -- {file_name} CREATED!! in {dir}")
        

    end_time = datetime.datetime.now()
    log.info(f"Cleaner ended at {end_time}")
    duration = end_time - start_time
    log.info(f"Total duration: {duration}")
    log.info(f"Total files cleaned: {cleaned}")
    print(
        f"Cleaner finished. Duration in seconds: {duration.total_seconds()}, that is {duration.total_seconds() / 60} minutes."
    )


if __name__ == "__main__":
    main()