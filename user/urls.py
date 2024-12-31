from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoginUserView

router = DefaultRouter()
router.register('', UserViewSet, basename='user_reg')


urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('',include(router.urls)),
]
