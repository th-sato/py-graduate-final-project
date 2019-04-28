from picar import back_wheels, front_wheels
from constants.constants import STRAIGHT_ANGLE
import picar


class Robot:
    def __init__(self):
        picar.setup()
        db_file = "autonomous_car/picar_v/config"
        self.fw = front_wheels.Front_Wheels(debug=False, db=db_file)
        self.bw = back_wheels.Back_Wheels(debug=False, db=db_file)
        self.bw.ready()
        self.fw.ready()
        self.bw_status = 0

    def restart(self):
        self.bw.ready()
        self.fw.ready()
        self.bw_status = 0

    def __speed(self, speed):
        _speed = speed
        if speed < 0:
            _speed = 0
        elif speed > 100:
            _speed = 100
        else:
            _speed = speed

        if self.bw_status != 0:
            self.bw.speed = _speed

    def stop_car(self):
        self.bw_status = 0
        self.bw.stop()

    def forward(self, speed):
        self.bw_status = 1
        self.bw.forward()
        self.__speed(speed)

    def backward(self, speed):
        self.bw_status = -1
        self.bw.backward()
        self.__speed(speed)

    # angle < 0: turn left
    # angle > 0: turn right
    # angle = 0: straight
    def turn(self, angle):
        angle = STRAIGHT_ANGLE + angle
        # print("Angle", angle, type(angle))
        self.fw.turn(angle)

    def calibration_back_wheel(self, action):
        if action == 'calibration':
            self.bw.calibration()
        elif action == 'left':
            self.bw.cali_left()
        elif action == 'right':
            self.bw.cali_right()
        elif action == 'calibration_ok':
            self.bw.cali_ok()
        else:
            print 'Back Wheel. Command error "%s"' % action

    def calibration_front_wheel(self, action):
        if action == 'calibration':
            self.fw.calibration()
        elif action == 'left':
            self.fw.cali_left()
        elif action == 'right':
            self.fw.cali_right()
        elif action == 'calibration_ok':
            self.fw.cali_ok()
        else:
            print 'Front Wheel. Command error "%s"' % action
