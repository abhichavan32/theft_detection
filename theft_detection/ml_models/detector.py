"""
Machine Learning Models for Electricity Theft Detection
Uses: Local Outlier Factor (LOF), Isolated Forest, and Voting Classifier
"""

import numpy as np
import pandas as pd
import joblib
import os
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from django.conf import settings


class ElectricityTheftDetector:
    """
    Ensemble model for detecting electricity theft using multiple algorithms
    """
    
    def __init__(self, models_dir=None):
        self.models_dir = models_dir or settings.ML_MODELS_DIR
        self.scaler = StandardScaler()
        self.lof_model = None
        self.if_model = None
        self.scaler_fitted = False
        self.contamination = 0.1  # Expect ~10% anomalies
        
    def train(self, X, y=None):
        """
        Train the LOF and Isolation Forest models
        X: Feature matrix (n_samples, n_features)
        y: Label array (optional, for validation)
        """
        # Fit scaler
        X_scaled = self.scaler.fit_transform(X)
        self.scaler_fitted = True
        
        # Train LOF (unsupervised) - use novelty=True for prediction on new data
        self.lof_model = LocalOutlierFactor(
            n_neighbors=20,
            contamination=self.contamination,
            novelty=True,
            n_jobs=-1
        )
        self.lof_model.fit(X_scaled)
        
        # Train Isolation Forest (unsupervised)
        self.if_model = IsolationForest(
            contamination=self.contamination,
            random_state=42,
            n_jobs=-1
        )
        self.if_model.fit(X_scaled)
        
        # Save models
        self.save_models()
        
    def load_models(self):
        """Load pre-trained models from disk"""
        try:
            scaler_path = os.path.join(self.models_dir, 'scaler.pkl')
            lof_path = os.path.join(self.models_dir, 'lof_model.pkl')
            if_path = os.path.join(self.models_dir, 'if_model.pkl')
            
            if all(os.path.exists(p) for p in [scaler_path, lof_path, if_path]):
                self.scaler = joblib.load(scaler_path)
                self.lof_model = joblib.load(lof_path)
                self.if_model = joblib.load(if_path)
                self.scaler_fitted = True
                return True
        except Exception as e:
            print(f"Error loading models: {e}")
        return False
    
    def save_models(self):
        """Save trained models to disk"""
        os.makedirs(self.models_dir, exist_ok=True)
        joblib.dump(self.scaler, os.path.join(self.models_dir, 'scaler.pkl'))
        joblib.dump(self.lof_model, os.path.join(self.models_dir, 'lof_model.pkl'))
        joblib.dump(self.if_model, os.path.join(self.models_dir, 'if_model.pkl'))
    
    def predict(self, X):
        """
        Predict using ensemble voting system
        Returns: (voting_prediction, confidence, lof_prediction, lof_score, if_prediction, if_score)
        """
        if not self.scaler_fitted or self.lof_model is None or self.if_model is None:
            self.load_models()
        
        X_scaled = self.scaler.transform(X)
        
        # LOF prediction (-1 for anomaly/theft, 1 for normal)
        lof_pred = self.lof_model.predict(X_scaled)
        lof_scores = self.lof_model.score_samples(X_scaled)
        
        # Isolation Forest prediction (-1 for anomaly/theft, 1 for normal)
        if_pred = self.if_model.predict(X_scaled)
        if_scores = self.if_model.score_samples(X_scaled)
        
        # Voting system
        votes = []
        for lof_p, if_p in zip(lof_pred, if_pred):
            vote = 0
            if lof_p == -1:
                vote += 1
            if if_p == -1:
                vote += 1
            votes.append(vote)
        
        votes = np.array(votes)
        voting_pred = np.where(votes >= 1, -1, 1)  # Majority voting (threshold=1)
        confidence = np.abs(votes / 2.0)  # Confidence based on agreement
        
        return {
            'voting_prediction': voting_pred,
            'confidence': confidence,
            'lof_prediction': lof_pred,
            'lof_score': lof_scores,
            'if_prediction': if_pred,
            'if_score': if_scores,
            'votes': votes
        }
    
    def predict_single(self, X_single):
        """Predict for a single sample (1D array or list)"""
        X_single = np.array(X_single).reshape(1, -1)
        return self.predict(X_single)


# Global detector instance
detector = None

def get_detector():
    """Get or create the global detector instance"""
    global detector
    if detector is None:
        detector = ElectricityTheftDetector()
        if not detector.load_models():
            print("Warning: No pre-trained models found. Train models before prediction.")
    return detector
