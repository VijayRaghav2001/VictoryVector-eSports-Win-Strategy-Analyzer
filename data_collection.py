import requests
import pandas as pd
import json
import time
import os
import random
from dotenv import load_dotenv

load_dotenv()

class DataCollector:
    def __init__(self):
        self.api_keys = {
            'riot': os.getenv('RIOT_API_KEY'),
            'steam': os.getenv('STEAM_API_KEY')
        }
        self.base_paths = {
            'raw': '../data/raw/',
            'processed': '../data/processed/'
        }

        # Ensure directories exist
        for path in self.base_paths.values():
            os.makedirs(path, exist_ok=True)

        # Validate API keys
        if not self.api_keys['riot']:
            print("Warning: Riot API key not found in environment variables.")
        if not self.api_keys['steam']:
            print("Warning: Steam API key not found in environment variables.")

    def fetch_riot_data(self, match_ids):
        """Fetch data from Riot Games API"""
        base_url = "https://americas.api.riotgames.com/lol/match/v5/matches/"
        headers = {"X-Riot-Token": self.api_keys['riot']}
        
        matches_data = []
        for match_id in match_ids:
            url = f"{base_url}{match_id}"
            for attempt in range(3):
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        matches_data.append(response.json())
                        break
                    elif response.status_code == 429:  # Rate limited
                        wait_time = int(response.headers.get("Retry-After", 2))
                        print(f"Rate limited. Waiting {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        print(f"Error {response.status_code}: {response.text}")
                        break
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching match {match_id}: {e}")
                    time.sleep(2 ** attempt + random.random())
            time.sleep(1.2)  # Riot API rate limiting
        
        return matches_data
    
    def fetch_dota_data(self, match_ids):
        """Fetch data from OpenDota API"""
        base_url = "https://api.opendota.com/api/matches/"
        
        matches_data = []
        for match_id in match_ids:
            url = f"{base_url}{match_id}"
            for attempt in range(3):
                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        matches_data.append(response.json())
                        break
                    else:
                        print(f"Error {response.status_code}: {response.text}")
                        break
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching match {match_id}: {e}")
                    time.sleep(2 ** attempt + random.random())
            time.sleep(1)  # OpenDota rate limiting
        
        return matches_data
    
    def save_data(self, data, filename, data_type='raw', pretty=False):
        """Save data to appropriate location"""
        path = os.path.join(self.base_paths[data_type], filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            if pretty:
                json.dump(data, f, indent=4)
            else:
                json.dump(data, f, separators=(',', ':'))
        print(f"Data saved to {path}")
    
    def load_sample_data(self):
        """Load sample data for demonstration purposes"""
        sample_data = {
            'matches': [],
            'players': [],
            'teams': []
        }
        return sample_data

    def to_dataframe(self, matches_data):
        """Convert list of matches into a pandas DataFrame"""
        return pd.json_normalize(matches_data)

if __name__ == "__main__":
    collector = DataCollector()
    # Example usage with sample data
    sample = collector.load_sample_data()
    collector.save_data(sample, "sample.json")
    df = collector.to_dataframe([sample])
    print(df.head())
