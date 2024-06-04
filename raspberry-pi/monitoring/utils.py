import requests
def check_internet_connection():
    try:
        response = requests.get("https://dns.tutorialspoint.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False
