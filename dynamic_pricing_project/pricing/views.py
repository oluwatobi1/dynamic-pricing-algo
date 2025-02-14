from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView, Response
from .serializers import PriceSerializer
from django.utils import timezone
from utils import constants, utils
from decimal import Decimal, ROUND_HALF_UP
from drf_yasg.utils import swagger_auto_schema

from drf_yasg import openapi


# Create your views here.




def home(request):
    return JsonResponse({"message": "Welcome to Dynamic Pricing API"}, status=200)


class PricingView(APIView):
    '''
    API Endpoint for calculating the fare for a ride based on the distance, traffic level, demand level and the peak time.
    '''
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('distance', openapi.IN_QUERY, description="Distance in KM", type=openapi.TYPE_NUMBER),
            openapi.Parameter('traffic_level', openapi.IN_QUERY, description="Traffic condition (low, normal, high)", type=openapi.TYPE_STRING),
            openapi.Parameter('demand_level', openapi.IN_QUERY, description="Demand condition (normal, peak)", type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.Response("Successful Response", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'base_fare': openapi.Schema(type=openapi.TYPE_NUMBER),
                'distance_fare': openapi.Schema(type=openapi.TYPE_NUMBER),
                'traffic_multiplier': openapi.Schema(type=openapi.TYPE_NUMBER),
                'demand_multiplier': openapi.Schema(type=openapi.TYPE_NUMBER),
                'total_fare': openapi.Schema(type=openapi.TYPE_NUMBER),
                "peak_hour_multiplier": openapi.Schema(type=openapi.TYPE_NUMBER),
                "request_time":  openapi.Schema(type=openapi.TYPE_STRING),
            },
        ))},
    )
    def get(self, request):
        '''
        This method calculates the fare based on the distance, traffic level, demand level and the current time.
        '''
        serializer = PriceSerializer(data=request.GET)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        validated_data = serializer.validated_data
        distance = validated_data["distance"]
        traffic_level = validated_data["traffic_level"]
        demand_level = validated_data["demand_level"]

        traffic_multiplier = constants.TRAFFIC_RATE[traffic_level]
        demand_multiplier = constants.DEMAND_RATE[demand_level]


        current_time = timezone.now().time()
        peak_hour_multiplier = 1
        if utils.is_peak_hours(current_time):
            peak_hour_multiplier = constants.PEAK_HOURS_RATE

        total_fare = (constants.BASE_FARE + (distance * constants.PER_KM_RATE)) * (traffic_multiplier * demand_multiplier * peak_hour_multiplier)

        # this is to ensure consistent rounding to 2 decimal places.. Cos: round() can 33.445 down to 33.44 instead of 33.45
        total_fare = Decimal(str(total_fare)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        return Response({
            "base_fare": constants.BASE_FARE,
            "distance_fare": distance * constants.PER_KM_RATE,
            "traffic_multiplier": traffic_multiplier,
            "demand_multiplier": demand_multiplier,
            "total_fare": total_fare,
            "peak_hour_multiplier": peak_hour_multiplier,
            "request_time": current_time.strftime("%H:%M"),
        }, status=200)
        
