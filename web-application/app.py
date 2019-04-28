from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from env import *
import logging
import redis
import requests

app = Flask(__name__)
r = redis.Redis(host=REDIS_IP, port=REDIS_PORT, db=0)
CORS(app, support_credentials=True)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/redis-image', methods=['GET', 'POST'])
# @cross_origin(supports_credentials=True)
def image():
    if request.method == 'GET':
        img = r.get(REDIS_KEY_IMAGE)
        if img is not None:
            return HTML_IMAGE_HEADER + img, 200
        else:
            return "", 200
    elif request.method == 'POST':
        json = request.get_json()
        r.set(REDIS_KEY_IMAGE, json['image'])
        return "OK", 200
    else:
        return "Method not found", 404


@app.route('/start', methods=['GET'])
def start_autonomous_car():
    url = HOST_AUTONOMOUS_CAR + '/start'
    if request.method == 'GET':
        requests.get(url)
    else:
        return 'Method not allowed!', 404
    return 'OK', 200


@app.route('/stop', methods=['GET'])
def stop_autonomous_car():
    url = HOST_AUTONOMOUS_CAR + '/stop'
    if request.method == 'GET':
        requests.get(url)
    else:
        return 'Method not allowed!', 404
    return 'OK', 200


@app.route('/calibration', methods=['POST'])
def calibration_autonomous_car():
    url = HOST_AUTONOMOUS_CAR + '/calibration'
    if request.method == 'POST':
        json_calibration = request.get_json()
        requests.post(url, json=json_calibration)
    else:
        return 'Method not allowed!', 404
    return 'OK', 200


@app.route('/commands-by-request', methods=['POST'])
def commands_by_request_autonomous_car():
    url = HOST_AUTONOMOUS_CAR + '/commands-by-request'
    if request.method == 'POST':
        json_commands = request.get_json()
        requests.post(url, json=json_commands)
    else:
        return 'Method not allowed!', 404
    return 'OK', 200


# @app.route('/calibration', methods=['POST'])
# def teste():
#     json = request.get_json()
#     print json['wheel']
#     print json['action']
#     return "OK", 200


if __name__ == "__main__":
    # app.run(host=HOST, port=PORT, debug=False)
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
