import skfuzzy as fuzzy
import numpy as np
from skfuzzy import control as ctrl


class FuzzyController:

    def __init__(self):
        # Auto-membership function: Distance
        self._distance = ctrl.Antecedent(np.arange(0, 0.5, 0.001), 'distance')
        self.__auto_membership_distance()
        # Auto-membership function: Angle
        self._angle = ctrl.Consequent(np.arange(0, 0.45, 0.01), 'angle')
        self.__auto_membership_angle()
        self._angle_LF = ctrl.ControlSystemSimulation(self.__angle_rules())

    def __auto_membership_distance(self):
        self._distance['center'] = fuzzy.pimf(self._distance.universe, 0, 0.01, 0.02, 0.04)
        self._distance['low_dist'] = fuzzy.trimf(self._distance.universe, [0.02, 0.05, 0.1])
        self._distance['medium_dist'] = fuzzy.trimf(self._distance.universe, [0.05, 0.10, 0.2])
        self._distance['high_dist'] = fuzzy.pimf(self._distance.universe, 0.15, 0.2, 0.4, 0.5)

    def __auto_membership_angle(self):
        self._angle['zero'] = fuzzy.pimf(self._angle.universe, 0, 0.02, 0.05, 0.07)
        self._angle['low'] = fuzzy.trimf(self._angle.universe, [0.03, 0.1, 0.25])
        self._angle['medium'] = fuzzy.trimf(self._angle.universe, [0.15, 0.25, 0.35])
        self._angle['high'] = fuzzy.trimf(self._angle.universe, [0.25, 0.35, 0.45])

    def __angle_rules(self):
        angle_rules = []
        angle_rules.append(ctrl.Rule(self._distance['center'], self._angle['zero']))
        angle_rules.append(ctrl.Rule(self._distance['low_dist'], self._angle['low']))
        angle_rules.append(ctrl.Rule(self._distance['medium_dist'], self._angle['medium']))
        angle_rules.append(ctrl.Rule(self._distance['high_dist'], self._angle['high']))
        return angle_rules

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
