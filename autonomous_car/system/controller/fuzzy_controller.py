from skfuzzy import control as ctrl


class FuzzyController:
    NUM_RULES = 4

    def __init__(self):
        print "FuzzyController"
    #     self.set_distance()
    #     self.set_angle()
    #     self.set_rules()
    #     self.set_control()
    #
    # def set_distance(self):
    #     self.distances['center'] = 1
    #     self.distances['low_dist'] = 1
    #     self.distances['medium_dist'] = 1
    #     self.distances['high_dist'] = 1
    #
    # def set_angle(self):
    #     self.angles['zero'] = 1
    #     self.angles['low'] = 1
    #     self.angles['medium'] = 1
    #     self.angles['high'] = 1
    #
    # def set_rules(self):
    #     self.rules[FuzzyController.NUM_RULES] = ctrl.Rule(self.distances['center'], self.angles['zero'])
    #     self.rules[FuzzyController.NUM_RULES-1] = ctrl.Rule(self.distances['low_dist'], self.angles['low'])
    #     self.rules[FuzzyController.NUM_RULES-2] = ctrl.Rule(self.distances['medium_dist'], self.angles['medium'])
    #     self.rules[FuzzyController.NUM_RULES-3] = ctrl.Rule(self.distances['high_dist'], self.angles['high'])
    #
    # def set_control(self):
    #     self.angle_ctrl = ctrl.ControlSystem(self.rules)
    #     self.angle_LF = ctrl.ControlSystemSimulation(self.angle_ctrl)

    def teste(self):
        a = 1