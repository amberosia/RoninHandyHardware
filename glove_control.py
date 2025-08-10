##################################################################
# script to read serial data from Arduino and store in a structure
##################################################################
import serial
import time
import requests

# Change to your Bluetooth COM port
ser = serial.Serial('COM7', 115200)
time.sleep(2)  # wait for Arduino reset
# exit()

# Example thresholds for each of the 5 values
thresholds = [1700, 1800, 1600, 1200, 1800]

# Local API endpoint
url = "http://127.0.0.1:7001/receive_signals"  # change to your API route

try:
    while True:
        # Read each lines
        line = ser.readline().decode('utf-8').strip()
        # exit()
        if line:
            values = line.split(",")  # list of strings
            values = [int(v) for v in values]  # convert to ints

            # Compare with thresholds
            for i, val in enumerate(values):
                if i!=0:
                    continue
                payload = {
                    "signal": "finger"+str(i+1),
                    "value": "flexed"+str(i+1) if (val > thresholds[i]) else "notflexed"+str(i+1)
                }
                print(val)
                #print(payload)
                # Send JSON to local server 
                try:
                    print(payload)
                    response = requests.post(url, json=payload, timeout=3)
                    # exit()
                    print(f"Server response: {response.status_code} - {response.text}")
                    print("Success")
                    #time.sleep(1)
                except requests.exceptions.RequestException as e:
                    print(f"Error sending data: {e}")

            #print(values)  # see values in console


# exit upon KeyboardInterrupt (Ctrl + C)
except KeyboardInterrupt:
    print("Stopped")
    ser.close()


