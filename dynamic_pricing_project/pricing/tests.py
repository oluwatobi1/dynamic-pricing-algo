from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch
from datetime import datetime
from rest_framework import status
from utils import constants
from decimal import Decimal, ROUND_HALF_UP
# Create your tests here.

class PricingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/calculate_fare/"

        self.test_table = [
            {
                "name": "Standard Fare Calculation",
                "params": {"distance": 5, "traffic_level":"low", "demand_level":"normal"},
                "expected": { "base_fare":constants.BASE_FARE, "distance_fare": 5*constants.PER_KM_RATE, "traffic_multiplier": constants.TRAFFIC_RATE["low"], "demand_multiplier": constants.DEMAND_RATE["normal"], 
                             "total_fare": (2.5 + (5*constants.PER_KM_RATE)) * (constants.TRAFFIC_RATE["low"] * constants.DEMAND_RATE["normal"])},
                "expected_status": status.HTTP_200_OK,
            },
            {
                "name": "High Traffic Pricing",
                "params": {"distance": 8, "traffic_level":"high", "demand_level":"normal"},
                "expected": { "base_fare":constants.BASE_FARE, "distance_fare": 8*constants.PER_KM_RATE, "traffic_multiplier": constants.TRAFFIC_RATE["high"], "demand_multiplier": constants.DEMAND_RATE["normal"], 
                             "total_fare": (2.5 + (8*constants.PER_KM_RATE)) * (constants.TRAFFIC_RATE["high"] * constants.DEMAND_RATE["normal"])},
                "expected_status": status.HTTP_200_OK,
            },
            {
                "name": "Surge Pricing (High Demand)",
                "params": {"distance": 12, "traffic_level":"normal", "demand_level":"peak"},
                "expected": { "base_fare":constants.BASE_FARE, "distance_fare": 12*constants.PER_KM_RATE, "traffic_multiplier": constants.TRAFFIC_RATE["normal"], "demand_multiplier": constants.DEMAND_RATE["peak"], 
                             "total_fare": (2.5 + (12*constants.PER_KM_RATE)) * (constants.TRAFFIC_RATE["normal"] * constants.DEMAND_RATE["peak"])},
                "expected_status": status.HTTP_200_OK,
            },
            {
                "name": "Peak Hour with High Traffic",
                "params": {"distance": 7, "traffic_level":"high", "demand_level":"peak"},
                "expected": { "base_fare":constants.BASE_FARE, "distance_fare": 7 * constants.PER_KM_RATE, "traffic_multiplier": constants.TRAFFIC_RATE["high"], "demand_multiplier": constants.DEMAND_RATE["peak"], 
                             "total_fare": (2.5 + (7*constants.PER_KM_RATE)) * (constants.TRAFFIC_RATE["high"] * constants.DEMAND_RATE["peak"])},
                "expected_status": status.HTTP_200_OK,
            },
            {
                "name": "Long Distance Ride",
                "params": {"distance": 20, "traffic_level":"low", "demand_level":"normal"},
                "expected": { "base_fare":constants.BASE_FARE, "distance_fare": 20 * constants.PER_KM_RATE, "traffic_multiplier": constants.TRAFFIC_RATE["low"], "demand_multiplier": constants.DEMAND_RATE["normal"], 
                             "total_fare": (2.5 + (20*constants.PER_KM_RATE)) * (constants.TRAFFIC_RATE["low"] * constants.DEMAND_RATE["normal"])},
                "expected_status": status.HTTP_200_OK,
            },
            {
                "name": "Invalid Distance Ride(Negative)",
                "params": {"distance": -10, "traffic_level":"low", "demand_level":"normal"},
                  "expected_status": status.HTTP_400_BAD_REQUEST,
            },
            {
                "name": "Invalid Traffic level",
                "params": {"distance": 10, "traffic_level":"heavy holdup", "demand_level":"normal"},
                  "expected_status": status.HTTP_400_BAD_REQUEST,
            },
            {
                "name": "Invalid Demand level",
                "params": {"distance": 15, "traffic_level":"low", "demand_level":"heavy demand"},
                  "expected_status": status.HTTP_400_BAD_REQUEST,
            },
            {
                "name": "Missing Parameters",
                "params": {},
                  "expected_status": status.HTTP_400_BAD_REQUEST,
            },
        ]

        
    @patch('pricing.views.timezone')
    def test_pricing_calculation_with_mocked_time(self, mock_timezone):
        '''
        Test the pricing calculation with controlled request times.
        '''

        test_times = [
            {"name":"Outside Peak Hour", "time": "11:30", "expected_peak_hour_multiplier": 1},
            {"name":"Morning Peak Hour", "time": "08:35", "expected_peak_hour_multiplier": constants.PEAK_HOURS_RATE},
            {"name":"Evening Peak Hour", "time": "18:45", "expected_peak_hour_multiplier": constants.PEAK_HOURS_RATE},
        ]
        for test_time in test_times:
            mock_timezone.now.return_value.time.return_value = datetime.strptime(test_time["time"], "%H:%M").time()
            for test_case in self.test_table:
                with self.subTest(msg=f'{test_case["name"]} - {test_time["name"]}'):
                    response = self.client.get(self.url, test_case["params"])
                    self.assertEqual(response.status_code, test_case["expected_status"])
                    if "expected" in test_case:
                        data = response.json()

                        expected_data = test_case["expected"].copy()
                        tf = expected_data["total_fare"] * test_time["expected_peak_hour_multiplier"]
                        total_fare = Decimal(str(tf)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                        expected_data["total_fare"] = float(total_fare)
                        expected_data["peak_hour_multiplier"] = test_time["expected_peak_hour_multiplier"]
                        expected_data["request_time"] = test_time["time"]

                        self.assertEqual(data, expected_data)
