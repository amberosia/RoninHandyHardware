##################################################################
# script to read serial data from Arduino and store in a structure
##################################################################
import serial
import time
import requests

# Change to your Bluetooth COM port
ser = serial.Serial('COM9', 115200)
time.sleep(2)  # wait for Arduino reset

data = []

# Example thresholds for each of the 6 values
thresholds = [100, 200, 150, 300, 250, 400]

# Local API endpoint
url = "http://127.0.0.1:5000/data"  # change to your API route

try:
    while True:
        # Read each lines
        line = ser.readline().decode('utf-8').strip()
        if line:
            values = line.split(",")  # list of strings
            values = [int(v) for v in values]  # convert to ints

            # Compare with thresholds
            for i, val in enumerate(values):
                payload = {
                    "signal": i,
                    "value": "flexed" if (val > thresholds[i]) else "not flexed"
                }
                # Send JSON to local server
                try:
                    response = requests.post(url, json=payload)
                    print(f"Server response: {response.status_code} - {response.text}")
                except requests.exceptions.RequestException as e:
                    print(f"Error sending data: {e}")

            data.append(values)
            print(values)  # see values in console


# exit upon KeyboardInterrupt (Ctrl + C)
except KeyboardInterrupt:
    print("Stopped")
    ser.close()
