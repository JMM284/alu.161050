import kagglehub
import shutil
import os
"""
Important:

Due to recent updates in the kagglehub library, automatic downloading may fail 
if you don’t have a valid Kaggle API key (kaggle.json) or if the library version 
behaves differently. 

For reproducibility, the repository includes the Raw_data folder with the required CSV files.
"""

def run_extract():
    print("Starting data download from Kaggle")
    # Download the dataset files to a temporary folder
    path_download = kagglehub.dataset_download("evangower/valorant-esports-top-earnings")
    
    folder_raw_data = "Raw_data"
    
    # Create the folder if it does not exist 
    if not os.path.exists(folder_raw_data):
        os.makedirs(folder_raw_data)
    
    # Move all files to the Raw_data folder
    for file_name in os.listdir(path_download):
        source = os.path.join(path_download, file_name)
        destination = os.path.join(folder_raw_data, file_name)
        
        # We copy only the files to keep the directory clean
        if os.path.isfile(source):
            shutil.copy2(source, destination)
        
    print(" Files copied to Raw_data.")

if __name__ == "__main__":
    run_extract()