from utils import utils, constants
from django.utils import timezone
from django.utils.timezone import localtime
from utils import constants, utils
from decimal import Decimal, ROUND_HALF_UP









def calculate_price(distance, demand_level, traffic_level):
    '''
    Calculate the price of a ride based on the distance, demand level and traffic level
    
    '''
    traffic_multiplier = constants.TRAFFIC_RATE[traffic_level]
    demand_multiplier = constants.DEMAND_RATE[demand_level]
    # current_time = timezone.now().time()
    current_time = localtime(timezone=None).time()
    print("local_time", current_time)


    peak_hour_multiplier = 1
    if utils.is_peak_hours(current_time):
        peak_hour_multiplier = constants.PEAK_HOURS_RATE

    total_fare = (constants.BASE_FARE + (distance * constants.PER_KM_RATE)) * (traffic_multiplier * demand_multiplier * peak_hour_multiplier)

    # consistent rounding to 2 decimal places.. 
    total_fare = Decimal(str(total_fare)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return {
            "base_fare": constants.BASE_FARE,
            "distance_fare": distance * constants.PER_KM_RATE,
            "traffic_multiplier": traffic_multiplier,
            "demand_multiplier": demand_multiplier,
            "total_fare": total_fare,
            "peak_hour_multiplier": peak_hour_multiplier,
            "request_time": current_time.strftime("%H:%M"),
        }
