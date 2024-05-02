from flask import Flask, request, jsonify

app = flask.Flask(__name__)

# A route to accept data from the Raspberry Pi sensor
@app.route('/sensor_data', methods=['POST'])
def sensor_data():
    if flask.request.method == 'POST':
        # Try to extract temperature and humidity from the received JSON
        message = flask.request.data
        return message    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)
