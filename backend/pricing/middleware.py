import pytz
import requests
from django.utils import timezone
from timezonefinder import TimezoneFinder

class TimezoneMiddleware:
    """Middleware to set user timezone based on GPS or IP."""
    



    def __init__(self, get_response):
        self.get_response = get_response
        self.timezone_finder = TimezoneFinder() 

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return response
    
    def __get_timezone_from_gps(self, lat, lon):
        """Get timezone from GPS coordinates."""
        try:
            return self.timezone_finder.timezone_at(lng=lon, lat=lat) or "UTC"
        except Exception:
            return "UTC"

    def __get_location_from_ip(self, ip):
        """Fallback: Get location (lat, lon) from IP, since they are"""
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            data = response.json()
            
            if "loc" in data:
                lat, lon = map(float, data["loc"].split(","))
                return lat, lon
        except Exception:
            pass
        return None, None

    def process_request(self, request):
        """Detect and set the user's timezone."""
        lat = request.GET.get("latitude")
        lon = request.GET.get("longitude")
        ip_list = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR"))
        print("ip_list", ip_list)
        if ip_list:
            ip = ip_list.split(",")[0].strip() 
        else:
            ip = request.META.get("REMOTE_ADDR")
        print("ip init", ip, lon, lat)
        if lat and lon:
            timezone_str = self.__get_timezone_from_gps(float(lat), float(lon))
            print("gps timezone ", lat, lon, timezone_str)
        else:
            lat, lon = self.__get_location_from_ip(ip)
            timezone_str = self.__get_timezone_from_gps(lat, lon) if lat and lon else "UTC"
        print("ip timezone ", ip, lon, lat, timezone_str)
        timezone.activate(pytz.timezone(timezone_str))
        request.user_timezone = timezone_str 
