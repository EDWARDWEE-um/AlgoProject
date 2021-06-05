from django.shortcuts import render
from .serializers import DistanceSerializer, CustomSerializerer, HubLocationSerializer
from delivery.models import Customer, HubLocation, Distance
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, BasePermission, AllowAny
from rest_framework import viewsets

# Create your views here.


class CustomerView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = CustomSerializerer

    def get_queryset(self):
        return Customer.objects.all()


class HubLocationView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = HubLocationSerializer

    def get_queryset(self):
        return HubLocation.objects.all()


class DistanceView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = DistanceSerializer

    def get_queryset(self):
        return Distance.objects.all()
