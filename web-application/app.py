from flask import Flask, request, render_template, redirect, send_file
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

@app.route('/get-video')
@cross_origin()
def get_video():
    url = HOST_AUTONOMOUS_CAR + '/video_output'
    return redirect(url)


@app.route('/log')
def log():
    url = HOST_AUTONOMOUS_CAR + '/log_output'
    return redirect(url)


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


def post_method(url, request_data):
    if request_data.method == 'POST':
        json_calibration = request_data.get_json()
        requests.post(url, json=json_calibration)
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


# @app.route('/get-video', methods=['GET'])
# def get_video():
#     # url = HOST_AUTONOMOUS_CAR + '/get-video'
#     import os
#     file_path = os.path.join(os.path.join(os.getcwd(), 'web-application/static/video-test'), 'output.mp4')
#     return send_file(file_path, as_attachment=True, cache_timeout=0)


# @app.route('/calibration', methods=['POST'])
# def teste():
#     json = request.get_json()
#     print json['wheel']
#     print json['action']
#     return "OK", 200


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=False, threaded=True)
    # app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
