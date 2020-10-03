from rest_framework import serializers
from api_delivery.models import DeliveryMasterModel
from api_delivery.models import DeliveryPartModel

class DeliveryMasterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMasterModel
        fields = ('master_seq',
            'memo_code',
            'order_code',
            'cust_code',
            'cust_name',
            'cust_lat',
            'cust_lng',
            'cust_address',
            'delivery_date',
            'driver_mobile_num',
            'driver_name',
            'delivery_state_code',
            'delivery_message',
            'save_date',
            'distance',
            'part_count',
            'complete_date',
            'image_file_url')

class DeliveryPartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPartModel
        fields = ('master_seq',
                  'part_seq',
                  'part_code',
                  'part_name',
                  'save_date')


