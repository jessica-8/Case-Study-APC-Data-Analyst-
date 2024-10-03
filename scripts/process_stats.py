import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


def add_rank(df, df_standings):
    print(df_standings.columns)
    df_stats = pd.merge(df, df_standings[['League_Position', 'club_id', 'season','season_id']], how='left', left_on=['club_id', 'season'], right_on=['club_id', 'season'])
    return df_stats

def read_team_stats(filename, path_squad_map, df_standings):
    xls = pd.ExcelFile(filename)
    sheet_names = xls.sheet_names

    df_stats = []

    for sheet in sheet_names:
        print(sheet)  
        df = pd.read_excel(filename, sheet_name=sheet)
        df['season'] = sheet  
        df['season'] = df['season'].str.replace('_', '/') 
        df_stats.append(df)  

    df_stats = pd.concat(df_stats, ignore_index=True)

    #remove duplicate columns
    df_stats = df_stats.loc[:, ~df_stats.columns.duplicated()]
    #merge squad map to assign squad id's
    squad_map = pd.read_csv(path_squad_map)
    df_stats = pd.merge(df_stats, squad_map, how='left', left_on='Squad', right_on='Squad')
    df_stats = add_rank(df_stats, df_standings)

    return df_stats


