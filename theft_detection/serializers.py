from rest_framework import serializers
from .models import ElectricityData, PredictionResult


class ElectricityDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricityData
        fields = '__all__'


class PredictionResultSerializer(serializers.ModelSerializer):
    meter_id = serializers.CharField(source='electricity_data.meter_id', read_only=True)
    
    class Meta:
        model = PredictionResult
        fields = [
            'id',
            'meter_id',
            'lof_prediction',
            'lof_score',
            'if_prediction',
            'if_score',
            'voting_prediction',
            'confidence',
            'created_at'
        ]
