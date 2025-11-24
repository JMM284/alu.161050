# Importamos las bibliotecas necesarias
import os
import click
import re
import logging as log
import datetime
import shutil

INPUT_DIRECTORY = "./files/"
CLEANED_DIRECTORY = f"{INPUT_DIRECTORY}cleaned"
OUTPUT_DIRECTORY_OK = f"{INPUT_DIRECTORY}validations/ok"
OUTPUT_DIRECTORY_KO = f"{INPUT_DIRECTORY}validations/ko"
ROOT = "https://acordes.lacuerda.net"
URL_ARTIST_INDEX = "https://acordes.lacuerda.net/tabs/"
SONG_VERSION = 0
INDEX = "abcdefghijklmnopqrstuvwxyz#"


dir_list = list()
output_file = str()
dir_path = str() # modificado
file_name = str()


def validate_song_format(song):
    """Validates if the song follows a basic expected format."""
    # Regex pattern for song format
    pattern = r"((?:[A-Z][#b]?(?:m|maj|min|aug|dim|sus|add)?\d*\s+)*\n.+)+" # modificado

    # Check if the song matches the pattern
    match = re.fullmatch(pattern, song, flags=re.DOTALL)

    # If there is a match, the song is in the correct format
    if match:
        return True
    else:
        return False

#Nueva validacion añadida
def validate_song_additional(song): 
    """Additional validation: at least 5 lines.""" 
    MIN_LINES = 5 
    lines = song.strip().split("\n") 
    return len(lines) >= MIN_LINES 


def list_files_recursive(path: str = "."):
    """Lists all files in a directory recursively."""
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry) # modificado
        if os.path.isdir(full_path):
            list_files_recursive(full_path)
        else:
            dir_list.append(full_path)

    return dir_list


@click.command()
@click.option(
    "--init",
    "-i",
    is_flag=True,
    default=False,
    help=(
        "If flag is present, drops all files and validates from the clean directory. "
    ),
)
def main(init):
    log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s') # modificado
    # Start time tracking
    start_time = datetime.datetime.now()
    log.info(f"Validator started at {start_time}")
    print("Starting validator...")

    if init:
        if os.path.exists(OUTPUT_DIRECTORY_OK):
            shutil.rmtree(OUTPUT_DIRECTORY_OK)
        if os.path.exists(OUTPUT_DIRECTORY_KO):
            shutil.rmtree(OUTPUT_DIRECTORY_KO)
        log.info("Directories Removed")

    OK = 0
    KO = 0

    for file_path in list_files_recursive(CLEANED_DIRECTORY):

        text = str()
        try: # modificado
            with open(file_path, "r", encoding="utf-8") as file: # modificado
                text = file.read()
        except Exception as e: # modificado
            log.error(f"Error reading file {file_path}: {e}") # modificado
            continue # modificado

        # Formatting of the text goes in that function call
        validated = validate_song_format(text) and validate_song_additional(text)  # modificado

        base_output_dir = OUTPUT_DIRECTORY_OK if validated else OUTPUT_DIRECTORY_KO # modificado
        
        if validated:
            OK += 1
        else:
            KO += 1

        try: # modificado
            relative_path = os.path.relpath(file_path, CLEANED_DIRECTORY) # modificado
        except ValueError as e: # modificado
            log.error(f"Could not get relative path for {file_path}: {e}") # modificado
            continue # modificado
            
        output_file = os.path.join(base_output_dir, relative_path) # modificado
        
        dir_path = os.path.dirname(output_file) # modificado
        file_name = os.path.basename(output_file) # modificado

        # Creates the path if not exists
        if not os.path.exists(dir_path): # modificado
            os.makedirs(dir_path, exist_ok=True) # modificado
            print("OKs = ", OK, "-- KOs = ", KO, "--", dir_path, " CREATED!!") # modificado

        try: # modificado
            with open(output_file, "w", encoding="utf-8") as file: # modificado
                file.write(text)
                print("OKs = ", OK, "-- KOs = ", KO, "--", file_name, " CREATED!!")
        except Exception as e: # modificado
            log.error(f"Error writing file {output_file}: {e}") # modificado

    log.info(f"OKs = {OK}, -- KOs = {KO}, --")
    end_time = datetime.datetime.now()
    log.info(f"Validator ended at {end_time}")
    duration = end_time - start_time
    log.info(f"Total duration: {duration}")
    print(
        f"Validator finished. Duration in seconds: {duration.total_seconds()}, that is {duration.total_seconds() / 60} minutes."
    )


if __name__ == "__main__":
    main()

# def validate_song_additional(song):
#     """Additional validation: at least 5 lines."""
#     MIN_LINES = 5
#     lines = song.strip().split("\n")
#     return len(lines) >= MIN_LINES