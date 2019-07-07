from env.constants import *
from threading import Thread
import time
from system.system import System
from system.image_processing.image_processing import video_writer
from picar_v.camera.camera import Camera
from picar_v.robot import Robot
# import requests


class AutonomousCar:
    def __init__(self, controller, color_street):
        self._stop_car = False
        self._controller = controller
        self._color_street = color_street
        self._video_processed = None
        self._video_original = None
        self._robot = Robot()
        # self._image_to_show = STREET_ORIGINAL_IMAGE
        self._image_to_show = STREET_LINES_DRAWN
        self._send_commands_robot = True
        self._camera = Camera(source=VIDEO_CAPTURE)
        self._system = System(self._controller, self._color_street)
        self._camera.start()

    def __start(self):
        Thread(target=self.update, args=()).start()

    def start(self):
        self._stop_car = False
        self._send_commands_robot = True
        self._camera.start()
        self.__start()

    def stop(self):
        self._stop_car = True
        self._send_commands_robot = False
        self._camera.stop()
        time.sleep(2)
        self._robot.stop_car()

    @property
    def video_original(self):
        return self._video_original

    @property
    def video_processed(self):
        return self._video_processed

    def image_to_show(self, option):
        self._image_to_show = option

    def send_commands_robot(self, command):
        self._send_commands_robot = command

    def backwheel_calib(self, action):
        self._robot.calibration_back_wheel(action)

    def frontwheel_calib(self, action):
        self._robot.calibration_front_wheel(action)

    def speed_request(self, speed):
        if speed > 0:
            self._robot.forward(speed)
        else:
            self._robot.backward(abs(speed))

    def turn_request(self, value):
        if (value > -45) and (value < 45):
            self._robot.turn(value)

    def commands_by_request(self, command):
        if command == "forward":
            self._robot.forward(40)
        elif command == "backward":
            self._robot.backward(40)
        elif command == "right":
            self._robot.turn(35)
        elif command == "left":
            self._robot.turn(-35)
        elif command == "straight":
            self._robot.turn(0)
        elif command == "stop":
            self._robot.stop_car()
        else:
            print "Command to Picar-V not found"

    def get_log_car(self):
        return self._system.get_log_system()

    def update(self):
        self._system.reset_log()
        video_output = video_writer()
        while not self._stop_car:
            # self._video_original = self.image_test()
            self._video_original = self._camera.frame
            self._video_processed, speed, angle = self._system.output(self._video_original, self._image_to_show)
            video_output.write(self._video_processed)
            if self._send_commands_robot:
                self._robot.forward(speed)
                self._robot.turn(angle)
            else:
                self._robot.forward(0)
                # Keep only turn command active
                self._robot.turn(angle)
                # self._robot.turn(0)
        video_output.release()
