from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView, Response
from .serializers import PriceRequestSerializer, PriceResponseSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import calculate_price


# Create your views here.




def home(request):
    return JsonResponse({"message": "Welcome to Dynamic Pricing API"}, status=200)


class PricingView(APIView):
    '''
    API Endpoint for calculating the fare for a ride based on the distance, traffic level, demand level and the peak time.
    '''
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('distance', openapi.IN_QUERY, description="Distance in KM", type=openapi.TYPE_NUMBER,required=True),
            openapi.Parameter('traffic_level', openapi.IN_QUERY, description="Traffic condition (low, normal, high)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('demand_level', openapi.IN_QUERY, description="Demand condition (normal, peak)", type=openapi.TYPE_STRING, required=True),
            # longitudes and latitudes as optional parameters for peak pricing based peak time of the day
            openapi.Parameter('latitude', openapi.IN_QUERY, description="Starting Latitude", type=openapi.TYPE_NUMBER, default=6.516045),
            openapi.Parameter('longitude', openapi.IN_QUERY, description="Starting Longitude", type=openapi.TYPE_NUMBER, default=3.340390),

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
        serializer = PriceRequestSerializer(data=request.GET)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        validated_data = serializer.validated_data
        distance = validated_data["distance"]
        traffic_level = validated_data["traffic_level"]
        demand_level = validated_data["demand_level"]
        price_data = calculate_price(distance, demand_level, traffic_level)
        return Response(price_data, status=200)
        
