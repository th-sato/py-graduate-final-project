import skfuzzy as fuzzy
import numpy as np
from skfuzzy import control as ctrl


class FuzzyController:

    def __init__(self):
        # Auto-membership function: Distance
        self._distance = self.__auto_membership_distance()
        # Auto-membership function: Angle
        self._angle = self.__auto_membership_angle()
        self._angle_LF = self.__angle_rules(self._distance, self._angle)

    @staticmethod
    def __auto_membership_distance():
        distance = ctrl.Antecedent(np.arange(0, 10, 0.1), 'distance')
        distance['center'] = fuzzy.pimf(distance.universe, 0, 0.1, 1.0, 1.5)
        distance['low_dist'] = fuzzy.trimf(distance.universe, [1.0, 3.0, 5.0])
        distance['medium_dist'] = fuzzy.trimf(distance.universe, [4.0, 6.0, 8.0])
        distance['high_dist'] = fuzzy.pimf(distance.universe, 7.0, 8.0, 9.0, 10.0)
        return distance

    @staticmethod
    def __auto_membership_angle():
        angle = ctrl.Consequent(np.arange(0, 45, 1), 'angle')
        angle['zero'] = fuzzy.pimf(angle.universe, 0, 3, 5, 7)
        angle['low'] = fuzzy.trimf(angle.universe, [6, 13, 22])
        angle['medium'] = fuzzy.trimf(angle.universe, [20, 26, 32])
        angle['high'] = fuzzy.trimf(angle.universe, [30, 38, 45])
        return angle

    @staticmethod
    def __angle_rules(distance, angle):
        rules = ctrl.ControlSystem([ctrl.Rule(distance['center'], angle['zero']),
                                   ctrl.Rule(distance['low_dist'], angle['low']),
                                   ctrl.Rule(distance['medium_dist'], angle['medium']),
                                   ctrl.Rule(distance['high_dist'], angle['high'])])
        control_system = ctrl.ControlSystemSimulation(rules)
        return control_system

    @property
    def distance(self):
        return self._distance

    @property
    def angle(self):
        return self._angle

    @property
    def angle_lf(self):
        return self._angle_LF

    def output(self, input_distance, curvature):
        try:
            speed = 40
            self._angle_LF.input['distance'] = input_distance
            self._angle_LF.compute()
            angle = self._angle_LF.output['angle']
            return speed, angle
        except Exception as e:
            print str(e)
            return 40, 10
