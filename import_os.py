import  os
import logging
import requests
import zipfile
import pandas as pd

urls={
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip" #This url is wrong because the year 2220 does not exist
}

download_dir = r"C:\Users\jorge\OneDrive\Escritorio\3 Curso AI-IF\alu.161050\Ejercicio 1"


for url in urls:
    fname = url.split("/")[-1]
    fpath = os.path.join(download_dir, fname)

    print(f"Descargando {fname}...")

    # Descargar el ZIP
    r = requests.get(url)
    with open(fpath, "wb") as f:
        f.write(r.content)

    # Extraer CSV en la carpeta y borrar el ZIP
    with zipfile.ZipFile(fpath, "r") as zip_ref:
        zip_ref.extractall(download_dir)

    os.remove(fpath)

print(f"Archivos descargados y extraídos en: {download_dir}")