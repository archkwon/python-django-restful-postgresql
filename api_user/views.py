from django.shortcuts import render
import bcrypt
import jwt

from django.http import HttpResponse
from django.http.response import JsonResponse
from django.http import QueryDict

from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from api_user.serializers import CommuteModelSerializer
from api_user.models import UserModel
from api_user.models import TbCommuteInfo
from api_user.serializers import UserModelSerializer
from datetime import datetime
from django.shortcuts import get_object_or_404
from kinpecdriverapi.settings import SECRET_KEY

# [FBV] - Function based views - 함수기반(api_view)

"""
API 사용자조회
API 사용자등록
API 사용자전체삭제
"""
@api_view(['GET', 'POST'])
def api_user_list(request):

    if request.method == 'GET':
        user_list = UserModel.objects.all()
        user_list_serializer = UserModelSerializer(user_list, many=True)
        return JsonResponse(user_list_serializer.data, safe=False)

    elif request.method == 'POST':
        user_info = JSONParser().parse(request)
        user_info['user_pw'] = bcrypt.hashpw(user_info['user_pw'].encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        user_info['cre_id'] = 'admin'
        user_info['upt_id'] = 'admin'

        user_serializer = UserModelSerializer(data=user_info)

        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
API 사용자상세조회
API 사용자수정
API 사용자상세삭제
"""
@api_view(['GET', 'PUT', 'DELETE'])
def api_user_detail(request, pk):

    try:
        db_user_info = UserModel.objects.get(pk=pk)
    except UserModel.DoesNotExist:
        return JsonResponse({'message' : '사용자 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        user_serializer = UserModelSerializer(db_user_info)
        return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':

        user_info = JSONParser().parse(request)
        user_serializer = UserModelSerializer(db_user_info, data=user_info)

        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        db_user_info.delete()
        return JsonResponse({'message': '정상적으로 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

"""
API 로그인
"""
@api_view(['GET'])
def api_login(request):
    user_id = request.GET['userId']
    user_pw = request.GET['userPw']

    try:
        if UserModel.objects.filter(user_id=user_id).exists():
            user = UserModel.objects.get(user_id=user_id)

            if bcrypt.checkpw(user_pw.encode('UTF-8'), user.user_pw.encode('UTF-8')):
                token = jwt.encode({'user_id' : user.user_id}, SECRET_KEY, algorithm='HS256').decode('UTF-8')
                #return JsonResponse({'token' : token}, status=status.HTTP_200_OK)
                return JsonResponse({'userId': user.user_id}, status=status.HTTP_200_OK)

            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return JsonResponse({'message' : 'INVALID_KEYS'}, status=status.HTTP_400_BAD_REQUEST)




# [CBV] - Class based views - 클래스기반 (APIView)
"""
API 사용자조회
API 사용자등록
API 사용자전체삭제
"""
class UserListAction(APIView):
    def get(self, request):
        user_list = UserModel.objects.all()
        user_list_serializer = UserModelSerializer(user_list, many=True)
        return JsonResponse(user_list_serializer.data, safe=False)

    def post(self, request):
        user_json = JSONParser().parse(request)
        user_json['user_pw'] = bcrypt.hashpw(user_json['user_pw'].encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        user_json['cre_id'] = 'admin'
        user_json['upt_id'] = 'admin'

        user_serializer = UserModelSerializer(data=user_json)

        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
API 사용자상세조회
API 사용자수정
API 사용자상세삭제
"""
class UserDetailAction(APIView):

    def get_object(self, userId):
        return get_object_or_404(UserModel, pk=userId)

    def get(self, request, userId, format=None):
        user_detail = self.get_object(userId)
        user_serializer = UserModelSerializer(user_detail)
        return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, userId):
        user_json = JSONParser().parse(request)
        user_detail = self.get_object(userId)

        user_serializer = UserModelSerializer(user_detail, data=user_json)

        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, userId):
        user_detail = self.get_object(userId)
        user_detail.delete()
        return JsonResponse({'message': '정상적으로 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

"""
API 세션
"""
class SessionAction(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')

        if user_id:
            user_detail = UserModel.objects.get(user_id=request.session.get('user_id'))
            user_serializer = UserModelSerializer(user_detail)
            return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

"""
API 로그인
"""
class LoginAction(APIView):
    def post(self, request):
        userId = request.POST.get('userId', '')
        userPw = request.POST.get('userPw', '')
        deviceToken = request.POST.get('deviceToken', '')

        if UserModel.objects.filter(user_id=userId).exists():

            user_detail = UserModel.objects.get(user_id=userId)

            if bcrypt.checkpw(userPw.encode('UTF-8'), user_detail.user_pw.encode('UTF-8')):
                user_detail.device_token = deviceToken
                user_detail.save()

                if userId:
                    save_session(request, userId, userPw)

                    user_detail = UserModel.objects.get(user_id=userId)
                    user_serializer = UserModelSerializer(user_detail)
                return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)

            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


def save_session(request, user_id, user_pw):
    request.session['user_id'] = user_id
    request.session['user_pw'] = user_pw

"""
로그인 토큰 업데이트
"""
class LoginTokenAction(APIView):

    def put(self, request):
        userId = request.session.get('user_id')
        put = QueryDict(request.body)
        deviceToken = put.get('deviceToken')

        if UserModel.objects.filter(user_id=userId).exists():
             user_detail = UserModel.objects.get(user_id=userId)
             user_detail.device_token = deviceToken
             user_detail.save()

             return HttpResponse(status=status.HTTP_200_OK)

        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

"""
API 출근기록
"""
class RegisterTimeGoWorkAction(APIView):

    def post(self, request):
        userId = request.POST.get('user_id', '')
        attendee_time = request.POST.get('attendee_time', '')
        quitting_time = request.POST.get('quitting_time', '')

        if (attendee_time == '' and quitting_time == '') or userId == '':
            return JsonResponse(user_info.errors, status=status.HTTP_400_BAD_REQUEST)

        now = datetime.now()
        id = now.strftime('%Y%m%d%H%M%S%f')

        commute_json = {
            "id": id,
            "user_id": userId,
            "attendee_time": attendee_time,
            "quitting_time": quitting_time
        }
        commute_serializer = CommuteModelSerializer(data=commute_json)

        if commute_serializer.is_valid():
            commute_serializer.save()
            return JsonResponse(commute_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(commute_serializer.errors, status=status.HTTP_400_BAD_REQUEST)