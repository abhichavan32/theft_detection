from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Avg, Q
from django.contrib import messages
import numpy as np
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import ElectricityData, PredictionResult
from .serializers import ElectricityDataSerializer, PredictionResultSerializer
from .ml_models.detector import get_detector


# HTML Views
def index(request):
    """Home page with dashboard"""
    try:
        total_records = ElectricityData.objects.count()
        theft_records = PredictionResult.objects.filter(voting_prediction='theft').count()
        normal_records = PredictionResult.objects.filter(voting_prediction='normal').count()
        
        # Ensure we show some theft records on the dashboard if they exist
        recent_thefts = list(PredictionResult.objects.select_related('electricity_data').filter(voting_prediction='theft')[:5])
        recent_normals = list(PredictionResult.objects.select_related('electricity_data').filter(voting_prediction='normal')[:5])
        
        # Combine and sort by created_at descending
        recent_predictions = sorted(recent_thefts + recent_normals, key=lambda x: x.created_at, reverse=True)
        
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
            
        # Search by meter ID or prediction
        search_query = request.GET.get('search', '').strip()
        if search_query:
            predictions = predictions.filter(
                Q(electricity_data__meter_id__icontains=search_query) |
                Q(voting_prediction__icontains=search_query)
            )
        elif not theft_filter:
            # If no search and no specific filter, mix recent normal and theft records
            recent_thefts = list(predictions.filter(voting_prediction='theft')[:10])
            recent_normals = list(predictions.filter(voting_prediction='normal')[:10])
            predictions = sorted(recent_thefts + recent_normals, key=lambda x: x.created_at, reverse=True)
        
        context = {
            'predictions': predictions,
            'theft_filter': theft_filter,
            'search_query': search_query,
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


@require_http_methods(["POST"])
def retrain_model(request):
    """Retrain the machine learning models using historical data"""
    try:
        data_records = ElectricityData.objects.all()
        if data_records.count() < 10:
            messages.error(request, 'Not enough historical data to retrain. Need at least 10 records.')
            return redirect('theft_detection:predictions_list')
            
        features = [
            'daily_consumption', 'monthly_consumption',
            'peak_hours_consumption', 'off_peak_hours_consumption',
            'voltage_variation', 'current_variation',
            'power_factor', 'reactive_power'
        ]
        
        X = []
        for record in data_records:
            row = [getattr(record, f) for f in features]
            X.append(row)
            
        X = np.array(X)
        
        detector = get_detector()
        detector.train(X)
        
        messages.success(request, f'Model successfully retrained using {len(X)} historical records to improve accuracy.')
    except Exception as e:
        messages.error(request, f'Error retraining model: {str(e)}')
        
    return redirect('theft_detection:predictions_list')


@require_http_methods(["POST"])
def predict_api(request):
    """Simple rule-based prediction for manual form submissions"""
    try:
        fields = [
            'daily_consumption', 'monthly_consumption',
            'peak_hours_consumption', 'off_peak_hours_consumption',
            'voltage_variation', 'current_variation',
            'power_factor', 'reactive_power',
        ]

        values = {}
        for field in fields:
            raw = request.POST.get(field)
            if raw is None:
                return JsonResponse({'error': f'Missing field: {field}'}, status=400)
            values[field] = float(raw)

        triggers = []

        if values['daily_consumption'] > 35:
            triggers.append('high_daily')
        if values['monthly_consumption'] > 1000:
            triggers.append('high_monthly')
        if values['peak_hours_consumption'] > values['daily_consumption'] * 0.8:
            triggers.append('heavy_peak_usage')
        if values['off_peak_hours_consumption'] > values['daily_consumption'] * 0.6:
            triggers.append('heavy_off_peak_usage')
        if abs(values['voltage_variation']) > 6:
            triggers.append('voltage_fluctuation')
        if abs(values['current_variation']) > 2.5:
            triggers.append('current_fluctuation')
        if values['power_factor'] < 0.85:
            triggers.append('low_power_factor')
        if values['reactive_power'] > 6:
            triggers.append('high_reactive_power')

        is_theft = len(triggers) > 0
        voting_pred = 'theft' if is_theft else 'normal'
        lof_pred = voting_pred
        if_pred = voting_pred

        max_rules = 8
        confidence = len(triggers) / max_rules if max_rules else 0.0

        meter_id = request.POST.get('meter_id')
        if not meter_id:
            meter_id = f'MTR-MANUAL-{timezone.now().strftime("%Y%m%d%H%M%S")}'

        electricity_data = ElectricityData.objects.create(
            meter_id=meter_id,
            daily_consumption=values['daily_consumption'],
            monthly_consumption=values['monthly_consumption'],
            peak_hours_consumption=values['peak_hours_consumption'],
            off_peak_hours_consumption=values['off_peak_hours_consumption'],
            voltage_variation=values['voltage_variation'],
            current_variation=values['current_variation'],
            power_factor=values['power_factor'],
            reactive_power=values['reactive_power'],
            is_theft=is_theft
        )

        lof_score = float(-len(triggers))
        if_score = float(-len(triggers) / 2.0)

        PredictionResult.objects.create(
            electricity_data=electricity_data,
            lof_prediction=lof_pred,
            lof_score=lof_score,
            if_prediction=if_pred,
            if_score=if_score,
            voting_prediction=voting_pred,
            confidence=float(confidence)
        )

        return JsonResponse({
            'voting_prediction': voting_pred,
            'lof_prediction': lof_pred,
            'if_prediction': if_pred,
            'confidence': float(confidence),
            'lof_score': lof_score,
            'if_score': if_score,
            'rules_triggered': triggers,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# API Views
class ElectricityDataViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for electricity data"""
    queryset = ElectricityData.objects.all()
    serializer_class = ElectricityDataSerializer
    
    @action(detail=False, methods=['post'])
    def predict(self, request):
        """Simple rule-based prediction API suited for this project"""
        try:
            fields = [
                'daily_consumption', 'monthly_consumption',
                'peak_hours_consumption', 'off_peak_hours_consumption',
                'voltage_variation', 'current_variation',
                'power_factor', 'reactive_power',
            ]

            values = {}
            for field in fields:
                if field not in request.data:
                    return Response({'error': f'Missing field: {field}'}, status=400)
                values[field] = float(request.data[field])

            triggers = []

            if values['daily_consumption'] > 35:
                triggers.append('high_daily')
            if values['monthly_consumption'] > 1000:
                triggers.append('high_monthly')
            if values['peak_hours_consumption'] > values['daily_consumption'] * 0.8:
                triggers.append('heavy_peak_usage')
            if values['off_peak_hours_consumption'] > values['daily_consumption'] * 0.6:
                triggers.append('heavy_off_peak_usage')
            if abs(values['voltage_variation']) > 6:
                triggers.append('voltage_fluctuation')
            if abs(values['current_variation']) > 2.5:
                triggers.append('current_fluctuation')
            if values['power_factor'] < 0.85:
                triggers.append('low_power_factor')
            if values['reactive_power'] > 6:
                triggers.append('high_reactive_power')

            is_theft = len(triggers) > 0
            voting_pred = 'theft' if is_theft else 'normal'
            lof_pred = voting_pred
            if_pred = voting_pred

            max_rules = 8
            confidence = len(triggers) / max_rules if max_rules else 0.0

            meter_id = request.data.get('meter_id')
            if not meter_id:
                meter_id = f'MTR-API-{timezone.now().strftime("%Y%m%d%H%M%S")}'

            electricity_data = ElectricityData.objects.create(
                meter_id=meter_id,
                daily_consumption=values['daily_consumption'],
                monthly_consumption=values['monthly_consumption'],
                peak_hours_consumption=values['peak_hours_consumption'],
                off_peak_hours_consumption=values['off_peak_hours_consumption'],
                voltage_variation=values['voltage_variation'],
                current_variation=values['current_variation'],
                power_factor=values['power_factor'],
                reactive_power=values['reactive_power'],
                is_theft=is_theft
            )

            lof_score = float(-len(triggers))
            if_score = float(-len(triggers) / 2.0)

            PredictionResult.objects.create(
                electricity_data=electricity_data,
                lof_prediction=lof_pred,
                lof_score=lof_score,
                if_prediction=if_pred,
                if_score=if_score,
                voting_prediction=voting_pred,
                confidence=float(confidence)
            )

            return Response({
                'voting_prediction': voting_pred,
                'lof_prediction': lof_pred,
                'if_prediction': if_pred,
                'confidence': float(confidence),
                'lof_score': lof_score,
                'if_score': if_score,
                'rules_triggered': triggers,
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
