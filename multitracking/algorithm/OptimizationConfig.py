import numpy as np

class OptimizationConfig:

    @staticmethod
    def get_x0(arm_id):
        x = 0.0  # plane_info['x']
        y = 0.0  # plane_info['y']
        dx = 0.009999749997
        dy = 0.009999749997

        if arm_id == 0:
            dz = -0.9999
        else:
            dz = 0.9999

        return [x, y, dx, dy, dz]

    @staticmethod
    def get_minimize_methods():
        return ['SLSQP', 'Nelder-Mead', 'Powell']

    @staticmethod
    def get_constraints():
        def constraint(params):
            return 1.0 - np.sum([di ** 2 for di in params[-3:]])  # dx^2 + dy^2 + dz^2 = 1 (params = [..., dx, dy, dz])

        con = {'type': 'eq', 'fun': constraint}
        return [con]

    @staticmethod
    def get_minimize_bounds():
        b_x = (-100.0, 100.0)   # We suppose that the track will begin in (x,y) ~ (0,0)
        b_y = (-100.0, 100.0)
        b_dir = (-1.0, 1.0)

        return [b_x, b_y, b_dir, b_dir, b_dir]

    @staticmethod
    def get_least_squares_bounds():
        minimize_bounds = OptimizationConfig.get_minimize_bounds()

        lower_bounds = []
        upper_bounds = []

        for bound in minimize_bounds:
            lower_bounds.append(bound[0])
            upper_bounds.append(bound[1])

        bounds = (lower_bounds, upper_bounds)

        return bounds
