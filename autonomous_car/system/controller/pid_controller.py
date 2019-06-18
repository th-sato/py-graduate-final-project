
class PIDController:
    def __init__(self):
        # Constantes do controlador
        # Proporcional
        self.KP = {'angle': 400.0, 'speed': 5.0}
        # Integral
        # self.KI = {'angle': 30.0, 'speed': 1.0}
        # Derivative
        # self.KD = {'angle': 1.0, 'speed': 1.0}
        self.max_error = 100000.0
        self.min_error = -100000.0
        # self.previous_i_error = {'angle': 0.0, 'speed': 0.0}
        # self.previous_d_error = {'angle': 0.0, 'speed': 0.0}
        # self.previous_time = 0.0

    def reset(self, now_time):
        # self.previous_i_error = {'angle': 0, 'speed': 0}
        # self.previous_d_error = {'angle': 0, 'speed': 0}
        # self.previous_time = now_time
        return

    def proportional(self, error, variable):
        proporcional_controller = self.KP[variable] * error
        return self.__set_max(proporcional_controller, self.min_error, self.max_error)

    # def integral(self, error, time_interval, variable):
    #     actual_error = error * time_interval
    #     integral_part = self.previous_i_error[variable] + actual_error
    #     self.previous_i_error[variable] = integral_part
    #     integral_controller = self.KI[variable] * integral_part
    #     return self.__set_max(integral_controller, self.min_error, self.max_error)

    # def derivative(self, error, time_interval, variable):
    #     derivative_part = (error - self.previous_d_error[variable]) / time_interval
    #     self.previous_d_error[variable] = error
    #     derivative_controller = self.KD[variable] * derivative_part
    #     return self.__set_max(derivative_controller, self.min_error, self.max_error)

    def pi_controller(self, error, variable, interval=0.01):
        p = self.proportional(error, variable)
        # i = self.integral(error, interval, variable)
        # d = self.derivative(error, interval, variable)
        return p

    def output(self, distance_center, radius_curvature, run_time):
        try:
            # interval = run_time - self.previous_time
            # self.previous_time = run_time
            angle = self.p_controller(distance_center, 'angle')
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
