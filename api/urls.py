from django.conf.urls import url
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.views.location_user_view import ListCreateLocationView, RetrieveUpdateDestroyLocationView
from api.views.photo_view import RetrieveDestroyPhotoView, ListPhotoView, CreatePhotoView
from api.views.user_view import LoginView, LogoutView, RegisterUserView, PasswordChangeUserView, RetrieveUpdateUserView

schema_view = get_schema_view(
    openapi.Info(
        title="PAI Backend API",
        default_version='v1'
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('user/locations/', ListCreateLocationView.as_view(), name="user_locations_bezpk"),
    path('user/locations/<int:pk>/', RetrieveUpdateDestroyLocationView.as_view(), name="user_locations_zpk"),
    path('user/locations/<int:pk>/photos/', ListPhotoView.as_view(), name="photos_list"),
    path('photos/', CreatePhotoView.as_view(), name="photos_c"),
    path('photos/<int:pk>/', RetrieveDestroyPhotoView.as_view(), name="photos_rd"),
    path('user/register/', RegisterUserView.as_view(), name="register"),
    path('user/', RetrieveUpdateUserView.as_view(), name="users_ru"),
    path('change-password/', PasswordChangeUserView.as_view(), name="change-password"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
