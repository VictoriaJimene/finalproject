from flask import Flask, request

app = Flask(__name__)

# A route to accept data from the Raspberry Pi sensor
@app.route('/sensor_data', methods=['POST'])
def sensor_data():
    if request.method == 'POST':
        # Try to extract temperature and humidity from the received JSON
        data = request.get_json()
        if data is not None:
            temperature = data.get('Temperature')
            humidity = data.get('Humidity')
            # Optionally, process or store the received data here
            print(f"Received temperature: {temperature} C, humidity: {humidity} %")
            return "Data received successfully", 200
        else:
            return "No data received", 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)

