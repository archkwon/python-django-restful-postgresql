from django.shortcuts import render

from django.http.response import JsonResponse
from django.db import connection, transaction

from rest_framework.views import APIView
from rest_framework import status

from api_location.models import LocationModel
from api_user.models import UserModel
from api_location.serializers import LocationModelSerializer
from datetime import datetime
import time

# Create your views here.
"""
API 위치정보전체조회
"""
class LocationListAction(APIView):
    def get(self, request):
        if ('userId' in request.GET) and ('searchDate' in request.GET):

            userId = request.GET['userId']
            searchDate = request.GET['searchDate']

            if (userId is not None and userId != '') and (searchDate is not None and searchDate != ''):

                location_list = LocationModel.objects.filter(user_id=userId).filter(
                    save_dt__year=searchDate[:4],
                    save_dt__month=searchDate[4:6],
                    save_dt__day=searchDate[6:8])
                location_list_serializer = LocationModelSerializer(location_list, many=True)

                return JsonResponse(location_list_serializer.data, status=status.HTTP_200_OK, safe=False)

            return JsonResponse([], status=status.HTTP_200_OK, safe=False)

        return JsonResponse([], status=status.HTTP_200_OK, safe=False)

"""
API 기사들의 최신 위치 데이터 조회
"""
class LocationRecentAction(APIView):
    def get(self, request):
        location_list = LocationModel.objects.order_by(
            'user_id', '-save_dt'
        ).distinct(
            'user_id'
        )
        location_list_serializer = LocationModelSerializer(location_list, many=True)

        return JsonResponse(location_list_serializer.data, status=status.HTTP_200_OK, safe=False)

"""
API 위치정보등록
"""
class LocationRegisterAction(APIView):

    def post(self, request):

        userId = request.POST.get('userId', '')
        userMobileNo = request.POST.get('userMobileNo', '')
        lat = request.POST.get('lat', '')
        lng = request.POST.get('lng', '')

        user_info = UserModel.objects.get(user_id=userId)

        if userId == '' or userMobileNo == '':
            return JsonResponse(user_info.errors, status=status.HTTP_400_BAD_REQUEST)

        now = datetime.now()
        seq = now.strftime('%Y%m%d%H%M%S%f')

        location_json = {
            "seq": seq,
            "user_id": userId,
            "user_nm": user_info.user_nm,
            "user_mobile_no": userMobileNo,
            "lat": lat,
            "lng": lng
        }

        location_serializer = LocationModelSerializer(data=location_json)

        if location_serializer.is_valid():
            location_serializer.save()

            return JsonResponse(location_serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(location_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
