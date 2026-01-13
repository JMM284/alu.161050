import pandas as pd

def run_transform(players, teams):
    
    # 1. Dimension Tables
    dim_players = players[['Player', 'Join_Date', 'Leave_Date']].drop_duplicates()
    dim_teams = teams[['Team']].drop_duplicates()

    # 2. Fact Tables 
    fact_players = players[
        ['Player', 'Rank', 'Gold', 'Silver', 'Bronze', 'S Tier', 'Earnings_Float', 'Total_Medals']
    ]

    fact_teams = teams[
        ['Team', 'Rank', 'Gold', 'Silver', 'Bronze', 'S Tier', 'Earnings_Float']
    ]

    return dim_players, dim_teams, fact_players, fact_teams