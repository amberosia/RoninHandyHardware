from pylsl import StreamInlet, resolve_byprop
import time
import requests

# resolve an EMG stream on the lab network and notify the user
print("Looking for an EMG stream...")
streams = resolve_byprop('type', 'EMG')
inlet = StreamInlet(streams[0])
print("EMG stream found!")

# initialize time threshold and variables for storing time
time_thres_bicep = 500
time_thres_cheek = 1200
prev_time = 0
flex_thres = 0.5

# json values to send
bicep = "false"
mode = 0

# Local API endpoint
url = "http://127.0.0.1:7000/receive_signals"  # change to your API route

try:
	while True:

		samples, timestamp = inlet.pull_sample() # get EMG data sample and its timestamp

		curr_time = int(round(time.time() * 1000)) # get current time in milliseconds


		if ((samples[0] >=  flex_thres) & (curr_time - time_thres_bicep > prev_time)): # if an EMG spike is detected from the cheek muscles send 'G'
			prev_time = int(round(time.time() * 1000)) # update time
			bicep = "true"
		else:
			bicep = "false"


		if((samples[2] >=  flex_thres) & (curr_time - time_thres_cheek > prev_time)): # if an EMG spike is detected from the eyebrow muscles send 'R'
			prev_time = int(round(time.time() * 1000)) # update time
			mode = (mode + 1) % 3

		bicepPayload = {
			"signal": "bicep",
			"value": bicep
		}

		cheekPayload = {
			"signal": "trigger",
			"value": str(mode)
		}

		# Send JSON to local server
		try:
			response = requests.post(url, json=bicepPayload)
			print(f"Server response: {response.status_code} - {response.text}")
			response = requests.post(url, json=cheekPayload)
			print(f"Server response: {response.status_code} - {response.text}")
		except requests.exceptions.RequestException as e:
			print(f"Error sending data: {e}")

		#print(bicepPayload)
		#print(cheekPayload)

# exit upon KeyboardInterrupt (Ctrl + C)
except KeyboardInterrupt:
	print("Stopped")