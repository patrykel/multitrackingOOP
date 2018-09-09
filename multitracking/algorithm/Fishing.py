from geometry_classes.Point3D import *
from geometry_classes.Line import *
from multitracking.math_utility.DeterminantsEquation2D import *

import numpy as np

V_DIRECTION = 'v'
U_DIRECTION = 'u'
FITTING_RESULT = 'FittingResult'

'''
:param multi_track_records: [MultiTrackRecord(event_id, group_id, combination, hit_lines, solution, method, exec_time)]

:param multi_lines_dict:
    {
        rp_id {
            u_direction {
                line_no : [hit_lines]
            }
        }
    }

:return: fishing_dicrionary:
{
    multi_track_record_idx:
    {
        'fit_result' : FittingResult,
        'u': {
                line_no : FittingResult (FittingResult tylko do hit_lines-ów z line_no)
            }
        'v' : {
                line_no : fitting_result (FittingResult tylko do hit_lines-ów z line_no)
            }
    }
}
'''


######################
# FISHING BY FITTING #
######################

class FittingResult:
    def __init__(self, objective_value, hit_lines, hit_lines_number):
        self.objective = objective_value
        self.hit_lines = hit_lines
        self.hit_lines_number = hit_lines_number
        self.avg_objective = objective_value / hit_lines_number


def create_fitting_result(multi_track_record):
    objective_value = multi_track_record.solution.fun
    hit_lines = multi_track_record.hit_lines
    hit_lines_number = len(hit_lines)

    return FittingResult(objective_value, hit_lines, hit_lines_number)


def create_lines_fit_dictionary(fishing_rp, multi_track_record, multi_lines_dict, direction):
    fittings_dictionary = {}

    for line_no in multi_lines_dict[fishing_rp][direction]:
        hit_lines = multi_lines_dict[fishing_rp][direction][line_no]
        objective_value = objective_fun(multi_track_record.solution.x, hit_lines)
        fitting_result = FittingResult(objective_value, hit_lines, len(hit_lines))

        fittings_dictionary[line_no] = fitting_result

    return fittings_dictionary


def create_fishing_dictionary(fishing_rp, multi_track_records, multi_lines_dict):
    fishing_dictionary = {}

    for track_idx in range(len(multi_track_records)):
        multi_track_record = multi_track_records[track_idx]

        fishing_dictionary[track_idx] = {}
        fishing_dictionary[track_idx][FITTING_RESULT] = create_fitting_result(multi_track_record)
        fishing_dictionary[track_idx][U_DIRECTION] = create_lines_fit_dictionary(fishing_rp, multi_track_record,
                                                                                 multi_lines_dict, U_DIRECTION)
        fishing_dictionary[track_idx][V_DIRECTION] = create_lines_fit_dictionary(fishing_rp, multi_track_record,
                                                                                 multi_lines_dict, V_DIRECTION)


def objective_fun(params, hit_lines):
    x, y, dx, dy, dz = params
    line = Line(x=x, y=y, dx=dx, dy=dy, dz=dz)  # Assume z = 0
    return np.sum([line.distance(other) for other in hit_lines])  # Sum of distances
