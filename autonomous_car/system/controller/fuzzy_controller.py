import skfuzzy as fuzzy
import numpy as np
from skfuzzy import control as ctrl


class FuzzyController:

    def __init__(self):
        # Auto-membership functions
        self.distance = self.__auto_membership_distance()
        self.angle = self.__auto_membership_angle()
        self.radius_curvature = self.__auto_membership_radius_curvature()
        self.speed = self.__auto_membership_speed()
        # Control System
        self.angle_control_system = self.__angle_rules(self.distance, self.angle)
        self.speed_control_system = self.__speed_rules(self.radius_curvature, self.speed)

    @staticmethod
    def __auto_membership_distance():
        distance = ctrl.Antecedent(np.arange(0, 0.5, 0.001), 'distance')
        distance['center'] = fuzzy.pimf(distance.universe, 0, 0.01, 0.02, 0.03)
        distance['low_dist'] = fuzzy.pimf(distance.universe, 0.02, 0.03, 0.05, 0.1)
        distance['medium_dist'] = fuzzy.trimf(distance.universe, [0.039, 0.10, 0.2])
        distance['high_dist'] = fuzzy.pimf(distance.universe, 0.15, 0.2, 0.4, 0.5)
        return distance

    @staticmethod
    def __auto_membership_angle():
        angle = ctrl.Consequent(np.arange(0, 45, 1), 'angle')
        angle['zero'] = fuzzy.pimf(angle.universe, 0, 2, 5, 7)
        angle['low'] = fuzzy.trimf(angle.universe, [3, 10, 25])
        angle['medium'] = fuzzy.trimf(angle.universe, [15, 25, 35])
        angle['high'] = fuzzy.trimf(angle.universe, [25, 35, 45])
        return angle

    @staticmethod
    def __angle_rules(distance, angle):
        rules = ctrl.ControlSystem([ctrl.Rule(distance['center'], angle['zero']),
                                   ctrl.Rule(distance['low_dist'], angle['low']),
                                   ctrl.Rule(distance['medium_dist'], angle['medium']),
                                   ctrl.Rule(distance['high_dist'], angle['high'])])
        control_system = ctrl.ControlSystemSimulation(rules)
        return control_system

    @staticmethod
    def __auto_membership_radius_curvature():
        radius_curvature = ctrl.Antecedent(np.arange(-1, 201, 1), 'radius_curvature')
        radius_curvature['low_r_curv'] = fuzzy.pimf(radius_curvature.universe, -1, 3, 8, 10)
        radius_curvature['medium_r_curv'] = fuzzy.pimf(radius_curvature.universe, 5, 30, 80, 130)
        radius_curvature['high_r_curv'] = fuzzy.pimf(radius_curvature.universe, 100, 130, 170, 201)
        return radius_curvature

    @staticmethod
    def __auto_membership_speed():
        speed = ctrl.Consequent(np.arange(25, 75, 1), 'speed')
        speed['low'] = fuzzy.pimf(speed.universe, 25, 32, 35, 45)
        speed['medium'] = fuzzy.pimf(speed.universe, 40, 45, 50, 54)
        speed['high'] = fuzzy.pimf(speed.universe, 48, 57, 65, 75)
        return speed

    @staticmethod
    def __speed_rules(radius_curvature, speed):
        rules = ctrl.ControlSystem([ctrl.Rule(radius_curvature['high_r_curv'], speed['high']),
                                    ctrl.Rule(radius_curvature['medium_r_curv'], speed['medium']),
                                    ctrl.Rule(radius_curvature['low_r_curv'], speed['low'])])
        control_system = ctrl.ControlSystemSimulation(rules)
        return control_system

    def output(self, distance_center, radius_curvature):
        try:
            self.angle_control_system.input['distance'] = abs(distance_center)
            self.angle_control_system.compute()
            self.speed_control_system.input['radius_curvature'] = abs(radius_curvature)
            self.speed_control_system.compute()
            angle = self.angle_control_system.output['angle']
            speed = self.speed_control_system.output['speed']
            if distance_center < 0:
                angle = - angle
            return speed, angle
        except Exception as e:
            print str(e)
            return 0, 0
