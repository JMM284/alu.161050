import pandas as pd
import numpy as np

# Predefined real data for certain players
players_dict = {
    'zombs': ['2020-04-28', '2022-04-29'],
    'ShahZaM': ['2020-04-28', '2022-12-11'],
    'dapr': ['2020-06-01', '2023-01-01'],
    'SicK': ['2020-04-28', '2023-05-10'],
    'cNed': ['2021-03-01', '2022-11-01'],
    'starxo': ['2021-03-01', '2023-01-01'],
    'nAts': ['2021-01-18', '2022-09-21'],
    'Chronicle': ['2021-01-18', '2022-11-01'],
    'TenZ': ['2021-06-01', '2024-01-01'],
    'ScreaM': ['2020-08-07', '2022-11-10'],
    'mixwell': ['2020-06-16', '2022-10-15']
}

def calc_dates(row):
    player = row['Player']
    
    # 1. Use real data if the player is in the dictionary
    if player in players_dict:
        return players_dict[player][0], players_dict[player][1]
    
    # 2. If the player is not in the dictionary, generate a random date between 2020 and 2022
    year = np.random.choice([2020, 2021, 2022])
    
    month = np.random.randint(1, 13)
    day = np.random.randint(1, 28)
    
    start_date = f"{year}-{month:02d}-{day:02d}"
    
    # 3.Calculate leave date by adding between 400 and 800 days to join date
    end_date_dt = pd.to_datetime(start_date) + pd.to_timedelta(np.random.randint(400, 800), unit='D')
    
    return start_date, end_date_dt.strftime('%Y-%m-%d')

def run_validation():
    players = pd.read_csv('Raw_data/Players.csv')
    teams = pd.read_csv('Raw_data/Teams.csv')

    print(players.isnull().sum())
    
    # Create a backup of the 'Earnings' column
    backup_earnings = players['Earnings'].copy()
    
    # Introduce some NaN values for testing in the 'Earnings' column
    players.loc[10:20, 'Earnings'] = np.nan
    print(players.isnull().sum())
    
    # Fill NaN values with backup before final fill
    players['Earnings'] = players['Earnings'].fillna(backup_earnings)
    print(players.isnull().sum())
    
    players['Earnings_Float'] = players['Earnings'].replace(r'[\$,]', '', regex=True).astype(float)
    teams['Earnings_Float'] = teams['Earnings'].replace(r'[\$,]', '', regex=True).astype(float)

    players[['Join_Date', 'Leave_Date']] = players.apply(lambda x: pd.Series(calc_dates(x)), axis=1)
    players['Total_Medals'] = players['Gold'] + players['Silver'] + players['Bronze']

    return players, teams

if __name__ == "__main__":
    run_validation()