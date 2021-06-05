from .views import  CustomerView, HubLocationView, DistanceView
from rest_framework.routers import DefaultRouter
from django.urls import path, include

app_name = 'distanceapi'

router = DefaultRouter()
router.register('customer', CustomerView, basename='customer')
router.register('hublocation', HubLocationView, basename='hublocation')
router.register('distance', DistanceView, basename='distance')


urlpatterns = [
    # Post Admin URLs
    path('', include(router.urls)),

]