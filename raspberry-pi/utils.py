# importing geopy library and Nominatim class
from geopy.geocoders import Nominatim


def geolocateByAddress(address):
	# calling the Nominatim tool and create Nominatim class
	#loc = Nominatim(user_agent="my-app")

	# entering the location name
	#getLoc = loc.geocode(addres
	return {"address": "Elizabeth st", "lat": 144.9600585, "long": -37.8080842}

result = geolocateByAddress("175 5th Avenue NYC")
print(result)
