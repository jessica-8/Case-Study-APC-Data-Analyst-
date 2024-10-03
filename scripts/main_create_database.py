import sqlite3
import pandas as pd
import glob
from process_standings import read_data
from process_transfers import read_transfers, create_player_table, create_dimension_tables
from process_stats import read_team_stats

#Define paths to the raw data files
path_standings = 'data/raw/*standings*'
path_transfers = 'data/raw/transfers-bundesliga.csv'
path_performance = 'data/raw/bundesliga-player-stats-general-19-24.xlsx'
path_squad_map = 'data/processed/squads_map_performance.csv'
path_team_stats = 'data/raw/bundesliga-team-performance-stats-19-24.xlsx'
path_player_stats = 'data/raw/bundesliga-player-performance-stats-23-24.xlsx'
sql_schema_path = 'scripts/schema.sql'  # Path to the SQL schema file


# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('data/bundesliga3.db')
cursor = conn.cursor()

# Read and execute SQL schema from file
with open(sql_schema_path, 'r') as file:
    sql_script = file.read()

cursor.executescript(sql_script)

#Read, process and insert the transfers data.
transfers_df = read_transfers(path_transfers)
transfers_df.to_sql('transfers', conn, if_exists='replace', index=False)

#Create dimension tables season, club and competition.
season_df, club_df, competition_df = create_dimension_tables(path_transfers)
season_df.to_sql('season', conn, if_exists='replace', index=False)
club_df.to_sql('club', conn, if_exists='replace', index=False)
competition_df.to_sql('competition', conn, if_exists='replace', index=False)

#Read, process and insert the standings data.
standings_df = read_data(glob.glob(path_standings), club_df, season_df, competition_df)  
standings_df.to_sql('standings', conn, if_exists='replace', index=False)

#Read, process and insert the player data (derived from the transfers data).
player_df = create_player_table(path_transfers)
player_df.to_sql('player', conn, if_exists='replace', index=False)

#Performance data

team_performance_df = read_team_stats(path_team_stats, path_squad_map, standings_df)
team_performance_df.to_sql('teamStats', conn, if_exists='replace', index=False)

player_performance_stats = read_team_stats(path_player_stats, path_squad_map, standings_df)
player_performance_stats.to_sql('playerStats', conn, if_exists='replace', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()
