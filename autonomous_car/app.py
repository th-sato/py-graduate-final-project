from constants.constants import FUZZY_CONTROLLER, HOST, PORT, DETECT_YELLOW, STREET_ORIGINAL_IMAGE, STREET_DETECTING, STREET_LINES_DRAWN
from flask import Flask, request, send_file
from flask_cors import CORS
from autonomous_car import AutonomousCar
import os

app = Flask(__name__)
CORS(app, support_credentials=True)
# autonomous_car = AutonomousCar(FUZZY_CONTROLLER)


@app.route('/start')
def start():
    autonomous_car.start()
    return 'OK', 200


@app.route('/stop')
def stop():
    autonomous_car.stop()
    return 'OK', 200


@app.route('/video_output')
def video_output():
    file_path = os.path.join(os.path.join(os.getcwd(), 'autonomous_car/static/'), 'output.avi')
    return send_file(file_path, as_attachment=True, cache_timeout=0)


@app.route('/log_output')
def log_output():
    file_path = os.path.join(os.path.join(os.getcwd(), 'autonomous_car/static/'), 'log.txt')
    return send_file(file_path, as_attachment=True, cache_timeout=0)


@app.route('/calibration', methods=['POST'])
def car_calibration():
    if request.method == 'POST':
        json = request.get_json()
        if json['wheel'] == 'back':
            autonomous_car.backwheel_calib(json['action'])
        elif json['wheel'] == 'front':
            autonomous_car.frontwheel_calib(json['action'])
        else:
            return 'Command Error in wheel!', 404
    else:
        return 'Method not allowed!', 404
    return 'OK', 200


@app.route('/commands-by-request', methods=['POST'])
def commands_by_request():
    if request.method == 'POST':
        json = request.get_json()
        autonomous_car.commands_by_request(json['command'])
    else:
        return 'Method not allowed!', 404
    return 'OK', 200


@app.route('/input-values', methods=['POST'])
def input_values():
    if request.method == 'POST':
        json = request.get_json()
        speed = int(json['speed'])
        wheel = int(json['wheel'])
        autonomous_car.speed_request(speed)
        autonomous_car.turn_request(wheel)
    else:
        return 'Method not allowed!', 404
    return 'OK', 200


@app.route('/selected-video', methods=['POST'])
def selected_video():
    if request.method == 'POST':
        json = request.get_json()
        video = int(json['selected_video'])
        if video == 'img-original':
            selected = STREET_ORIGINAL_IMAGE
        elif video == 'img-color':
            selected = STREET_DETECTING
        # img-processed
        else:
            selected = STREET_LINES_DRAWN

        autonomous_car.image_to_show(selected)
    else:
        return 'Method not allowed!', 404
    return 'OK', 200


@app.route('/')
def home():
    return "OK", 200


@app.before_first_request
def before_first_request():
    global autonomous_car
    autonomous_car = AutonomousCar(FUZZY_CONTROLLER, DETECT_YELLOW)


if __name__ == "__main__":
    # app.run(host=HOST, port=PORT, debug=False, threaded=True)
    app.run(host=HOST, port=PORT, debug=True, threaded=True)


# Intervalo para considerar da imagem
# HEIGHT: 240 --> 420
# HEIGHT/2 --> HEIGHT - HEIGHT/8 = HEIGHT(1 - 1/8)

# H: 0 - 180
# S: 0 - 255
# V: 0 - 255

