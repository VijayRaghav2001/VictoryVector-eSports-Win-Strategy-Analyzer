import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
import numpy as np
import os

class DataVisualizer:
    def __init__(self):
        self.base_path = '../data/processed/'
        self.figures_path = '../reports/figures/'
        
    def load_data(self, filename):
        """Load processed data"""
        path = os.path.join(self.base_path, filename)
        return pd.read_csv(path)
    
    def plot_win_correlation(self, df, game_type='lol'):
        """Create correlation matrix for win factors"""
        if game_type == 'lol':
            features = [
                'first_blood', 'first_tower', 'total_towers', 
                'total_dragons', 'total_barons', 'win'
            ]
            title = 'League of Legends Win Correlation Matrix'
        else:
            features = [
                'kills', 'deaths', 'assists', 'gold_per_min', 
                'xp_per_min', 'radiant_win'
            ]
            title = 'Dota 2 Win Correlation Matrix'
        
        # Calculate correlation matrix
        corr_matrix = df[features].corr()
        
        # Create heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title(title)
        plt.tight_layout()
        plt.savefig(os.path.join(self.figures_path, f'{game_type}_correlation_matrix.png'))
        plt.close()
    
    def plot_feature_importance(self, importances, feature_names, game_type='lol'):
        """Plot feature importance from model"""
        indices = np.argsort(importances)[::-1]
        
        plt.figure(figsize=(10, 6))
        plt.title(f"Feature Importance - {game_type.upper()}")
        plt.bar(range(len(importances)), importances[indices])
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.figures_path, f'{game_type}_feature_importance.png'))
        plt.close()
    
    def plot_win_rate_by_objective(self, df, game_type='lol'):
        """Plot win rate by objectives"""
        if game_type == 'lol':
            objectives = ['first_blood', 'first_tower']
            title = 'League of Legends Win Rate by Objective'
        else:
            objectives = ['first_blood']  # Example for Dota
            title = 'Dota 2 Win Rate by Objective'
        
        fig, axes = plt.subplots(1, len(objectives), figsize=(15, 5))
        fig.suptitle(title)
        
        for i, objective in enumerate(objectives):
            win_rates = df.groupby(objective)['win'].mean()
            axes[i].bar(win_rates.index, win_rates.values)
            axes[i].set_title(f'Win Rate by {objective.replace("_", " ").title()}')
            axes[i].set_ylabel('Win Rate')
            axes[i].set_ylim(0, 1)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.figures_path, f'{game_type}_win_rate_by_objective.png'))
        plt.close()
    
    def create_interactive_plot(self, df, x_col, y_col, color_col, game_type='lol'):
        """Create an interactive plot using Plotly"""
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                         title=f"{game_type.upper()} Match Analysis")
        fig.write_html(os.path.join(self.figures_path, f'{game_type}_interactive_plot.html'))

if __name__ == "__main__":
    visualizer = DataVisualizer()
    
    # Example usage:
    # lol_data = visualizer.load_data('lol_matches_processed.csv')
    # visualizer.plot_win_correlation(lol_data, 'lol')
    # visualizer.plot_win_rate_by_objective(lol_data, 'lol')