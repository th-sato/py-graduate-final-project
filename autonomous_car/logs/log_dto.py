
class LogDto:
    def __init__(self):
        # self._time =
        self.speed = 0
        self.angle = 0
        self.dist_center = 0
        self.curv = 0

    def __repr__(self):
        return str(self.__dict__)

