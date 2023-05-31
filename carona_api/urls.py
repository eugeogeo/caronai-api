from django.urls import path
from caronapi.views import UserViewSet, RideListView, RideHistoryView, RideCreateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from caronapi.views import CustomTokenObtainPairView

schema_view = get_schema_view(
    openapi.Info(
        title="CaronAPI",
        default_version='v1',
        description="API para gerenciar caronas",
    ),
    public=True,
)

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/users/', UserViewSet.as_view({'post': 'create'}), name='user-create'),
    path('api/rides/', RideListView.as_view(), name='ride-list'),
    path('api/ride-history/', RideHistoryView.as_view(), name='ride-history'),
    path('api/rides/create/', RideCreateView.as_view(), name='ride-create'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
