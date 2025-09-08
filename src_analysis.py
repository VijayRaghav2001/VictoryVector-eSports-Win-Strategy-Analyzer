import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import joblib
import os

class ESportsAnalyzer:
    def __init__(self):
        self.base_path = '../data/processed/'
        self.models_path = '../models/trained_models/'
        
    def load_data(self, filename):
        """Load processed data"""
        path = os.path.join(self.base_path, filename)
        return pd.read_csv(path)
    
    def prepare_features(self, df, game_type='lol'):
        """Prepare features for modeling"""
        if game_type == 'lol':
            # For League of Legends data
            features = [
                'first_blood', 'first_tower', 'total_towers', 
                'total_dragons', 'total_barons', 'game_duration'
            ]
            target = 'win'
        else:
            # For Dota 2 data
            features = [
                'kills', 'deaths', 'assists', 'gold_per_min', 
                'xp_per_min', 'game_duration'
            ]
            target = 'radiant_win'
        
        X = df[features]
        y = df[target]
        
        return X, y
    
    def train_model(self, X, y, model_type='random_forest'):
        """Train a machine learning model"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        if model_type == 'random_forest':
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == 'xgboost':
            model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        else:
            raise ValueError("Unsupported model type")
        
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.2f}")
        print(classification_report(y_test, y_pred))
        
        return model, X_test, y_test
    
    def feature_importance(self, model, feature_names):
        """Calculate and display feature importance"""
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            print("Feature ranking:")
            for f in range(len(feature_names)):
                print(f"{f + 1}. {feature_names[indices[f]]} ({importances[indices[f]]:.4f})")
            
            return importances, indices
        else:
            print("Model doesn't have feature_importances_ attribute")
            return None, None
    
    def save_model(self, model, filename):
        """Save trained model to file"""
        path = os.path.join(self.models_path, filename)
        joblib.dump(model, path)
        print(f"Model saved to {path}")

if __name__ == "__main__":
    analyzer = ESportsAnalyzer()
    
    # Example usage for League of Legends data
    # lol_data = analyzer.load_data('lol_matches_processed.csv')
    # X, y = analyzer.prepare_features(lol_data, 'lol')
    # model, X_test, y_test = analyzer.train_model(X, y, 'random_forest')
    # analyzer.feature_importance(model, X.columns.tolist())
    # analyzer.save_model(model, 'lol_win_predictor.pkl')