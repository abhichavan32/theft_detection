from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
import numpy as np
from datetime import timedelta

from .models import ElectricityData, PredictionResult
from .serializers import ElectricityDataSerializer, PredictionResultSerializer
from .ml_models.detector import get_detector
from .ml_models.data_utils import DataPreprocessor


# HTML Views
def index(request):
    """Home page with dashboard"""
    try:
        total_records = ElectricityData.objects.count()
        theft_records = PredictionResult.objects.filter(voting_prediction='theft').count()
        normal_records = PredictionResult.objects.filter(voting_prediction='normal').count()
        
        recent_predictions = PredictionResult.objects.select_related('electricity_data').all()[:10]
        
        context = {
            'total_records': total_records,
            'theft_records': theft_records,
            'normal_records': normal_records,
            'recent_predictions': recent_predictions,
        }
        return render(request, 'index.html', context)
    except Exception as e:
        return render(request, 'index.html', {'error': str(e)})


def predictions_list(request):
    """View all predictions"""
    try:
        predictions = PredictionResult.objects.select_related('electricity_data').all()
        
        # Filter by theft status
        theft_filter = request.GET.get('theft')
        if theft_filter:
            predictions = predictions.filter(voting_prediction=theft_filter)
        
        context = {
            'predictions': predictions,
            'theft_filter': theft_filter,
        }
        return render(request, 'predictions_list.html', context)
    except Exception as e:
        return render(request, 'predictions_list.html', {'error': str(e)})


def meter_detail(request, meter_id):
    """View details for a specific meter"""
    try:
        meter_data = ElectricityData.objects.filter(meter_id=meter_id)
        if not meter_data.exists():
            return render(request, 'meter_detail.html', {'error': 'Meter not found'})
        
        predictions = PredictionResult.objects.filter(
            electricity_data__meter_id=meter_id
        ).select_related('electricity_data')
        
        # Statistics
        theft_count = predictions.filter(voting_prediction='theft').count()
        normal_count = predictions.filter(voting_prediction='normal').count()
        avg_confidence = predictions.aggregate(
            avg=Avg('confidence')
        )['avg'] or 0
        
        context = {
            'meter_id': meter_id,
            'predictions': predictions[:50],
            'theft_count': theft_count,
            'normal_count': normal_count,
            'avg_confidence': avg_confidence,
        }
        return render(request, 'meter_detail.html', context)
    except Exception as e:
        return render(request, 'meter_detail.html', {'error': str(e)})


def predict_page(request):
    """Page for manual prediction"""
    return render(request, 'predict.html')


# API Views
class ElectricityDataViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for electricity data"""
    queryset = ElectricityData.objects.all()
    serializer_class = ElectricityDataSerializer
    
    @action(detail=False, methods=['post'])
    def predict(self, request):
        """Predict theft for given features"""
        try:
            required_fields = DataPreprocessor.FEATURE_COLUMNS
            
            # Extract features from request
            features = []
            for field in required_fields:
                if field not in request.data:
                    return Response({'error': f'Missing field: {field}'}, status=400)
                features.append(float(request.data[field]))
            
            # Make prediction
            detector = get_detector()
            X = np.array([features])
            results = detector.predict(X)
            
            voting_pred = 'theft' if results['voting_prediction'][0] == -1 else 'normal'
            lof_pred = 'theft' if results['lof_prediction'][0] == -1 else 'normal'
            if_pred = 'theft' if results['if_prediction'][0] == -1 else 'normal'
            
            return Response({
                'voting_prediction': voting_pred,
                'lof_prediction': lof_pred,
                'if_prediction': if_pred,
                'confidence': float(results['confidence'][0]),
                'lof_score': float(results['lof_score'][0]),
                'if_score': float(results['if_score'][0]),
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get statistics"""
        try:
            total = ElectricityData.objects.count()
            theft_count = PredictionResult.objects.filter(voting_prediction='theft').count()
            normal_count = PredictionResult.objects.filter(voting_prediction='normal').count()
            
            # Get accuracy if original labels exist
            accuracy = None
            if total > 0:
                correct = 0
                for pred in PredictionResult.objects.select_related('electricity_data').all():
                    is_theft = pred.electricity_data.is_theft
                    pred_theft = pred.voting_prediction == 'theft'
                    if is_theft == pred_theft:
                        correct += 1
                accuracy = correct / total
            
            return Response({
                'total_records': total,
                'theft_detected': theft_count,
                'normal_detected': normal_count,
                'accuracy': accuracy,
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class PredictionResultViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for prediction results"""
    queryset = PredictionResult.objects.select_related('electricity_data')
    serializer_class = PredictionResultSerializer
    
    @action(detail=False, methods=['get'])
    def by_meter(self, request):
        """Get predictions for a specific meter"""
        meter_id = request.query_params.get('meter_id')
        if not meter_id:
            return Response({'error': 'meter_id parameter required'}, status=400)
        
        predictions = self.queryset.filter(electricity_data__meter_id=meter_id)
        serializer = self.get_serializer(predictions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def theft_only(self, request):
        """Get only theft predictions"""
        predictions = self.queryset.filter(voting_prediction='theft')
        serializer = self.get_serializer(predictions, many=True)
        return Response(serializer.data)
