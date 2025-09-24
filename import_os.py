import os
import requests
import zipfile
import pandas as pd 

# urls = [
#     "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
#     "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
#     "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
#     "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
#     "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
#     "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
#     #"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip"  # URL incorrecta
# ]

# download_dir = r"C:\Users\jorge\OneDrive\Escritorio\3 Curso AI-IF\alu.161050\Ejercicio 1"


# for url in urls:
#     fname = url.split("/")[-1]  # Obtiene el nombre del archivo separando la url por / y toma la ultima parte (el nombre del archivo)

#     fpath = os.path.join(download_dir, fname) # Crea la ruta completa donde se guardará el archivo descargado y ira al destino con el nombre (fname).


#     print(f"Descargando {fname}...") # Muestra un mensaje indicando qué archivo se está descargando.

#     # Descargar el ZIP
#     r = requests.get(url)

#     if r.status_code != 200:
#         print(f"No se pudo descargar {fname} (Error {r.status_code})")
#         continue
#     # Verifica si la descarga fue exitosa (código HTTP 200).
#     # Si hubo un error, imprime un mensaje de error y pasa a la siguiente URL.

#     with open(fpath, "wb") as f:
#         f.write(r.content)
#     # Abre un archivo en modo escritura binaria ('wb') y guarda el contenido descargado.

#     # Extraer CSV en la carpeta y borrar el ZIP
#     with zipfile.ZipFile(fpath, "r") as zip_ref:
#         zip_ref.extractall(download_dir)
#     # Abre el archivo ZIP descargado y guarda todo el la direccion especificada (download_dir).

#     os.remove(fpath)
#     # Borra el archivo ZIP 


# print(f"Archivos descargados y extraídos en: {download_dir}")
# # Muestra un mensaje indicando que todos los archivos han sido descargados y extraídos.


downloads = r"C:\Users\jorge\OneDrive\Escritorio\3 Curso AI-IF\alu.161050\Ejercicio 1"

csv_files = [f for f in os.listdir(downloads) if f.endswith(".csv")]
if not csv_files:
    print("No hay archivos CSV en 'downloads/'")
    exit()
    
for csv_file in csv_files:
    file_path = os.path.join(downloads, csv_file)
    print(f"\nMostrando las primeras filas de: {csv_file}")
    df = pd.read_csv(file_path)
    print(df.head())
    print(df.isnull().sum())