from constants.constants import FUZZY_CONTROLLER, PROPORCIONAL_CONTROLLER
from calibration.calibration import calibration
from system.image_processing.image_processing import show_image
from autonomous_car import AutonomousCar
import time

autonomous_car = AutonomousCar(FUZZY_CONTROLLER)


def stop_autonomous_car_by_seconds(seconds):
    time.sleep(seconds)
    autonomous_car.stop()


def main():
    calibration()
    autonomous_car.start()
    stop_autonomous_car_by_seconds(1)
    show_image(autonomous_car.video_original)
    show_image(autonomous_car.video_processed)


if __name__ == "__main__":
    main()


# Intervalo para considerar da imagem
# HEIGHT: 240 --> 420
# HEIGHT/2 --> HEIGHT - HEIGHT/8 = HEIGHT(1 - 1/8)

# H: 0 - 180
# S: 0 - 255
# V: 0 - 255

