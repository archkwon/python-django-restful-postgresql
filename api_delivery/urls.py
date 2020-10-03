from api_delivery import views
from django.urls import path

urlpatterns = [
    path('v1/driver/api/delivery/post', views.DeliveryRegisterAction.as_view()),
    path('v1/driver/api/delivery/put', views.DeliveryModifyAction.as_view()),
    path('v1/driver/api/delivery/delete', views.DeliveryDeleteAction.as_view()),
    path('v1/driver/api/destination/recent', views.DriverDestinationRecentAction.as_view()),
    path('v2/driver/api/delivery/complete', views.DeliveryCompleteAction.as_view()), #파일업로드 제외버전
    #path('v1/driver/api/delivery/complete', views.DeliveryCompleteAction_DOC.as_view()),  #일반경로 파일업로드
    path('v1/driver/api/delivery/complete', views.DeliveryCompleteAction_AWS.as_view()),  #AWS S3파일업로드
]

 