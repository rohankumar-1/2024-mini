"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import json
import urequests
import network


N: int = 10
sample_ms = 10.0
on_ms = 500

FIREBASE_URI = '''https://miniproject-7f29e-default-rtdb.firebaseio.com/{name}.json'''

# WIFI CONNECTION
SSID = None # commented out for security
PASSWORD = None # commented out for security


def random_time_interval(tmin: float, tmax: float) -> float:
	"""return a random time interval between max and min"""
	return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
	# let user know game started / is over

	for _ in range(N):
		led.high()
		time.sleep(0.1)
		led.low()
		time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
	"""Writes data to a JSON file.

	Parameters
	----------

	json_filename: str
	The name of the file to write to. This will overwrite any existing file.

	data: dict
	Dictionary data to write to the file.
	"""
	with open(json_filename, "w") as f:
		json.dump(data, f)


def scorer(t: list[int | None]) -> None:
	# collate results
	misses = t.count(None)
	print(f"You missed the light {misses} / {len(t)} times")

	if(misses != N): # dont send empty values if the user missed all the blinks

		t_good = [x for x in t if x is not None]

		print(t_good)

		# add key, value to this dict to store the minimum, maximum, average response time
		# and score (non-misses / total flashes) i.e. the score a floating point number
		# is in range [0..1]
		data = {
      		'min': min(t_good), 
        	'max': max(t_good), 
         	'avg': sum(t_good) / len(t_good)
		}

		print(data) # gets printed in avg, max, min order

		# make dynamic filename and write JSON
		now: tuple[int] = time.localtime()

		now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
		filename = f"score-{now_str}.json"

		print("write", filename)
		write_json(filename, data)
		upload_to_firebase(data, now_str)
  
  
def connect_to_wifi(ssid, password):
    """a function that connects to local wifi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    
    print("Connected to Wifi.")
    

def upload_to_firebase(data: str, name: str):
    """ function sends data to firebase Realtime Database using name as ID """
    try:
        res = urequests.post(
            url=FIREBASE_URI.format(name=name),
            json=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        if res.status_code==200:
            print("Successful upload to firebase.")
        else:
            print("Unsuccessful upload to firebase.")
    except Exception as e:
        print(e)
    

if __name__ == "__main__":
	# using "if __name__" allows us to reuse functions in other script files
 
	# connect to wifi
	connect_to_wifi(SSID, PASSWORD)

	led = Pin("LED", Pin.OUT)
	button = Pin(15, Pin.IN, Pin.PULL_UP)

	t: list[int | None] = []

	blinker(3, led)

	for i in range(N):
		time.sleep(random_time_interval(0.5, 5.0))

		led.high()

		tic = time.ticks_ms()
		t0 = None
		while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
			if button.value() == 0:
				t0 = time.ticks_diff(time.ticks_ms(), tic)
				led.low()
				break

		t.append(t0)

		led.low()

		blinker(5, led)

	scorer(t)

