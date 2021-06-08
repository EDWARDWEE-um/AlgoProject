from django.db import models
from django.urls import reverse
# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    originLat = models.FloatField(null=True, blank=True, default=None)
    originLong = models.FloatField(null=True, blank=True, default=None)
    destination = models.CharField(max_length=200)
    destinationLat = models.FloatField(null=True, blank=True, default=None)
    destinationLong = models.FloatField(null=True, blank=True, default=None)
    oriToDes = models.FloatField(null=True, blank=True, default=None)
    # def __str__(self):
    #     return f"{self.name}: {self.origin} to {self.destination}"

    def get_absolute_url(self):
        return reverse('showresult', kwargs={'pk': self.pk})


class HubLocation(models.Model):
    courier_name = models.CharField(max_length=200)
    delivery_hub = models.CharField(max_length=200)
    deliverylat = models.FloatField(null=True, blank=True, default=None)
    deliverylong = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.courier_name}"


class Distance(models.Model):
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE ,related_name='%(class)s_name')
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer_name")

    distanceCityLink = models.FloatField(null=True, blank=True, default=None)
    distancePosLaju = models.FloatField(null=True, blank=True, default=None)
    distanceGdex = models.FloatField(null=True, blank=True, default=None)
    distanceJnT = models.FloatField(null=True, blank=True, default=None)
    distanceDHL = models.FloatField(null=True, blank=True, default=None)
    shortestDistance = models.CharField(max_length=200, default="")
    distanceShortest = models.FloatField(null=True, blank=True, default=None)

    # customer
    # origin
    # courier (we need to know what courier later)
    # hub
    # destination
    # total distance = from_origin_to_hub + hub-to-destination (we calc in views)
