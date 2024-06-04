import requests
def check_internet_connection():
    try:
        response = requests.get("https://google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def geolocateByAddress(address):
    geolocator = Nominatim(user_agent="my-app")
    location = geolocator.geocode(address)
    return {'address': location.address, 'lat': location.latitude, 'long': location.longitude}
