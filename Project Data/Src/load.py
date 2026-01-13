import os

def run_load(dim_players_table, dim_teams_table, fact_players_table, fact_teams_table):
    # Target folder for processed data
    output_folder = 'Processed_data'
    
    # Create the folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Save tables as CSV files
    dim_players_table.to_csv(os.path.join(output_folder, 'dim_players.csv'), index=False)
    dim_teams_table.to_csv(os.path.join(output_folder, 'dim_teams.csv'), index=False)
    fact_players_table.to_csv(os.path.join(output_folder, 'fact_players.csv'), index=False)
    fact_teams_table.to_csv(os.path.join(output_folder, 'fact_teams.csv'), index=False)
    
    print("Data successfully saved in Processed_data folder.")

if __name__ == "__main__":
    print("Waiting to load data...")
