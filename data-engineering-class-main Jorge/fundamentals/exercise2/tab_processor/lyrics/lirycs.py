import os
import re
import logging as log
import datetime

# --- Configuración de Rutas ---
INPUT_DIRECTORY = os.path.normpath("./files/")
# Directorio de LECTURA: Archivos crudos (songs/)
SONGS_INPUT_DIRECTORY = os.path.join(INPUT_DIRECTORY, "songs")
# Directorio de ESCRITURA: Resultados separados (lyrics/)
LYRICS_OUTPUT_DIRECTORY = os.path.join(INPUT_DIRECTORY, "lyrics") 
LOGS_DIRECTORY = os.path.normpath("./logs/")

# --- Configuración de Logs ---
if not os.path.exists(LOGS_DIRECTORY):
    os.makedirs(LOGS_DIRECTORY, exist_ok=True)
log.basicConfig(
    filename=os.path.join(LOGS_DIRECTORY, "lyrics.log"),
    filemode="w",
    encoding="utf-8",
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=log.INFO,
)
logger = log.getLogger(__name__)

# --- Lógica de Remoción y Separación ---

def is_chord_line(line: str) -> bool:
    """
    Identifica si una línea es un acorde, tablatura o línea vacía/de separación.
    """
    line = line.strip()
    if not line:
        return True
    
    # Patrón común de tablatura o línea separadora
    if re.search(r'^[-=|#]*$', line):
        return True
    
    # Contar letras minúsculas (indicador de letra de canción)
    lowercase_count = len(re.findall(r'[a-záéíóúüñ]', line))
    
    if lowercase_count < 4 and len(line) > 1:
        # Si la proporción de mayúsculas (acordes) es alta
        uppercase_count = len(re.findall(r'[A-Z]', line))
        if uppercase_count > lowercase_count:
             return True

    return False

def extract_lyrics_and_chords(tab_content: str) -> tuple[str, str]:
    """
    Procesa el contenido y devuelve la letra (lyrics) y los acordes (chords) en dos partes.
    """
    lines = tab_content.split('\n')
    lyrics_lines = []
    chords_lines = [] 
    
    for line in lines:
        if is_chord_line(line):
            chords_lines.append(line)
        else:
            lyrics_lines.append(line)
            
    # Limpieza final de la letra: unir líneas y eliminar saltos dobles al inicio/final
    final_lyrics = '\n'.join(lyrics_lines)
    final_lyrics = re.sub(r'\n{2,}', '\n\n', final_lyrics).strip()

    # Limpieza final de los acordes: unir líneas y eliminar espacios
    final_chords = '\n'.join(chords_lines)
    final_chords = final_chords.strip()
    
    return final_lyrics, final_chords

def process_songs(input_path: str, output_path: str):
    """
    Busca archivos en 'songs/', extrae la letra y los acordes, y los guarda en 'lyrics/'.
    """
    start_time = datetime.datetime.now()
    log.info(f"Lyrics extractor started at {start_time}. Reading from {input_path}")
    print(f"Starting lyrics extraction. Output directory: {output_path}")
    
    songs_count = 0
    
    # 1. Crear el directorio de salida (files/lyrics) si no existe
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
        log.info(f"Output Directory CREATED: {output_path}")

    # Recorre recursivamente los archivos en el directorio de entrada (songs/)
    for root, _, files in os.walk(input_path):
        for file_name in files:
            # Solo procesar archivos que terminan en .txt
            if not file_name.endswith(".txt") or file_name.startswith("."):
                continue
                
            file_path = os.path.join(root, file_name)
            
            try:
                # Lectura del archivo crudo de songs/
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 1. Extraer letra y acordes
                lyrics, chords = extract_lyrics_and_chords(content)
                
                # --- Construcción de la nueva ruta de salida en 'files/lyrics' ---
                
                # Determinar el subdirectorio relativo (e.g., 'a' o 'abel_pintos')
                relative_dir = os.path.relpath(root, input_path)
                output_dir = os.path.join(output_path, relative_dir)
                
                # Crear el subdirectorio si no existe
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                
                # Nombre base del archivo (e.g., 'cancion' de 'cancion.txt')
                base_name, _ = os.path.splitext(file_name) 

                # 2. Guardar el archivo de solo Letra (e.g., cancion.lyrics)
                lyrics_file_path = os.path.join(output_dir, base_name + ".lyrics")
                with open(lyrics_file_path, "w", encoding="utf-8") as out_f:
                    out_f.write(lyrics)
                
                # 3. Guardar el archivo de solo Acordes (e.g., cancion.chords)
                chords_file_path = os.path.join(output_dir, base_name + ".chords")
                with open(chords_file_path, "w", encoding="utf-8") as out_f:
                    out_f.write(chords)
                
                # --- Fin Lógica de Guardado ---
                
                songs_count += 1
                print(f"Processed: {os.path.join(relative_dir, base_name)}. Wrote .lyrics and .chords.")
                
            except Exception as e:
                log.error(f"Could not process or save files for {file_path}: {e}")

    end_time = datetime.datetime.now()
    log.info(f"Lyrics extractor ended at {end_time}")
    print(f"\nFinished. Total songs processed: {songs_count}")


if __name__ == "__main__":
    process_songs(SONGS_INPUT_DIRECTORY, LYRICS_OUTPUT_DIRECTORY)