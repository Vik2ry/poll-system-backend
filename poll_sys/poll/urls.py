from django.urls import path, include
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from .views import UserViewSet, PollViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'polls', PollViewSet, basename='polls')
# router.register(r'options', OptionViewSet, basename='options')


urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # LObtain the token with credentials
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh the token
    path('', include(router.urls)),  
]
