import os
import requests
import zipfile
import pandas as pd 

urls = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
]

download_dir = "downloads"

os.makedirs(download_dir, exist_ok=True)

for url in urls:
    fname = url.split("/")[-1]
    fpath = os.path.join(download_dir, fname)

    print(f"Descargando {fname}...")
    r = requests.get(url)

    if r.status_code != 200:
        print(f"No se pudo descargar {fname} (Error {r.status_code})")
        continue

    with open(fpath, "wb") as f:
        f.write(r.content)

    with zipfile.ZipFile(fpath, "r") as zip_ref:
        zip_ref.extractall(download_dir)

    os.remove(fpath)

print(f"Archivos descargados y extraídos en: {download_dir}")

downloads = download_dir

csv_files = [f for f in os.listdir(downloads) if f.endswith(".csv")]

if not csv_files:
    print("No hay archivos CSV en 'downloads/'")
    exit()

for csv_file in csv_files:
    file_path = os.path.join(downloads, csv_file)
    df = pd.read_csv(file_path)
    
    print(f"\nArchivo: {csv_file}")
    print("Columnas:", df.columns.tolist())
    
    print(df.head())
    print(df.info())
    print(df.describe(include='all'))
    
    print("Valores nulos por columna:")
    print(df.isnull().sum())
    
