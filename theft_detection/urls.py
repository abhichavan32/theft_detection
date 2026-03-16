from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'electricity-data', views.ElectricityDataViewSet)
router.register(r'predictions', views.PredictionResultViewSet)

app_name = 'theft_detection'

urlpatterns = [
    # HTML Views
    path('', views.index, name='index'),
    path('predictions/', views.predictions_list, name='predictions_list'),
    path('meter/<str:meter_id>/', views.meter_detail, name='meter_detail'),
    path('predict/', views.predict_page, name='predict_page'),
    path('predict/api/', views.predict_api, name='predict_api'),
    path('retrain/', views.retrain_model, name='retrain_model'),
    
    # API endpoints
    path('api/', include(router.urls)),
]
