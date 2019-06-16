from flask import Flask, request, render_template, redirect, jsonify
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


# @app.route('/redis-image', methods=['GET', 'POST'])
# def image():
#     if request.method == 'GET':
#         img = r.get(REDIS_KEY_IMAGE)
#         if img is not None:
#             return HTML_IMAGE_HEADER + img, 200
#         else:
#             return "", 200
#     elif request.method == 'POST':
#         json = request.get_json()
#         r.set(REDIS_KEY_IMAGE, json['image'])
#         return "OK", 200
#     else:
#         return "Method not found", 404

def post_method(url, request_data):
    if request_data.method == 'POST':
        json_calibration = request_data.get_json()
        requests.post(url, json=json_calibration)
    else:
        return 'Method not allowed!', 404
    return 'OK', 200


@app.route('/get-video')
@cross_origin()
def get_video():
    url = HOST_AUTONOMOUS_CAR + '/video_output'
    return redirect(url)


@app.route('/get-log', methods=['GET'])
def get_log():
    url = HOST_AUTONOMOUS_CAR + '/get-log'
    if request.method == 'GET':
        return requests.get(url)
    else:
        return 'Method not allowed!', 404


@app.route('/get-image-processed-camera', methods=['GET'])
def get_image_processed_camera():
    url = HOST_AUTONOMOUS_CAR + '/get-image-processed-camera'
    if request.method == 'GET':
        resp = requests.get(url)
        return resp.content, resp.status_code, resp.headers.items()
    else:
        return 'Method not allowed!', 404


@app.route('/get-image-original-camera', methods=['GET'])
def get_image_original_camera():
    url = HOST_AUTONOMOUS_CAR + '/get-image-original-camera'
    if request.method == 'GET':
        resp = requests.get(url)
        return resp.content, resp.status_code, resp.headers.items()
    else:
        return 'Method not allowed!', 404


@app.route('/controller-active', methods=['POST'])
def controller_active():
    url = HOST_AUTONOMOUS_CAR + '/controller-active'
    return post_method(url, request)


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
    return post_method(url, request)


@app.route('/commands-by-request', methods=['POST'])
def commands_by_request_autonomous_car():
    url = HOST_AUTONOMOUS_CAR + '/commands-by-request'
    return post_method(url, request)


@app.route('/input-values', methods=['POST'])
def input_values():
    url = HOST_AUTONOMOUS_CAR + '/input-values'
    return post_method(url, request)


@app.route('/selected-video', methods=['POST'])
def selected_video():
    url = HOST_AUTONOMOUS_CAR + '/selected-video'
    return post_method(url, request)


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=False, threaded=True)
    # app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
