
import pandas as pd
import numpy as np
import glob


def tidy_club_names(df, col):
        club_name_map = {
            '1 FC Köln': '1. FC Köln', '1.FC Köln': '1. FC Köln', '1. FC Union Berlin': '1. FC Union Berlin',
            '1 FC Union Berlin': '1. FC Union Berlin', 'Union Berlin': '1. FC Union Berlin', 
            '1.FC Nuremberg': '1. FC Nürnberg', '1.FSV Mainz 05': '1. FSV Mainz 05', 
            "1.FC K'lautern": "1. FC Kaiserslautern", 'New York': 'New York Red Bulls', 
            'New York City': 'New York City FC', 'Bohemians': 'Bohemians 1905', 'Brann': 'SK Brann', 
            'Dinamo Moscow': 'Dynamo Moscow', 'Inter': 'Inter Milan', "Bor. M'gladbach": "Borussia Mönchengladbach", 
            "Bor. Dortmund": "Borussia Dortmund", "E. Frankfurt": "Eintracht Frankfurt", 
            "B. Leverkusen": "Bayer 04 Leverkusen", "1899 Hoffenheim": "TSG 1899 Hoffenheim", 
            "TSG Hoffenheim": "TSG 1899 Hoffenheim", "1.FSV Mainz 05": "1. FSV Mainz 05", 
            "Mainz 05": "1. FSV Mainz 05", "F. Düsseldorf": "Fortuna Düsseldorf", 
            "SC Paderborn": "SC Paderborn 07", "Arm. Bielefeld": "Arminia Bielefeld", 
            "Hertha BSC": "Hertha Berlin", "Heidenheim": "1. FC Heidenheim", "1 FC Heidenheim": "1. FC Heidenheim"
        }
        df[col] = df[col].replace(club_name_map)
        return df

def read_data(files, df_club, df_season, df_competition):

    # rename columns
    def rename_cols(df):
        col_names = ['Rank', 'Club', 'P_Home', 'W_Home', 'D_Home','L_Home','P_Away',
                    'W_Away','D_Away','L_Away','P_Total','W_Total','D_Total','L_Total',
                    'Goals_For','Goals_Against','Goals_Diff','Points']
        df.columns = col_names  #
        df = df.drop(0) 
        return df

    # extract the season and league from the filename
    def extract_season(filename):
        season = '_'.join(filename.split('-')[2:]).split('.')[0]
        league = filename.split('-')[1]
        return season, league
    
    #assign league position
    def assign_league_position(df):
        df['League_Position'] = df['Rank']
        df['League_Position'] = df['League_Position'].replace('C', 1)

        def replace_ranks(group):
            r_indices = group[group['League_Position'] == 'R'].index
            if len(r_indices) > 0:
                group.loc[r_indices[0], 'League_Position'] = 17
            if len(r_indices) > 1:
                group.loc[r_indices[1], 'League_Position'] = 18
            return group

        # for each season, replace the 'R' clubs with 17 and 18 ranks.
        df = df.groupby('Season').apply(replace_ranks)
        return df

    #set data types for columns
    def set_data_type(df):
        df = df.astype({
            'Rank': 'str', 'Club': 'str', 'P_Home': 'int', 'W_Home': 'int', 'D_Home': 'int',
            'L_Home': 'int', 'P_Away': 'int', 'W_Away': 'int', 'D_Away': 'int', 'L_Away': 'int',
            'P_Total': 'int', 'W_Total': 'int', 'D_Total': 'int', 'L_Total': 'int', 
            'Goals_For': 'int', 'Goals_Against': 'int', 'Goals_Diff': 'int', 'Points': 'int', 
            'League_Position': 'int'
        })
        return df

    # Main function logic
    dfs = []
    for file in files:
        try:
            df = pd.read_csv(file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file, encoding='latin1')

        df = rename_cols(df) 
        season, league = extract_season(file)  
        df['Season'] = season
        df['League'] = league
        df.loc[:, 'Season'] = df['Season'].str.replace('_', '/')
        df['competition_id'] = 'L1'

        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    df = tidy_club_names(df, 'Club')  
    df = assign_league_position(df)  
    df = set_data_type(df)  
    df.drop_duplicates(inplace=True) 

    df = pd.merge(df, df_club, left_on='Club', right_on='club_name', how='left')
    df = pd.merge(df, df_season, left_on='Season', right_on='season', how='left')
    # df = pd.merge(df, df_competition, left_on='League', right_on='competition_name', how='left')
    
    print("Standings df 1")
    print(df)
    df = df.drop(columns=['club_name', 'Season'])
    df = df.loc[:, ~df.columns.duplicated(keep='first')]
   
    return df

