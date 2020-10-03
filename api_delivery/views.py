from django.shortcuts import render
import os
import json
import math
import uuid
import boto3
from PIL import Image
from io import BytesIO
from datetime import datetime
from pyfcm import FCMNotification
from collections import OrderedDict
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from api_user.models import UserModel
from api_delivery.models import DeliveryMasterModel
from api_delivery.models import DeliveryPartModel
from api_delivery.models import DeliveryFileModel
from api_delivery.serializers import DeliveryMasterModelSerializer
from api_delivery.serializers import DeliveryPartModelSerializer
from api_delivery.forms import DeliveryFileForm
from django.core.exceptions import ImproperlyConfigured
from xml.etree.ElementTree import ParseError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#설정파일
config_file = os.path.join(BASE_DIR, 'config.json')
with open(config_file) as f:
    config = json.loads(f.read())

def get_config(setting, config=config):
    try:
        print("check config.json : ", config[setting])
        return config[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

# Create your views here.
"""
API 배송정보저장
"""
class DeliveryRegisterAction(APIView):

    def post(self, request):
        master_list = JSONParser().parse(request)

        try:
            for rows in master_list['masterList']:
                master_json = {}
                master_json['master_seq'] = rows['masterSeq']
                master_json['memo_code'] = rows['memoCode']
                master_json['order_code'] = rows['orderCode']
                master_json['cust_code'] = rows['custCode']
                master_json['cust_name'] = rows['custName']
                master_json['cust_lat'] = rows['custLat']
                master_json['cust_lng'] = rows['custLng']
                master_json['cust_address'] = rows['custAddress']
                master_json['distance'] = rows['custDistance']
                master_json['delivery_date'] = rows['deliveryDate']
                master_json['driver_mobile_num'] = rows['driverMobileNum']
                master_json['driver_name'] = rows['driverName']
                master_json['delivery_state_code'] = rows['deliveryStateCode']
                master_json['delivery_message'] = rows['deliveryMessage']
                master_json['part_count'] = rows['partCount']

                master_serializer = DeliveryMasterModelSerializer(data=master_json)
                if master_serializer.is_valid(raise_exception=True):
                    master_serializer.save()

                    for part_rows in rows['partList']:
                        part_json = {}
                        part_json['master_seq'] = part_rows['masterSeq']

                        now = datetime.now()
                        part_seq = now.strftime('%Y%m%d%H%M%S%f')
                        part_json['part_seq'] = part_seq + part_rows['partSeq']

                        part_json['part_code'] = part_rows['partCode']
                        part_json['part_name'] = part_rows['partName']

                        part_serializer = DeliveryPartModelSerializer(data=part_json)
                        if part_serializer.is_valid():
                            part_serializer.save()

            #FCM PUSH
            user_detail = UserModel.objects.get(user_id=master_list['masterList'][0]['driverMobileNum'])
            FCM_KEY = get_config("FCM_KEY")
            push_service = FCMNotification(api_key=FCM_KEY)
            registration_id = user_detail.device_token
            message_title = "AB"
            message_body = "refresh"
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
            print(result)

        except ParseError as error:
            return JsonResponse( 'Invalid JSON - {0}'.format(error), status=status.HTTP_400_BAD_REQUEST)

        return HttpResponse(status=status.HTTP_201_CREATED)

"""
API 배송정보수정
"""
class DeliveryModifyAction(APIView):

    def put(self, request):
        master_list = JSONParser().parse(request)

        try:
            for rows in master_list['masterList']:

                if DeliveryMasterModel.objects.filter(master_seq=rows['masterSeq']).exists():
                    master_detail = DeliveryMasterModel.objects.get(master_seq=rows['masterSeq'])

                    master_json = {}
                    master_json['master_seq'] = master_detail.master_seq
                    master_json['memo_code'] = master_detail.memo_code
                    master_json['order_code'] = master_detail.order_code
                    master_json['cust_code'] = master_detail.cust_code
                    master_json['cust_name'] = master_detail.cust_name
                    master_json['cust_lat'] = master_detail.cust_lat
                    master_json['cust_lng'] = master_detail.cust_lng
                    master_json['cust_address'] = master_detail.cust_address
                    master_json['distance'] = master_detail.distance
                    master_json['delivery_date'] = master_detail.delivery_date
                    master_json['delivery_state_code'] = master_detail.delivery_state_code
                    master_json['delivery_message'] = master_detail.delivery_message
                    master_json['part_count'] = master_detail.part_count
                    master_json['driver_mobile_num'] = rows['newMobileNum']
                    master_json['driver_name'] = rows['newDriverName']

                    master_serializer = DeliveryMasterModelSerializer(master_detail, data=master_json)
                    if master_serializer.is_valid():
                        master_serializer.save()

                #FCM PUSH
                old_user_detail = UserModel.objects.get(user_id=rows['oldMobileNum'])
                new_user_detail = UserModel.objects.get(user_id=rows['newMobileNum'])
                print(rows['oldMobileNum'])
                print(rows['newMobileNum'])
                FCM_KEY = get_config("FCM_KEY")
                push_service = FCMNotification(api_key=FCM_KEY)
                old_registration_id = old_user_detail.device_token
                new_registration_id = new_user_detail.device_token
                print(old_registration_id)
                print(new_registration_id)
                registration_ids = []
                registration_ids.append(old_registration_id)
                registration_ids.append(new_registration_id)
                message_title = "AB"
                message_body = "refresh"
                result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
                print(result)

        except ParseError as error:
            return JsonResponse( 'Invalid JSON - {0}'.format(error), status=status.HTTP_400_BAD_REQUEST)

        return HttpResponse(status=status.HTTP_200_OK)


"""
API 배송정보삭제
"""
class DeliveryDeleteAction(APIView):

    def put(self, request):
        master_list = JSONParser().parse(request)
        print(master_list['masterList'])

        #FCM PUSH
        driver_detail = DeliveryMasterModel.objects.filter(master_seq=master_list['masterList'][0]['masterSeq'])
        masterSeq = master_list['masterList'][0]['masterSeq']
        driver_master = DeliveryMasterModel.objects.get(master_seq=masterSeq)
        user_detail = UserModel.objects.get(user_id=driver_master.driver_mobile_num)
        FCM_KEY = get_config("FCM_KEY")
        push_service = FCMNotification(api_key=FCM_KEY)
        registration_id = user_detail.device_token
        message_title = "AB"
        message_body = "refresh"
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

        for rows in master_list['masterList']:
            if DeliveryMasterModel.objects.filter(master_seq=rows['masterSeq']).exists():
                DeliveryMasterModel.objects.filter(master_seq=rows['masterSeq']).delete()

            if DeliveryPartModel.objects.filter(master_seq=rows['masterSeq']).exists():
                DeliveryPartModel.objects.filter(master_seq=rows['masterSeq']).delete()

        return HttpResponse(status=status.HTTP_200_OK)

"""
API 기사님의 현재 배차출발 정보 조회
"""
class DriverDestinationRecentAction(APIView):
    def get(self, request):
        userId = request.GET['user_id']
        userType = request.GET['user_type']
        if userId == '':
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        today = datetime.now()
        searchDate = today.strftime('%Y%m%d%H%M%S%f')
        location_list = DeliveryMasterModel.objects.filter(
            driver_mobile_num=userId,
            delivery_state_code=userType
        ).filter(
            save_date__year=searchDate[:4],
            save_date__month=searchDate[4:6],
            save_date__day=searchDate[6:8]
        ).order_by(
            'distance'
        )
        delivery_list_serializer = DeliveryMasterModelSerializer(location_list, many=True)
        return JsonResponse(delivery_list_serializer.data, status=status.HTTP_200_OK, safe=False)

"""
API 기사배송완료(상태값만)
"""
class DeliveryCompleteAction(APIView):

    def post(self, request):
        master_seq = request.POST.get('master_seq', '')

        if DeliveryMasterModel.objects.filter(master_seq=master_seq).exists():
            DeliveryMasterModel.objects.filter(master_seq=master_seq).update(delivery_state_code='C',
                                                                             image_file_url='',
                                                                             complete_date=datetime.today().strftime(
                                                                                 '%Y-%m-%d %H:%M:%S'))

            return HttpResponse(status=status.HTTP_200_OK)

        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

"""
API 기사배송완료 일반경로파일업로드
"""
class DeliveryCompleteAction_DOC(APIView):

    def post(self, request, format=None):

        file_form = DeliveryFileForm(request.POST, request.FILES or None)

        if file_form.is_valid():

            image_obj = request.FILES['image_file']
            filename = image_obj._get_name()

            ext = os.path.splitext(filename)[1]
            valid_extensions = ['.png', '.jpeg', '.jpg', '.gif']
            if not ext.lower() in valid_extensions:
                return JsonResponse("Unsupported file extension.", status=status.HTTP_200_OK)

            if image_obj.size > 5 * 1024 * 1024:  # 5MB
                return JsonResponse("Max size of file is %s MB" % 5, status=status.HTTP_200_OK)

            fd = open(get_config("FILE_UPLOAD_PATH") + str(filename), 'wb+')
            for chunk in image_obj.chunks():
                fd.write(chunk)
            fd.close()

            data = file_form.cleaned_data
            file_seq = str(uuid.uuid4())
            master_seq = data['master_seq']

            fileModel = DeliveryFileModel.objects.create(
                file_seq=file_seq,
                master_seq=master_seq,
                image_file=filename,
                image_file_url='AWS'
            )
            fileModel.save()

            if DeliveryMasterModel.objects.filter(master_seq=master_seq).exists():
                DeliveryMasterModel.objects.filter(master_seq=master_seq).update(delivery_state_code='C',
                                                                                 image_file_url='',
                                                                                 complete_date=datetime.today().strftime(
                                                                                     '%Y-%m-%d %H:%M:%S'))

                return HttpResponse(status=status.HTTP_200_OK)

            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


"""
API 기사배송완료 AWS파일업로드
"""
class DeliveryCompleteAction_AWS(APIView):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=get_config("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=get_config("AWS_SECRET_ACCESS_KEY")
    )

    def post(self, request, format=None):

        file_form = DeliveryFileForm(request.POST, request.FILES or None)

        if file_form.is_valid():
            file_obj = request.FILES['image_file']
            file_name = file_obj._get_name()
            ext = os.path.splitext(file_name)[1]
            valid_extensions = ['.png', '.jpeg', '.jpg', '.gif']

            if not ext.lower() in valid_extensions:
                return JsonResponse("Unsupported file extension.", status=status.HTTP_200_OK)

            if file_obj.size > 5 * 1024 * 1024:  # 5MB
                return JsonResponse("Max size of file is %s MB" % 5, status=status.HTTP_200_OK)

            im = Image.open(file_obj)
            im = im.resize((600, 400))
            buffer = BytesIO()
            im.save(buffer, "png")
            buffer.seek(0)
            file_seq = str(uuid.uuid4())
            self.s3_client.upload_fileobj(
                buffer,
                get_config("AWS_STORAGE_BUCKET_NAME"),
                file_seq,
                ExtraArgs={
                    "ContentType": file_obj.content_type,
                    'ACL': 'public-read',  # 'private'
                }
            )
            file_url = get_config("AWS_STORAGE_BUCKET_URL") + file_seq

            data = file_form.cleaned_data
            master_seq = data['master_seq']
            fileModel = DeliveryFileModel.objects.create(
                file_seq=file_seq,
                master_seq=master_seq,
                image_file=file_name,
                image_file_url=file_url
            )
            fileModel.save()

            if DeliveryMasterModel.objects.filter(master_seq=master_seq).exists():
                DeliveryMasterModel.objects.filter(master_seq=master_seq).update(
                    delivery_state_code='C',
                    image_file_url=file_url,
                    complete_date=datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                )
                return HttpResponse(status=status.HTTP_200_OK)
        else :
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)