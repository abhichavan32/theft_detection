"""
Data generation and preprocessing utilities
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class DataGenerator:
    """Generate synthetic electricity consumption data"""
    
    @staticmethod
    def generate_normal_data(n_samples=1000, meter_id='M001'):
        """
        Generate normal electricity consumption patterns
        """
        data = []
        
        for i in range(n_samples):
            # Normal consumption patterns
            daily_consumption = np.random.normal(20, 3)  # kWh, mean=20, std=3
            monthly_consumption = daily_consumption * 30 + np.random.normal(0, 10)
            
            # Peak hours (9-21) have more consumption
            peak_hours = np.random.normal(12, 2)  # 9-21 hours
            off_peak_hours = np.random.normal(6, 1)  # 21-9 hours
            
            # Normal voltage and current
            voltage_variation = np.random.normal(0, 2)  # ±2V variation
            current_variation = np.random.normal(0, 1)  # ±1A variation
            
            # Good power factor (0.9-1.0)
            power_factor = np.random.uniform(0.92, 0.98)
            
            # Low reactive power
            reactive_power = np.random.normal(2, 0.5)
            
            data.append({
                'meter_id': meter_id,
                'daily_consumption': max(0.1, daily_consumption),
                'monthly_consumption': max(0.1, monthly_consumption),
                'peak_hours_consumption': max(0.1, peak_hours),
                'off_peak_hours_consumption': max(0, off_peak_hours),
                'voltage_variation': voltage_variation,
                'current_variation': current_variation,
                'power_factor': power_factor,
                'reactive_power': max(0, reactive_power),
                'is_theft': False
            })
        
        return data
    
    @staticmethod
    def generate_theft_data(n_samples=200, meter_id='M001'):
        """
        Generate suspicious electricity consumption patterns (theft)
        """
        data = []
        
        for i in range(n_samples):
            # Abnormal patterns indicating theft
            # High consumption at odd hours
            daily_consumption = np.random.uniform(35, 50)  # Unusually high
            monthly_consumption = daily_consumption * 30 + np.random.normal(0, 20)
            
            # Unusual consumption patterns
            peak_hours = np.random.uniform(15, 25)  # Very high peak
            off_peak_hours = np.random.uniform(8, 15)  # Unusually high off-peak
            
            # Voltage and current fluctuations (tampering)
            voltage_variation = np.random.uniform(-8, 8)  # Large fluctuations
            current_variation = np.random.uniform(-3, 3)  # Large fluctuations
            
            # Poor or unstable power factor
            power_factor = np.random.uniform(0.75, 0.88)
            
            # High reactive power (meter tampering)
            reactive_power = np.random.uniform(5, 12)
            
            data.append({
                'meter_id': meter_id,
                'daily_consumption': daily_consumption,
                'monthly_consumption': monthly_consumption,
                'peak_hours_consumption': peak_hours,
                'off_peak_hours_consumption': off_peak_hours,
                'voltage_variation': voltage_variation,
                'current_variation': current_variation,
                'power_factor': power_factor,
                'reactive_power': reactive_power,
                'is_theft': True
            })
        
        return data
    
    @staticmethod
    def generate_dataset(n_normal=1000, n_theft=200, num_meters=10):
        """
        Generate complete dataset with multiple meters
        """
        all_data = []
        
        for meter_num in range(num_meters):
            meter_id = f'M{meter_num+1:03d}'
            
            # Normal data
            normal_data = DataGenerator.generate_normal_data(
                n_samples=n_normal // num_meters,
                meter_id=meter_id
            )
            all_data.extend(normal_data)
            
            # Theft data
            theft_data = DataGenerator.generate_theft_data(
                n_samples=n_theft // num_meters,
                meter_id=meter_id
            )
            all_data.extend(theft_data)
        
        df = pd.DataFrame(all_data)
        # Randomize order
        df = df.sample(frac=1).reset_index(drop=True)
        return df


class DataPreprocessor:
    """Preprocess electricity data for ML models"""
    
    FEATURE_COLUMNS = [
        'daily_consumption',
        'monthly_consumption',
        'peak_hours_consumption',
        'off_peak_hours_consumption',
        'voltage_variation',
        'current_variation',
        'power_factor',
        'reactive_power'
    ]
    
    @staticmethod
    def get_features(df):
        """Extract feature matrix from dataframe"""
        return df[DataPreprocessor.FEATURE_COLUMNS].values
    
    @staticmethod
    def get_labels(df):
        """Extract labels from dataframe"""
        return df['is_theft'].values
