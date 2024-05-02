import time
import RPi.GPIO as GPIO
import Adafruit_DHT
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests 

# Constants for GPIO pins
buzzer_pin = 13  # GPIO pin 13 is connected to the buzzer
dht_pin = 4  # GPIO pin 4 for the DHT22 data pin

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Sensor configuration
dht_sensor = Adafruit_DHT.DHT22

# Data storage using pandas DataFrame
data = pd.DataFrame(columns=['Time', 'Temperature', 'Humidity'])

def buzz_buzzer():
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(0.2)  # Buzzer on for 200 milliseconds
    GPIO.output(buzzer_pin, GPIO.LOW)

def read_temperature_humidity():
    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
    if humidity is not None and temperature is not None:
        return temperature, humidity
    else:
        print("Failed to get reading from the humidity and temperature sensor.")
        return None, None

try:
    while len(data) < 10:  # Modify this number based on how many data points you want to collect
        temp, hum = read_temperature_humidity()
        if temp is not None and hum is not None:
            now = datetime.now()
            new_row = {'Time': now, 'Temperature': temp, 'Humidity': hum}
            data = data.append(new_row, ignore_index=True)
            print(f"Recorded at {now}: Temperature: {temp} C, Humidity: {hum} %")
            # Prepare the data to send
            payload = {'Temperature': temp, 'Humidity': hum}  # Use form data format
            url = "http://192.168.64.6:6000/sensor_data"
            try:
                response = requests.post(url, data=payload)
                if response.status_code == 200:
                    print("Data sent successfully to the server.")
                else:
                    print("Failed to send data to the server.")
            except requests.exceptions.RequestException as e:
                print(f"Error sending data: {e}")
        buzz_buzzer()
        time.sleep(20)  # Interval of 20 seconds

    # Plotting using Plotly
    fig = px.line(data, x='Time', y='Temperature', title='Temperature Over Time', labels={'Temperature': 'Temperature (C)'})
    fig.add_scatter(x=data['Time'], y=data['Humidity'], name='Humidity', mode='lines')

    # Save the plot
    fig.write_image("/Downloads/Temp_Sensor_Graph.png")
    fig.show()

except KeyboardInterrupt:
    print("Stopped by User")
finally:
    GPIO.cleanup()

