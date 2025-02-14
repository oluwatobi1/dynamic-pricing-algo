from django.urls import path
from .views import PricingView, home

urlpatterns = [
    path("", home, name='home'), 
    path('calculate_fare/', PricingView.as_view(), name='calculate_fare'),
]