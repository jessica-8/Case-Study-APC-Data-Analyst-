import pandas as pd


def count_positions(transfers):
    # Define the position mapping for classification
    position_mapping = {
        'Goalkeeper': 'Goalkeeper',
        'Left-Back': 'Defense',
        'Right-Back': 'Defense',
        'Centre-Back': 'Defense',
        'Defensive Midfield': 'Midfield',
        'Central Midfield': 'Midfield',
        'Attacking Midfield': 'Midfield',
        'Left Midfield': 'Midfield',
        'Right Midfield': 'Midfield',
        'Left Winger': 'Attack',
        'Right Winger': 'Attack',
        'Centre-Forward': 'Attack',
        'Second Striker': 'Attack'
    }

    # Map the positions in the 'transfers' DataFrame using the position_mapping
    # Assuming the column is 'position', not 'position.main'
    transfers['position_category'] = transfers['position.main'].map(position_mapping)

    # Count buy metrics based on position categories
    buy_counts = transfers.groupby(['to_club_id', 'season_id', 'position_category']).size().unstack(fill_value=0).reset_index()
    buy_counts['buy_count_total'] = buy_counts.drop(columns=['to_club_id', 'season_id']).sum(axis=1)
    buy_counts = buy_counts.rename(columns={'to_club_id': 'club_id'})
    # Dynamically rename the buy position columns to include 'buy_count_'
    buy_counts = buy_counts.rename(columns=lambda col: f'buy_count_{col}' if col not in ['club_id', 'season_id'] else col)

    # Count sell metrics based on position categories
    sell_counts = transfers.groupby(['from_club_id', 'season_id', 'position_category']).size().unstack(fill_value=0).reset_index()
    sell_counts['sell_count_total'] = sell_counts.drop(columns=['from_club_id', 'season_id']).sum(axis=1)
    sell_counts = sell_counts.rename(columns={'from_club_id': 'club_id'})
    # Dynamically rename the sell position columns to include 'sell_count_'
    sell_counts = sell_counts.rename(columns=lambda col: f'sell_count_{col}' if col not in ['club_id', 'season_id'] else col)

    return buy_counts, sell_counts


def count_transfer_type(transfers):
    # Count occurrences of each transfer_type for buys ('to_club_id')
    buy_counts = transfers.groupby(['to_club_id', 'season_id', 'transfer_type']).size().unstack(fill_value=0).reset_index()
    buy_counts = buy_counts.rename(columns=lambda x: f'buy_count_{x}' if x != 'to_club_id' and x != 'season_id' else x)
    buy_counts = buy_counts.rename(columns={'to_club_id': 'club_id'})
    
    # Count occurrences of each transfer_type for sells ('from_club_id')
    sell_counts = transfers.groupby(['from_club_id', 'season_id', 'transfer_type']).size().unstack(fill_value=0).reset_index()
    sell_counts = sell_counts.rename(columns=lambda x: f'sell_count_{x}' if x != 'from_club_id' and x != 'season_id' else x)
    sell_counts = sell_counts.rename(columns={'from_club_id': 'club_id'})
    
    return buy_counts, sell_counts

def count_age_groups(transfers):
    # Define age categories
    transfers['age_group'] = transfers['player_age_at_transfer'].apply(lambda age: 'under23' if age <= 21 else 'over23')
    
    # Count buy metrics based on age categories
    buy_counts = transfers.groupby(['to_club_id', 'season_id', 'age_group']).size().unstack(fill_value=0).reset_index()
    buy_counts['buy_count_total'] = buy_counts[['under23', 'over23']].sum(axis=1)
    buy_counts = buy_counts.rename(columns={
        'to_club_id': 'club_id', 
        'under23': 'buy_count_under23', 
        'over23': 'buy_count_over23'
    })

    # Count sell metrics based on age categories
    sell_counts = transfers.groupby(['from_club_id', 'season_id', 'age_group']).size().unstack(fill_value=0).reset_index()
    sell_counts['sell_count_total'] = sell_counts[['under23', 'over23']].sum(axis=1)
    sell_counts = sell_counts.rename(columns={
        'from_club_id': 'club_id', 
        'under23': 'sell_count_under23', 
        'over23': 'sell_count_over23'
    })

    return buy_counts, sell_counts

def count_profile_groups(transfers):
    # Define profile categories
    transfers['profile_group'] = transfers['market_value_million'].apply(lambda value: 'high_profile' if value >= 0.7 else 'low_profile')
    
    # Count buy metrics based on profile categories
    buy_counts = transfers.groupby(['to_club_id', 'season_id', 'profile_group']).size().unstack(fill_value=0).reset_index()
    buy_counts['buy_count_total'] = buy_counts[['high_profile', 'low_profile']].sum(axis=1)
    buy_counts = buy_counts.rename(columns={
        'to_club_id': 'club_id', 
        'high_profile': 'buy_count_high_profile', 
        'low_profile': 'buy_count_low_profile'
    })

    # Count sell metrics based on profile categories
    sell_counts = transfers.groupby(['from_club_id', 'season_id', 'profile_group']).size().unstack(fill_value=0).reset_index()
    sell_counts['sell_count_total'] = sell_counts[['high_profile', 'low_profile']].sum(axis=1)
    sell_counts = sell_counts.rename(columns={
        'from_club_id': 'club_id', 
        'high_profile': 'sell_count_high_profile', 
        'low_profile': 'sell_count_low_profile'
    })

    return buy_counts, sell_counts

def calculate_season_summary(standings, transfers, custom_funcs=[]):
    # Define the columns and club IDs
    cols = ['player_age_at_transfer', 'transfer_fee_euro', 'transfer_fee_million', 'market_value_euro', 'market_value_million']
    
    # Initialize empty DataFrames to store buy and sell summaries
    buy_summary_df = pd.DataFrame()
    sell_summary_df = pd.DataFrame()

    # Loop through 'to_club_id' (for buys) and 'from_club_id' (for sells)
    for col in cols:
        # Calculate buy metrics (using 'to_club_id')
        buy_mean_df = transfers.groupby(['to_club_id', 'season_id'])[col].mean().reset_index().rename(columns={'to_club_id': 'club_id', col: f'buy_mean_{col}'})
        buy_sum_df = transfers.groupby(['to_club_id', 'season_id'])[col].sum().reset_index().rename(columns={'to_club_id': 'club_id', col: f'buy_sum_{col}'})
        
        # Merge buy metrics
        if buy_summary_df.empty:
            buy_summary_df = buy_mean_df
        else:
            buy_summary_df = pd.merge(buy_summary_df, buy_mean_df, on=['club_id', 'season_id'], how='outer')

        buy_summary_df = pd.merge(buy_summary_df, buy_sum_df, on=['club_id', 'season_id'], how='outer')
        
        # Calculate sell metrics (using 'from_club_id')
        sell_mean_df = transfers.groupby(['from_club_id', 'season_id'])[col].mean().reset_index().rename(columns={'from_club_id': 'club_id', col: f'sell_mean_{col}'})
        sell_sum_df = transfers.groupby(['from_club_id', 'season_id'])[col].sum().reset_index().rename(columns={'from_club_id': 'club_id', col: f'sell_sum_{col}'})
        
        # Merge sell metrics
        if sell_summary_df.empty:
            sell_summary_df = sell_mean_df
        else:
            sell_summary_df = pd.merge(sell_summary_df, sell_mean_df, on=['club_id', 'season_id'], how='outer')

        sell_summary_df = pd.merge(sell_summary_df, sell_sum_df, on=['club_id', 'season_id'], how='outer')
    
    # Apply custom functions to generate additional columns
    for func in custom_funcs:
        # Pass the 'transfers' DataFrame and the 'buy_summary_df' and 'sell_summary_df'
        buy_custom, sell_custom = func(transfers)
        
        # Merge custom buy and sell data into summaries
        buy_summary_df = pd.merge(buy_summary_df, buy_custom, on=['club_id', 'season_id'], how='outer')
        sell_summary_df = pd.merge(sell_summary_df, sell_custom, on=['club_id', 'season_id'], how='outer')

    # Merge buy and sell summaries
    summary_df = pd.merge(buy_summary_df, sell_summary_df, on=['club_id', 'season_id'], how='outer')

    return summary_df



