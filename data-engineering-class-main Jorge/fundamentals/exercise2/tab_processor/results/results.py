import os

# Carpetas a analizar
CLEANED_DIR = "./files/cleaned"
VALIDATION_DIR = "./files/validations"
SONGS_DIR = "./files/songs"

def count_files(directory):
    """Cuenta todos los archivos dentro de 'directory' de manera recursiva."""
    total_files = 0
    for root, dirs, files in os.walk(directory):
        total_files += len(files)
    return total_files

if __name__ == "__main__":
    cleaned_count = count_files(CLEANED_DIR)
    validation_count = count_files(VALIDATION_DIR)
    songs_count = count_files(SONGS_DIR)

    print(f"Total files in '{CLEANED_DIR}': {cleaned_count}")
    print(f"Total files in '{VALIDATION_DIR}': {validation_count}")
    print(f"Total files in '{SONGS_DIR}': {songs_count}")
