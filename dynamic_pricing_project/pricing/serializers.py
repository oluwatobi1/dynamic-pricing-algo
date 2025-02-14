from rest_framework import serializers

class PriceSerializer(serializers.Serializer):
    distance = serializers.FloatField(min_value=0, max_value=10**7, required=True, error_messages={
        "required": "Distance is required",
        "min_value": "Distance cannot be negative",
        "invalid": "Enter a valid distance",
        "max_value": "Distance is too large. Must be less than 10^7"
        })
    



    traffic_level = serializers.ChoiceField(choices=["low", "normal", "high"], required=True, error_messages={
        "required": "Traffic level is required",
        "invalid_choice": "Enter a valid traffic level. Must be ['low', 'normal', 'high']"
        })
    
    demand_level = serializers.ChoiceField(choices=["normal", "peak"], required=True, error_messages={
        "required": "Demand level is required",
        "invalid_choice": "Enter a valid demand level. Must be ['normal', 'peak']"
        })