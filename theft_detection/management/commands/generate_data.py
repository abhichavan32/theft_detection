from django.core.management.base import BaseCommand
from theft_detection.models import ElectricityData, PredictionResult
from theft_detection.ml_models.data_utils import DataGenerator, DataPreprocessor
from theft_detection.ml_models.detector import ElectricityTheftDetector
from django.utils import timezone
import numpy as np


class Command(BaseCommand):
    help = 'Generate synthetic electricity data and train ML models'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--normal',
            type=int,
            default=1000,
            help='Number of normal samples to generate'
        )
        parser.add_argument(
            '--theft',
            type=int,
            default=200,
            help='Number of theft samples to generate'
        )
        parser.add_argument(
            '--meters',
            type=int,
            default=10,
            help='Number of meters'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data generation...'))
        
        n_normal = options['normal']
        n_theft = options['theft']
        num_meters = options['meters']
        
        # Generate data
        self.stdout.write(f'Generating {n_normal} normal samples and {n_theft} theft samples...')
        df = DataGenerator.generate_dataset(
            n_normal=n_normal,
            n_theft=n_theft,
            num_meters=num_meters
        )
        
        # Save to database
        self.stdout.write('Saving data to database...')
        for idx, row in df.iterrows():
            ElectricityData.objects.create(
                meter_id=row['meter_id'],
                daily_consumption=row['daily_consumption'],
                monthly_consumption=row['monthly_consumption'],
                peak_hours_consumption=row['peak_hours_consumption'],
                off_peak_hours_consumption=row['off_peak_hours_consumption'],
                voltage_variation=row['voltage_variation'],
                current_variation=row['current_variation'],
                power_factor=row['power_factor'],
                reactive_power=row['reactive_power'],
                is_theft=row['is_theft']
            )
            
            if (idx + 1) % 100 == 0:
                self.stdout.write(f'  Saved {idx + 1} records...')
        
        # Train models
        self.stdout.write(self.style.SUCCESS('Training ML models...'))
        X = DataPreprocessor.get_features(df)
        
        detector = ElectricityTheftDetector()
        detector.train(X)
        
        # Make predictions on all data
        self.stdout.write('Making predictions...')
        all_data = ElectricityData.objects.all()
        
        for data in all_data:
            features = np.array([[
                data.daily_consumption,
                data.monthly_consumption,
                data.peak_hours_consumption,
                data.off_peak_hours_consumption,
                data.voltage_variation,
                data.current_variation,
                data.power_factor,
                data.reactive_power
            ]])
            
            results = detector.predict(features)
            
            lof_pred = 'theft' if results['lof_prediction'][0] == -1 else 'normal'
            if_pred = 'theft' if results['if_prediction'][0] == -1 else 'normal'
            voting_pred = 'theft' if results['voting_prediction'][0] == -1 else 'normal'
            
            PredictionResult.objects.create(
                electricity_data=data,
                lof_prediction=lof_pred,
                lof_score=float(results['lof_score'][0]),
                if_prediction=if_pred,
                if_score=float(results['if_score'][0]),
                voting_prediction=voting_pred,
                confidence=float(results['confidence'][0])
            )
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully generated and predicted {len(all_data)} records!'
        ))
