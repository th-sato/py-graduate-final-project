
class LogDto:
    def __init__(self, time, speed, angle, dist_center, curv):
        self.time = time
        self.speed = speed
        self.angle = angle
        self.dist_center = dist_center
        self.curv = curv

    def __repr__(self):
        return str(self.__dict__)

