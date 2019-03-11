from picar import back_wheels, front_wheels
import picar


class PicarV:
    def __init__(self):
        picar.setup()
        db_file = "system/controller/picar_v/config"
        self.fw = front_wheels.Front_Wheels(debug=False, db=db_file)
        self.bw = back_wheels.Back_Wheels(debug=False, db=db_file)
        # self.fw.turning_max = 45
        self.bw.ready()
        self.fw.ready()
        self.bw_status = 0

    def restart(self):
        self.bw.ready()
        self.fw.ready()
        self.bw_status = 0

    def speed(self, speed):
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

    def forward(self):
        self.bw_status = 1
        self.bw.forward()

    def backward(self):
        self.bw_status = -1
        self.bw.backward()

    def turn_straight(self):
        self.fw.turn_straight()

    # angle < 0: turn left
    # angle > 0: turn right
    # angle = 0: straight
    def turn(self, angle):
        print("Angle", angle)
        self.fw.turn(angle)


