from rest_framework import serializers
from api_user.models import UserModel
from api_user.models import TbCommuteInfo

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('user_id',
                  'user_pw',
                  'user_nm',
                  'user_mobile_no',
                  'user_ty',
                  'device_token',
                  'cre_dt',
                  'cre_id',
                  'upt_dt',
                  'upt_id')

class CommuteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TbCommuteInfo
        fields = ('id',
                  'user_id',
                  'attendee_time',
                  'quitting_time',
                  'register_dt')
