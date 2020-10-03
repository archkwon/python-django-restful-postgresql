from api_location import views
from django.urls import path, include

urlpatterns = [
    path('v1/driver/api/location/list', views.LocationListAction.as_view()),
    path('v1/driver/api/location/recent/all', views.LocationRecentAction.as_view()),
    path('v1/driver/api/location/post', views.LocationRegisterAction.as_view()),
]
