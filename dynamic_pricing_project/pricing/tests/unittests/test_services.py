from django.test import TestCase
from unittest.mock import patch
from datetime import datetime
from pricing.services import calculate_price
from utils import constants
from decimal import Decimal, ROUND_HALF_UP

class PricingServiceTest(TestCase):




    @patch('pricing.services.timezone')
    def test_standard_fare_calculation_off_peak_period(self, mock_timezone):
        # Off peak hours
        request_time = "11:30"
        mock_timezone.now.return_value = datetime.strptime(request_time, "%H:%M")
        distance = 8
        demand = "normal"
        traffic = "high"
        total_fare = (constants.BASE_FARE + (distance*constants.PER_KM_RATE)) * (constants.TRAFFIC_RATE[traffic] * constants.DEMAND_RATE[demand])
        total_fare = Decimal(str(total_fare)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        expected = {
            "base_fare": constants.BASE_FARE,
            "distance_fare":(distance*constants.PER_KM_RATE),
            "traffic_multiplier": constants.TRAFFIC_RATE[traffic],
            "demand_multiplier": constants.DEMAND_RATE[demand],
            "total_fare": total_fare,
            "peak_hour_multiplier": 1,
            "request_time": request_time,
        }
        result = calculate_price(distance=distance,  demand_level=demand,traffic_level=traffic)
        self.assertEqual(result, expected)


    @patch('pricing.services.timezone')
    def test_standard_fare_calculation_peak_period(self, mock_timezone):
        # peak hours
        request_time = "08:30"
        mock_timezone.now.return_value = datetime.strptime(request_time, "%H:%M")
        distance = 5
        demand = "normal"
        traffic = "low"
        peak_hour_multiplier = constants.PEAK_HOURS_RATE # Expected higher fare during peak hours
        total_fare = (constants.BASE_FARE + (distance*constants.PER_KM_RATE)) * (constants.TRAFFIC_RATE[traffic] * constants.DEMAND_RATE[demand] *peak_hour_multiplier)
        total_fare = Decimal(str(total_fare)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        expected = {
            "base_fare": constants.BASE_FARE,
            "distance_fare":(distance*constants.PER_KM_RATE),
            "traffic_multiplier": constants.TRAFFIC_RATE[traffic],
            "demand_multiplier": constants.DEMAND_RATE[demand],
            "total_fare": total_fare,
            "peak_hour_multiplier": peak_hour_multiplier, # Expected higher fare during peak hours
            "request_time": request_time,
        }
        result = calculate_price(distance=distance,  demand_level=demand,traffic_level=traffic)
        self.assertEqual(result, expected)


    @patch('pricing.services.timezone')
    def test_high_traffic_peak_period(self, mock_timezone):
        # peak hours
        request_time = "08:30"
        mock_timezone.now.return_value = datetime.strptime(request_time, "%H:%M")
        distance = 8
        traffic = "high"
        demand = "normal"
        peak_hour_multiplier = constants.PEAK_HOURS_RATE # Expected higher fare during peak hours
        total_fare = (constants.BASE_FARE + (distance*constants.PER_KM_RATE)) * (constants.TRAFFIC_RATE[traffic] * constants.DEMAND_RATE[demand] *peak_hour_multiplier)
        total_fare = Decimal(str(total_fare)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        expected = {
            "base_fare": constants.BASE_FARE,
            "distance_fare":(distance*constants.PER_KM_RATE),
            "traffic_multiplier": constants.TRAFFIC_RATE[traffic],
            "demand_multiplier": constants.DEMAND_RATE[demand],
            "total_fare": total_fare,
            "peak_hour_multiplier": peak_hour_multiplier, # Expected higher fare during peak hours
            "request_time": request_time,
        }
        result = calculate_price(distance=distance,  demand_level=demand,traffic_level=traffic)
        self.assertEqual(result, expected)



    @patch('pricing.services.timezone')
    def test_surge_price_off_peak_period(self, mock_timezone):
        # Outside peak hours
        request_time = "11:30"
        mock_timezone.now.return_value = datetime.strptime(request_time, "%H:%M")
        distance = 12
        traffic = "normal"
        demand = "peak"
        peak_hour_multiplier = 1
        total_fare = (constants.BASE_FARE + (distance*constants.PER_KM_RATE)) * (constants.TRAFFIC_RATE[traffic] * constants.DEMAND_RATE[demand] *peak_hour_multiplier)
        total_fare = Decimal(str(total_fare)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        expected = {
            "base_fare": constants.BASE_FARE,
            "distance_fare":(distance*constants.PER_KM_RATE),
            "traffic_multiplier": constants.TRAFFIC_RATE[traffic],
            "demand_multiplier": constants.DEMAND_RATE[demand],
            "total_fare": total_fare,
            "peak_hour_multiplier": peak_hour_multiplier, 
            "request_time": request_time,
        }
        result = calculate_price(distance=distance,  demand_level=demand,traffic_level=traffic)
        self.assertEqual(result, expected)

    @patch('pricing.services.timezone')
    def test_peak_hour_with_high_traffic_outside_peak_period(self, mock_timezone):
        # Outside peak hours
        request_time = "11:30"
        mock_timezone.now.return_value = datetime.strptime(request_time, "%H:%M")
        distance = 7
        traffic = "high"
        demand = "peak"
        peak_hour_multiplier = 1
        total_fare = (constants.BASE_FARE + (distance*constants.PER_KM_RATE)) * (constants.TRAFFIC_RATE[traffic] * constants.DEMAND_RATE[demand] *peak_hour_multiplier)
        total_fare = Decimal(str(total_fare)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        expected = {
            "base_fare": constants.BASE_FARE,
            "distance_fare":(distance*constants.PER_KM_RATE),
            "traffic_multiplier": constants.TRAFFIC_RATE[traffic],
            "demand_multiplier": constants.DEMAND_RATE[demand],
            "total_fare": total_fare,
            "peak_hour_multiplier": peak_hour_multiplier, 
            "request_time": request_time,
        }
        result = calculate_price(distance=distance,  demand_level=demand,traffic_level=traffic)
        self.assertEqual(result, expected)



    @patch('pricing.services.timezone')
    def test_long_distance_peak_period(self, mock_timezone):
        # During peak hours
        request_time = "18:30"
        mock_timezone.now.return_value = datetime.strptime(request_time, "%H:%M")
        distance = 20
        traffic = "low"
        demand = "normal"
        peak_hour_multiplier = constants.PEAK_HOURS_RATE
        total_fare = (constants.BASE_FARE + (distance*constants.PER_KM_RATE)) * (constants.TRAFFIC_RATE[traffic] * constants.DEMAND_RATE[demand] *peak_hour_multiplier)
        total_fare = Decimal(str(total_fare)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        expected = {
            "base_fare": constants.BASE_FARE,
            "distance_fare":(distance*constants.PER_KM_RATE),
            "traffic_multiplier": constants.TRAFFIC_RATE[traffic],
            "demand_multiplier": constants.DEMAND_RATE[demand],
            "total_fare": total_fare,
            "peak_hour_multiplier": peak_hour_multiplier, 
            "request_time": request_time,
        }
        result = calculate_price(distance=distance,  demand_level=demand,traffic_level=traffic)
        self.assertEqual(result, expected)
