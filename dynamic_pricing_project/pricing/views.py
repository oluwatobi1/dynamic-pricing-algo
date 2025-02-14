from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView, Response
from .serializers import PriceSerializer
from django.utils import timezone
from utils import constants, utils


# Create your views here.




def home(request):
    return JsonResponse({"message": "Welcome to Dynamic Pricing API"}, status=200)


class PricingView(APIView):
    def get(self, request):
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

        total_fare = (constants.BASE_FARE + (distance * constants.PER_KM_RATE)) * \
              (traffic_multiplier * demand_multiplier * peak_hour_multiplier)

        return Response({
            "base_fare": constants.BASE_FARE,
            "distance_fare": distance * constants.PER_KM_RATE,
            "traffic_multiplier": traffic_multiplier,
            "demand_multiplier": demand_multiplier,
            "total_fare": total_fare,
            "peak_hour_multiplier": peak_hour_multiplier,
            "request_time": current_time.strftime("%H:%M"),
        }, status=200)
        

    def post(self, request):
        return HttpResponse("Hello, world. You're at the pricing index.")

