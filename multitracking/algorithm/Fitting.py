from geometry_classes.Line import *
from multitracking.algorithm.OptimizationConfig import *
from multitracking.track_dataframes.MultiTrackRecord import *
from scipy.optimize import least_squares
import time

HIT_LINES = []


def get_arm_id():
    return int(HIT_LINES[0].silicon_id / 1000)


def objective(params):
    x, y, dx, dy, dz = params
    line = Line(x=x, y=y, dx=dx, dy=dy, dz=dz)  # Assume z = 0
    return np.sum([line.distance(other) for other in HIT_LINES])  # Sum of distances


def compute_solution_track(x0, bounds):
    method = 'trf (least squares method)'

    start_time = time.time()
    solution = least_squares(objective, x0, bounds=bounds, jac='2-point', method='trf')
    exec_time = time.time() - start_time

    return solution, method, exec_time


def get_hit_lines(combination, multi_lines_dict):
    hit_lines = []
    for rp_tuple in combination:
        rp_id, direction, line_no = rp_tuple
        hit_lines = hit_lines + multi_lines_dict[rp_id][direction][line_no]

    return hit_lines


def compute_track_record(event_id, group_id, combination, multi_lines_dict):
    hit_lines = get_hit_lines(combination, multi_lines_dict)

    global HIT_LINES
    HIT_LINES = hit_lines

    arm_id = get_arm_id()

    minimize_methods = OptimizationConfig.get_minimize_methods()
    x0 = OptimizationConfig.get_x0(arm_id)
    bounds = OptimizationConfig.get_least_squares_bounds()

    solution, method, exec_time = compute_solution_track(x0, bounds)

    return MultiTrackRecord(event_id, group_id, combination, hit_lines, solution, method, exec_time)