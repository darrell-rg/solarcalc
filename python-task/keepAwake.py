



import requests
import time
import random

counter = 0

def make_request(url):
    try:
        response = requests.get(url)
        print(f"{counter} Response Code: {response.status_code}, Response Time: {response.elapsed.total_seconds()} seconds")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    pwr = random.randint(10, 9999)
    liters = random.randint(10, 400)
    url = f"https://cfe915ba-d8b7-41c6-84ff-4f1b5c0fd87f-prod.e1-us-cdp-2.choreoapis.dev/solar-calculator/solarcalcflask2/solar-sim-30a/v1.0/json?lat=40.5&lng=-104.7&tilt=40&azimuth=180&pwr={pwr}.96&losses=14&module_type=1&liters={liters}&uef=0.91&startingTemp=40&Rw=0.201&Re=-8.73&pps=3&ps=1&MN=null" 
    while True:
        make_request(url)
        sleep_time = random.randint(30, 60*4)  # Default sleep time is 5 min
        print(f"Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)
        counter += 1


