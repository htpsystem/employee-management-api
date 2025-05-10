from django.urls import path, include
# from api.views import login, callback
from rest_framework.routers import DefaultRouter
from api.viewsets.employee import EmployeeViewSet
from api.viewsets.address import AddressViewSet
from api.viewsets.auth import AuthViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]
