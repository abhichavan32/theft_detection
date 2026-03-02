from django.db import models
from django.contrib.auth.models import User


class ElectricityData(models.Model):
    """Model to store electricity consumption data"""
    meter_id = models.CharField(max_length=50)
    daily_consumption = models.FloatField()
    monthly_consumption = models.FloatField()
    peak_hours_consumption = models.FloatField()
    off_peak_hours_consumption = models.FloatField()
    voltage_variation = models.FloatField()
    current_variation = models.FloatField()
    power_factor = models.FloatField()
    reactive_power = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_theft = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Meter {self.meter_id} - {self.timestamp}"


class PredictionResult(models.Model):
    """Model to store prediction results"""
    PREDICTION_CHOICES = [
        ('theft', 'Electricity Theft'),
        ('normal', 'Normal Usage'),
    ]
    
    electricity_data = models.ForeignKey(ElectricityData, on_delete=models.CASCADE)
    lof_prediction = models.CharField(max_length=10, choices=PREDICTION_CHOICES)
    lof_score = models.FloatField()
    if_prediction = models.CharField(max_length=10, choices=PREDICTION_CHOICES)
    if_score = models.FloatField()
    voting_prediction = models.CharField(max_length=10, choices=PREDICTION_CHOICES)
    confidence = models.FloatField()  # Voting confidence
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Prediction for {self.electricity_data.meter_id} - {self.voting_prediction}"
