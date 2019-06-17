
class PIDController:
    def __init__(self):
        # Constantes do controlador
        # Proporcional
        self.KP = {'angle': 5.0, 'speed': 5.0}
        # Integral
        self.KI = {'angle': 1.0, 'speed': 1.0}
        # Derivative
        self.KD = {'angle': 1.0, 'speed': 1.0}
        self.max_error = 100000.0
        self.min_error = -100000.0
        self.previous_i_error = {'angle': 0, 'speed': 0}
        self.previous_d_error = {'angle': 0, 'speed': 0}
        self.previous_time = 0.0

    def reset(self, now_time):
        self.previous_i_error = {'angle': 0, 'speed': 0}
        self.previous_d_error = {'angle': 0, 'speed': 0}
        self.previous_time = now_time

    def proportional(self, error, variable):
        proporcional_part = self.KP[variable] * error
        return self.__set_max(proporcional_part, self.min_error, self.max_error)

    def integral(self, error, time_interval, variable):
        actual_error = error * time_interval
        self.previous_i_error = self.previous_i_error + actual_error
        integral_part = self.KI[variable] * self.previous_i_error
        return self.__set_max(integral_part, self.min_error, self.max_error)

    def derivative(self, error, time_interval, variable):
        d_error = (error - self.previous_error[variable]) / time_interval
        self.previous_d_error[variable] = error
        derivative_part = self.KD[variable] * d_error
        return self.__set_max(derivative_part, self.min_error, self.max_error)

    def pid_controller(self, error, variable, interval):
        r = self.proportional(error, variable) + self.integral(error, interval, variable) +\
            self.derivative(error, interval, variable)
        return r

    def output(self, distance_center, radius_curvature, run_time):
        try:
            interval = run_time - self.previous_time
            self.previous_time = run_time
            angle = self.pid_controller(distance_center, interval)
            # speed = self.pid_controller(radius_curvature, interval)
            speed = 45
            return speed, angle
        except Exception as e:
            print str(e)
            return 0, 0

    @staticmethod
    def __set_max(value, min_value, max_value):
        if value > 0 and value > max_value:
            return max_value
        if value < 0 and value < min_value:
            return min_value
        return value
