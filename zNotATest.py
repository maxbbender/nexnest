import googlemaps
import pprint
import math

gmaps = googlemaps.Client(key='AIzaSyACeJxqY35gOjqNTIukZb6A6Zh6jvQnY3w')

response = gmaps.distance_matrix(origins='45 South Clover Street, Poughkeepsie, NY, 12601',
                                 destinations='Marist College',
                                 units='imperial')

pprint.pprint(response)

print("number of miles")


distanceValue = response['rows'][0]['elements'][0]['duration']['value']
print('distanceValue : %d' % distanceValue)

# print('distanceValue in miles : %f' % round((distanceValue / 1609.34), 1))

print('distanceValue in miles : %f' % math.ceil((distanceValue / 60)))

