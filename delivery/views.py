from django.shortcuts import render
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from .forms import CustomerForm
from .models import Customer, HubLocation, Distance
from django.shortcuts import HttpResponse
from . import minHeap
from mapbox import Directions
import requests


def default_map(request):
    # TODO: move this token to Django settings from an environment variable
    # found in the Mapbox account settings and getting started instructions
    # see https://www.mapbox.com/account/ under the "Access tokens" section
    # if request.method == 'POST':
    customer_form = CustomerForm(request.POST or None, prefix='cus')
    if request.method == 'POST':

        if customer_form.is_valid():

            user = customer_form.save(commit=False)
            geolocator = Nominatim(user_agent="delivery")
            location1 = geolocator.geocode(
                customer_form.cleaned_data['origin'] + " Malaysia ")
            location2 = geolocator.geocode(
                customer_form.cleaned_data['destination'] + " Malaysia ")
            customerz = Customer()
            customerz.name = customer_form.cleaned_data['name']
            customerz.origin = customer_form.cleaned_data['origin']
            customerz.destination = customer_form.cleaned_data['destination']
            customerz.originLat = location1.latitude
            customerz.originLong = location1.longitude
            customerz.destinationLat = location2.latitude
            customerz.destinationLong = location2.longitude
            customerz.save()
            id = customerz.id

            # query all the delivery hubs
            hubLat = []
            hubLong = []
            hubName = []
            hubLocation = HubLocation.objects.filter().values(
                'deliverylat', 'deliverylong', 'courier_name')
            for hub in hubLocation:
                hubLat.append(hub['deliverylat'])
                hubLong.append(hub['deliverylong'])
                hubName.append(hub['courier_name'])
            # loop through all delivery hubs

            totalDistance = []
            for i in range(len(hubLat)):
                hubCoor = (hubLat[i], hubLong[i])
                cusCoor = (customerz.originLat, customerz.originLong)
                destiCoor = (customerz.destinationLat,
                             customerz.destinationLong)

                distanceObj = {
                    'origins': [{"latitude": cusCoor[0], "longitude":cusCoor[1]}, {"latitude": hubCoor[0], "longitude":hubCoor[1]}],
                    "destinations": [{"latitude": hubCoor[0], "longitude":hubCoor[1]}, {"latitude": destiCoor[0], "longitude":destiCoor[1]}],
                    "travelMode": "driving",
                }
                url = """https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key=AjTFB8Lz1hC464PmFGfuFFNE0JOD0KovK_BrHNA9jUQ1Y1Ox6wvxYjksswSL1fmW"""
                res = requests.post(url, json=distanceObj)
                distanceMatrix = res.json()
                distanceCusToHubKm = distanceMatrix["resourceSets"][0]["resources"][0]["results"][0]["travelDistance"]
                distanceHubToDesKm = distanceMatrix["resourceSets"][0]["resources"][0]["results"][3]["travelDistance"]
                totalDist = distanceHubToDesKm + distanceCusToHubKm
                totalDistance.append(totalDist)
            # Query current Db to get ID
            # customary = Customer.objects.get(pk=customary_id)

            cust_id = Customer.objects.get(id=id).id
            distance = Distance()
            distance.customer_id = cust_id  # we need int
            distance.distanceCityLink = totalDistance[0]
            distance.distancePosLaju = totalDistance[1]
            distance.distanceGdex = totalDistance[2]
            distance.distanceJnT = totalDistance[3]
            distance.distanceDHL = totalDistance[4]
            distance.save()

            show_result(request, id)
            return show_map(request, id)

            #   create a new record in a distance model (bridge entity)
            #   save to the distance model
        else:
            customer_form = CustomerForm(request.POST, prefix='cus')

    return render(request, 'delivery/default.html', {'customer_form': customer_form})


def show_result(request, pk):

    cust_id = Customer.objects.get(id=pk).id
    distance = Distance.objects.filter(customer=cust_id).values(

        'distanceCityLink',  'distancePosLaju',  'distanceGdex',  'distanceJnT',  'distanceDHL', 'shortestDistance')

    # if shortestDistance is already calculated
    if distance[0]['shortestDistance'] != "":
        return render(request, 'delivery/result.html',  {"khai": distance[0]['shortestDistance']})

    cityLink = distance[0]['distanceCityLink']
    posLaju = distance[0]['distancePosLaju']
    gDex = distance[0]['distanceGdex']
    jNT = distance[0]['distanceJnT']
    dHL = distance[0]['distanceDHL']

    dict = {cityLink: "City-link Express",
            posLaju: "Pos Laju",
            gDex: "GDEX",
            jNT: "JNT",
            dHL: "DHL"}

    min = minHeap.MinHeap(5)
    min.insert(cityLink)
    min.insert(posLaju)
    min.insert(gDex)
    min.insert(jNT)
    min.insert(dHL)
    min.minHeap()

    # get the courier name that has the shortest distance
    distanceShortest = min.getMin()
    ShortestDistance = dict[distanceShortest]
    distand = Distance.objects.filter(customer_id=cust_id).update(
        shortestDistance=ShortestDistance, distanceShortest=distanceShortest)

    # Frontend has a form that queries the customer name
    # Query the list of distances for the customer
    # After obtaining the list of distances, min-heapify
    # Extract min
    return render(request, 'delivery/result.html')


def show_map(request, pk):
    cust_id = Customer.objects.get(id=pk).id
    customer = Customer.objects.filter(id=cust_id).values(
        'originLat', 'originLong', 'destinationLat', 'destinationLong')
    distance = Distance.objects.filter(id=cust_id).values(
        'shortestDistance', 'distanceShortest')
    shortest = distance[0]['shortestDistance']
    distanceShort = distance[0]['distanceShortest']
    hubLocation = HubLocation.objects.filter(
        courier_name=shortest).values('deliverylat', 'deliverylong')
    oriLat = customer[0]['originLat']
    oriLong = customer[0]['originLong']
    destLat = customer[0]['destinationLat']
    destLong = customer[0]['destinationLong']
    delLat = hubLocation[0]['deliverylat']
    delLong = hubLocation[0]['deliverylong']

    return render(request, 'delivery/map.html', {"distance": distanceShort, 'oriLat': oriLat, 'oriLong': oriLong, 'shortest': shortest, 'destLat': destLat, 'destLong': destLong, 'delLat': delLat, 'delLong': delLong})
# pass origin destination and hub lat , long to frontend , store in javascript var to be rendere


# Frontend has a form that has a list of customer names
# If the customer does not have a shortest distance in Distance model
#   Redirect to show_result
# Else:
#   Query the customer's origin and destination
#   Query the list of couriers and their hubs
#   Query the shortest distance (company) from Distance model
#   For all couriers:
#       if courier-name != shortest distance:
#           plot the path of origin -> hub -> distance
#       else:
#           plot with different color
