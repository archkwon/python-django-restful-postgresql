from rest_framework import serializers
from api_location.models import LocationModel

class LocationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationModel
        fields = ('seq',
                  'user_id',
                  'user_nm',
                  'user_mobile_no',
                  'lat',
                  'lng',
                  'save_dt')

