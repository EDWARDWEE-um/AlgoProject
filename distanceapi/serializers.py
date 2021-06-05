from delivery.models import Customer, HubLocation, Distance
from rest_framework import serializers


class CustomSerializerer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('__all__')

class HubLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HubLocation
        fields = ('__all__')

class DistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distance
        fields = ('__all__')



