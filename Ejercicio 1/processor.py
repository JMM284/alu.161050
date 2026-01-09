import os
import pandas as pd

downloads = "downloads"

processed_dir = "processed"
if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)
# List of CSV files
csv_files = [f for f in os.listdir(downloads) if f.endswith(".csv")]

resultados = []

for csv_file in csv_files:
    file_path = os.path.join(downloads, csv_file)
    df = pd.read_csv(file_path)

    try:
        # Primero pruebo con la columna 'tripduration'
        if 'tripduration' in df.columns:
            df['tripduration'] = df['tripduration'].astype(str).str.replace(',', '').astype(float)
            mean_duration = df['tripduration'].mean()
            
        # despues pruebo con la columna larga porque hay un csv que la tiene y no tiene trip duration
        elif '01 - Rental Details Duration In Seconds Uncapped' in df.columns:
            col_larga = '01 - Rental Details Duration In Seconds Uncapped'
            df[col_larga] = df[col_larga].astype(str).str.replace(',', '').astype(float)
            mean_duration = df[col_larga].mean()
            
    except Exception as e:
        print(f"Error procesando {csv_file}: {e}")

    resultados.append([csv_file, mean_duration])
df_result = pd.DataFrame(resultados, columns=['archivo', 'duracion_media_segundos'])

# Save the result in the folder processed 
output_path = os.path.join(processed_dir, "mean_tripulation.csv")
df_result.to_csv(output_path, index=False)

print(f"Summary file saved at: {output_path}")
