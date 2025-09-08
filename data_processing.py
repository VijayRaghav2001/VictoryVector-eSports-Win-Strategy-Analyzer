import pandas as pd
import numpy as np
import json
import os

class DataProcessor:
    def __init__(self):
        self.base_paths = {
            'raw': '../data/raw/',
            'processed': '../data/processed/'
        }
    
    def load_json_data(self, filename):
        """Load JSON data from file"""
        path = os.path.join(self.base_paths['raw'], filename)
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    
    def process_lol_match_data(self, match_data):
        """Process League of Legends match data"""
        processed_matches = []
        
        for match in match_data:
            try:
                # Extract basic match information
                match_info = {
                    'match_id': match['metadata']['matchId'],
                    'game_duration': match['info']['gameDuration'],
                    'game_version': match['info']['gameVersion'],
                    'queue_id': match['info']['queueId']
                }
                
                # Extract team information
                for team in match['info']['teams']:
                    team_info = match_info.copy()
                    team_info['team_id'] = team['teamId']
                    team_info['win'] = 1 if team['win'] else 0
                    team_info['first_blood'] = team['objectives']['champion']['first']
                    team_info['first_tower'] = team['objectives']['tower']['first']
                    team_info['total_towers'] = team['objectives']['tower']['kills']
                    team_info['total_dragons'] = team['objectives']['dragon']['kills']
                    team_info['total_barons'] = team['objectives']['baron']['kills']
                    
                    processed_matches.append(team_info)
            
            except KeyError as e:
                print(f"Error processing match: {e}")
                continue
        
        return pd.DataFrame(processed_matches)
    
    def process_dota_match_data(self, match_data):
        """Process Dota 2 match data"""
        processed_matches = []
        
        for match in match_data:
            try:
                match_info = {
                    'match_id': match['match_id'],
                    'game_duration': match['duration'],
                    'radiant_win': match['radiant_win'],
                    'leagueid': match['leagueid'],
                    'series_id': match['series_id'],
                    'radiant_score': match['radiant_score'],
                    'dire_score': match['dire_score']
                }
                
                # Add player statistics
                for player in match['players']:
                    player_info = match_info.copy()
                    player_info['player_slot'] = player['player_slot']
                    player_info['hero_id'] = player['hero_id']
                    player_info['kills'] = player['kills']
                    player_info['deaths'] = player['deaths']
                    player_info['assists'] = player['assists']
                    player_info['gold_per_min'] = player['gold_per_min']
                    player_info['xp_per_min'] = player['xp_per_min']
                    
                    processed_matches.append(player_info)
            
            except KeyError as e:
                print(f"Error processing match: {e}")
                continue
        
        return pd.DataFrame(processed_matches)
    
    def clean_data(self, df):
        """Perform data cleaning operations"""
        # Handle missing values
        df = df.dropna()
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Remove outliers (example: games shorter than 5 minutes)
        if 'game_duration' in df.columns:
            df = df[df['game_duration'] > 300]  # 5 minutes in seconds
        
        return df
    
    def save_processed_data(self, df, filename):
        """Save processed data to CSV"""
        os.makedirs(self.base_paths['processed'], exist_ok=True)
        path = os.path.join(self.base_paths['processed'], filename)
        df.to_csv(path, index=False)
        print(f"Processed data saved to {path}")

if __name__ == "__main__":
    processor = DataProcessor()
    # Example usage:
    # lol_data = processor.load_json_data('lol_matches.json')
    # processed_lol = processor.process_lol_match_data(lol_data)
    # cleaned_lol = processor.clean_data(processed_lol)
    # processor.save_processed_data(cleaned_lol, 'lol_matches_processed.csv')
