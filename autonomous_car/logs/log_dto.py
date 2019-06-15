
class LogDto:
    def __init__(self):
        self._speed = 0
        self._angle = 0
        self._dist_center = 0
        self._curv = 0

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, new_speed):
        self._speed = new_speed

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, new_angle):
        self._angle = new_angle

    @property
    def dist_center(self):
        return self._dist_center

    @dist_center.setter
    def dist_center(self, new_dist_center):
        self._dist_center = new_dist_center

    @property
    def curv(self):
        return self._curv

    @curv.setter
    def curv(self, new_curv):
        self._curv = new_curv