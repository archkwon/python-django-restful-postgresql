from django.conf.urls import url
from api_user import views
from django.conf.urls import url, include
from django.urls import path, include

urlpatterns = [

    # [FBV] - Function based views - 함수기반(api_view)
    #url(r'^driver/api/user$', views.api_user_list),
    #url(r'^driver/api/user/(?P<pk>[A-Za-z0-9]+)$', views.api_user_detail),
    #url(r'^driver/api/login$', views.api_login)
    #url(r'^v1/user/session$', views.api_session_login)

    #[CBV] - Class based views - 클래스기반 (APIView)
    path('v1/driver/api/user', views.UserListAction.as_view()),
    path('v1/driver/api/user/<userId>', views.UserDetailAction.as_view()),
    path('v1/driver/api/login', views.LoginAction.as_view()),
    path('v1/user/session', views.SessionAction.as_view()),
    path('v1/driver/api/login/token', views.LoginTokenAction.as_view()),
    path('v1/driver/api/time/commute/post', views.RegisterTimeGoWorkAction.as_view())
]
