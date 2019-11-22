from django.conf.urls import url
from django.urls import path
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.schemas import get_schema_view

from . import views
from api.views.location_view import LocationList, LocationDetail
from api.views.user_view import LoginView, LogoutView
from api.views.location_user_view import LocationUserList, LocationUserDetailList
from api.views.user_register_view import LocationUserRegister

# urlpatterns = [
#     url(
#         r'^api/v1/locations/(?P<pk>[0-9]+)$',
#         views.get_delete_update_locations,
#         name='get_delete_update_locations'
#     ),
#     url(
#         r'^api/v1/locations/$',
#         views.get_post_locations,
#         name='get_post_locations'
#     )
# ]

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    path('locations/', LocationList.as_view(), name="locations_bezpk"),
    path('locations/<int:pk>/', LocationDetail.as_view(), name = "locations_zpk"),
    path('user/locations/', LocationUserList.as_view(), name="user_locations_bezpk"),
    path('user/locations/<int:pk>/', LocationUserDetailList.as_view(), name="user_locations_zpk"),
    path('user/register', LocationUserRegister.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('pla/', schema_view, name="docs"),
    path('logout/', LogoutView.as_view(), name="logout"),
]