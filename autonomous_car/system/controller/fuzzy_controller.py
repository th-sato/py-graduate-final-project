import skfuzzy as fuzzy
import numpy as np
from skfuzzy import control as ctrl


class FuzzyController:

    def __init__(self):
        # Auto-membership function: Distance
        self.distance = self.__auto_membership_distance()
        # Auto-membership function: Angle
        self.angle = self.__auto_membership_angle()
        self.angle_LF = self.__angle_rules(self.distance, self.angle)

    @staticmethod
    def __auto_membership_distance():
        distance = ctrl.Antecedent(np.arange(0, 0.5, 0.001), 'distance')
        distance['center'] = fuzzy.pimf(distance.universe, 0, 0.01, 0.02, 0.04)
        distance['low_dist'] = fuzzy.trimf(distance.universe, [0.02, 0.05, 0.1])
        distance['medium_dist'] = fuzzy.trimf(distance.universe, [0.05, 0.10, 0.2])
        distance['high_dist'] = fuzzy.pimf(distance.universe, 0.15, 0.2, 0.4, 0.5)
        return distance

    @staticmethod
    def __auto_membership_angle():
        angle = ctrl.Consequent(np.arange(0, 0.45, 0.01), 'angle')
        angle['zero'] = fuzzy.pimf(angle.universe, 0, 0.02, 0.05, 0.07)
        angle['low'] = fuzzy.trimf(angle.universe, [0.03, 0.1, 0.25])
        angle['medium'] = fuzzy.trimf(angle.universe, [0.15, 0.25, 0.35])
        angle['high'] = fuzzy.trimf(angle.universe, [0.25, 0.35, 0.45])
        return angle

    @staticmethod
    def __angle_rules(distance, angle):
        rules = ctrl.ControlSystem([ctrl.Rule(distance['center'], angle['zero']),
                                   ctrl.Rule(distance['low_dist'], angle['low']),
                                   ctrl.Rule(distance['medium_dist'], angle['medium']),
                                   ctrl.Rule(distance['high_dist'], angle['high'])])
        control_system = ctrl.ControlSystemSimulation(rules)
        return control_system

    def output(self, input_distance, curvature):
        try:
            speed = 40
            self.angle_LF.input['distance'] = abs(input_distance)
            self.angle_LF.compute()
            angle = self.angle_LF.output['angle']
            if input_distance < 0:
                angle = - angle
            return speed, angle * 100
        except Exception as e:
            print str(e)
            return 0, 0
