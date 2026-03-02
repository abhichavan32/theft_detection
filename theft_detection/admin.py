from django.contrib import admin
from .models import ElectricityData, PredictionResult

@admin.register(ElectricityData)
class ElectricityDataAdmin(admin.ModelAdmin):
    list_display = ('meter_id', 'daily_consumption', 'is_theft', 'timestamp')
    list_filter = ('is_theft', 'timestamp')
    search_fields = ('meter_id',)

@admin.register(PredictionResult)
class PredictionResultAdmin(admin.ModelAdmin):
    list_display = ('electricity_data', 'lof_prediction', 'if_prediction', 'voting_prediction', 'confidence')
    list_filter = ('voting_prediction', 'created_at')
    search_fields = ('electricity_data__meter_id',)
