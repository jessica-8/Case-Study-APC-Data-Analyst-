import pandas as pd
import numpy as np
import glob
from process_standings import tidy_club_names



def read_transfers(file):
    df = pd.read_csv(file)
    df = tidy_club_names(df,'from.club_name')
    df = tidy_club_names(df,'to.club_name')
    df = df.rename(columns={'from.club_id': 'from_club_id',
                            'to.club_id': 'to_club_id', 
                            'from.club_name': 'from_club_name',
                            'to.club_name': 'to_club_name',
                            'from.competition_id': 'from_competition_id',
                            'from.competition_name': 'from_competition_name',
                            'to.competition_id': 'to_competition_id',
                            'to.competition_name': 'to_competition_name',
                            'transfer_datetime': 'transfer_date'})

    return df

#Player table is derived from the transfers table as input
def create_player_table(file):
    df = read_transfers(file)
    df_player = df[['player_id', 'player_name', 'date_of_birth_datetime', 'citizenship', 'position.main', 'position.other', 'height_cm', 'foot']]
    #print(df_player.shape)

    #identify duplicate rows in df_player
    duplicate_rows = df_player[df_player.duplicated()]
    df_player = df_player.drop_duplicates()
    #print(duplicate_rows.shape)
    return df_player

    
#takes df_transfers as input
def create_dimension_tables(file): 
    df = read_transfers(file)
    print("Columns in df_transfers")
    print(df.columns)
    df_season = df[['season_id', 'season']]
    df_season = df_season.drop_duplicates()
    df_season.reset_index(drop=True, inplace=True)

    df_competition_from = df[['from_competition_id', 'from_competition_name']]
    df_competition_from.columns = ['competition_id', 'competition_name']

    df_competition_to = df[['to_competition_id', 'to_competition_name']]
    df_competition_to.columns = ['competition_id', 'competition_name']

    df_competition = pd.concat([df_competition_from, df_competition_to], ignore_index=True)
    df_competition = df_competition.drop_duplicates()
    df_competition.reset_index(drop=True, inplace=True)
    # print(df_competition)

    df_club_from = df[['from_club_id', 'from_club_name']]
    df_club_from.columns = ['club_id', 'club_name']

    df_club_to = df[['to_club_id', 'to_club_name']]
    df_club_to.columns = ['club_id', 'club_name']

    df_club = pd.concat([df_club_from, df_club_to], ignore_index=True)
    df_club = df_club.drop_duplicates()
    df_club.reset_index(drop=True, inplace=True)
    # print(df_club)

    return df_season, df_club, df_competition

