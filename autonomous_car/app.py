from env.constants import FUZZY_CONTROLLER, PROPORCIONAL_CONTROLLER, HOST, PORT, DETECT_YELLOW, STREET_ORIGINAL_IMAGE,\
    STREET_DETECTING, STREET_LINES_DRAWN, VIDEO_NAME
from system.image_processing.image_processing import jpgimg_to_base64
from flask import Flask, request, send_file, jsonify
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
    file_path = os.path.join(os.getcwd(), VIDEO_NAME)
    return send_file(file_path, as_attachment=True, cache_timeout=0)


@app.route('/get-log', methods=['GET'])
def get_log():
    log = autonomous_car.get_log_car()
    if log is not None:
        logs = []
        for item in log:
            logs.append(item)
        return jsonify({'logs': logs})
    else:
        return log


@app.route('/get-image-processed-camera')
def get_image_processed_camera():
    img_base64 = jpgimg_to_base64(autonomous_car.video_processed)
    return jsonify({"img": img_base64})


@app.route('/get-image-original-camera')
def get_image_original_camera():
    img_base64 = jpgimg_to_base64(autonomous_car.video_original)
    return jsonify({"img": img_base64})


@app.route('/controller-active', methods=['POST'])
def controller_active():
    if request.method == 'POST':
        json = request.get_json()
        if json['active'] == 'false':
            autonomous_car.send_commands_robot(False)
        else:
            autonomous_car.send_commands_robot(True)
    else:
        return 'Method not allowed!', 404
    return 'OK', 200


# @app.route('/log_output')
# def log_output():
#     file_path = os.path.join(os.path.join(os.getcwd(), 'autonomous_car/static/'), 'log.txt')
#     return send_file(file_path, as_attachment=True, cache_timeout=0)


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


def convert_string_to_int(string_value, default_value):
    try:
        converted = int(string_value)
        return converted
    except Exception as e:
        print str(e)
        return default_value


@app.route('/input-values', methods=['POST'])
def input_values():
    if request.method == 'POST':
        json = request.get_json()
        speed = convert_string_to_int(json['speed'], 0)
        angle = convert_string_to_int(json['angle'], 0)
        autonomous_car.speed_request(speed)
        autonomous_car.turn_request(angle)
    else:
        return 'Method not allowed!', 404
    return 'OK', 200


@app.route('/selected-video', methods=['POST'])
def selected_video():
    if request.method == 'POST':
        json = request.get_json()
        video = json['selected_video']
        if video == 'img-original':
            selected = STREET_ORIGINAL_IMAGE
        # elif video == 'img-color':
        #     selected = STREET_DETECTING
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
    # autonomous_car = AutonomousCar(PROPORCIONAL_CONTROLLER, DETECT_YELLOW)


if __name__ == "__main__":
    # app.run(host=HOST, port=PORT, debug=False, threaded=True)
    app.run(host=HOST, port=PORT, debug=True, threaded=True)


# Intervalo para considerar da imagem
# HEIGHT: 240 --> 420
# HEIGHT/2 --> HEIGHT - HEIGHT/8 = HEIGHT(1 - 1/8)

# H: 0 - 180
# S: 0 - 255
# V: 0 - 255

