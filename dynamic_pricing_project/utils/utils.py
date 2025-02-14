from .constants import PEAK_HOURS

def is_peak_hours(current_time):
    """
    Function to check if the current time is within peak hours
    """
    for start, end in PEAK_HOURS:
        if start <= current_time <= end:
            return True
    return False
