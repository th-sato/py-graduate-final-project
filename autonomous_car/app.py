from constants.constants import FUZZY_CONTROLLER
from picar_v.calibration.calibration import calibration
from flask import Flask
from autonomous_car import AutonomousCar

app = Flask(__name__)
# autonomous_car = AutonomousCar(FUZZY_CONTROLLER)


@app.route('/start')
def start():
    autonomous_car.restart()
    return 'OK', 200


@app.route('/stop')
def stop():
    autonomous_car.stop()
    return 'OK', 200


@app.route('/calibration')
def car_calibration():
    calibration()
    return 'OK', 200


@app.route('/')
def home():
    return "OK", 200


@app.before_first_request
def before_first_request():
    global autonomous_car
    autonomous_car = AutonomousCar(FUZZY_CONTROLLER)


if __name__ == "__main__":
    # app.run(debug=False)
    app.run(debug=True)


# Intervalo para considerar da imagem
# HEIGHT: 240 --> 420
# HEIGHT/2 --> HEIGHT - HEIGHT/8 = HEIGHT(1 - 1/8)

# H: 0 - 180
# S: 0 - 255
# V: 0 - 255

