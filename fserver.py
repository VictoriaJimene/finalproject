from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Data storage using pandas DataFrame
data = pd.DataFrame(columns=['Time', 'Temperature', 'Humidity'])

# A route to accept data from the Raspberry Pi sensor
@app.route('/sensor_data', methods=['POST'])
def receive_sensor_data():
    if request.method == 'POST':
        temperature = request.form.get('Temperature')  # Extract form data
        humidity = request.form.get('Humidity')
        if temperature is not None and humidity is not None:
            now = datetime.now()
            new_row = {'Time': now, 'Temperature': temperature, 'Humidity': humidity}
            data = data.append(new_row, ignore_index=True)
            print(f"Received temperature: {temperature} C, humidity: {humidity} %")
            return "Data received successfully", 200
        else:
            return "No data received", 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)


