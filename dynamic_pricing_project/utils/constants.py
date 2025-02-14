from datetime import time

BASE_FARE = 2.5
PER_KM_RATE = 1.00
PEAK_HOURS_RATE = 1.3

TRAFFIC_RATE = {
    "low": 1,
    "normal": 1.3,
    "high": 1.5,
}



DEMAND_RATE = {
    "normal": 1,
    "peak": 1.8,
}

PEAK_HOURS = [
    (time(hour=7, minute=0), time(hour=10, minute=0)), # this is Morning peak hours  ie 7 AM - 10 AM
    (time(hour=12, minute=0), time(hour=13, minute=0)), # this is Afternoon peak hours ie 12 PM - 13 PM
    (time(hour=17, minute=0), time(hour=20, minute=0)), # this is Evening peak hours ie 5 PM - 8 PM
]

