import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
import Adafruit_DHT
import time

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

def send_data_to_server(temp, hum):
    url = "http://192.168.64.6:5000/sensor_data"  # Update with your server's IP and port
    try:
        response = requests.post(url, data={'Temperature': temp, 'Humidity': hum})  # Adjust payload keys to match server's expected keys
        if response.status_code == 200:
            print("Data sent successfully to the server.")
        else:
            print("Failed to send data to the server.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

def plot_temp_humidity(data):
    fig = px.line(data, x='Time', y=['Temperature', 'Humidity'], title='Temperature and Humidity Over Time')
    fig.show()

def main():
    try:
        while len(data) < 10:  # Collect 10 readings
            temp, hum = read_temperature_humidity()
            if temp is not None and hum is not None:
                now = datetime.now()
                new_row = {'Time': now, 'Temperature': temp, 'Humidity': hum}
                data = data.append(new_row, ignore_index=True)
                print(f"Recorded at {now}: Temperature: {temp} C, Humidity: {hum} %")
                send_data_to_server(temp, hum)
            buzz_buzzer()
            time.sleep(20)  # Interval of 20 seconds

        plot_temp_humidity(data)

    except KeyboardInterrupt:
        print("Stopped by User")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()


