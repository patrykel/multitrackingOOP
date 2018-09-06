from geometry_classes.Point3D import *
from multitracking.math_utility.DeterminantsEquation2D import *

V_DIRECTION = 'v'
U_DIRECTION = 'u'

##################
# HIT CANDIDATES #
##################
def calculate_intersection(u_hit_line, v_hit_line):
    '''
    We compute c0 by crammers rule

    Given two lines:
    l1:  ( x1 ) + a ( u1)  // linia u       l2:  ( x2 ) + b ( u2)  // linia v
         ( y1 ) + a ( v1)                        ( y2 ) + b ( v2)

    [ u1  -u2] * [ a ] = [ x2 - x1 ]
    [ v1  -v2]   [ b ]   [ y2 - y1 ]

    COMPLY TO THAT:
    | a1 b1 | * | x | = | c1 |        -    x --> k_u
    | a2 b2 |   | y |   | c2 |        -    y --> k_v
    '''

    mapping = {
        'x1': u_hit_line.x, 'x2': v_hit_line.x,
        'y1': u_hit_line.y, 'y2': v_hit_line.y,
        'u1': u_hit_line.dx, 'u2': v_hit_line.dx,
        'v1': u_hit_line.dy, 'v2': v_hit_line.dy,
    }

    a1 = mapping['u1']
    b1 = - mapping['u2']
    c1 = mapping['x2'] - mapping['x1']

    a2 = mapping['v1']
    b2 = - mapping['v2']
    c2 = mapping['y2'] - mapping['y1']

    equation = DeterminantsEquation2D(a1, b1, c1, a2, b2, c2)
    k_u, k_v = equation.compute_solution()

    intersection_x = u_hit_line.x + k_u * u_hit_line.dx
    intersection_y = u_hit_line.y + k_u * u_hit_line.dy
    intersection_z = (u_hit_line.z + v_hit_line.z) / 2.0

    intersection = Point3D(
        intersection_x,
        intersection_y,
        intersection_z
    )

    return intersection


def calculate_hit_point_candidate(u_hits, v_hits):
    u_hit_line = u_hits[0]
    v_hit_line = v_hits[0]

    return calculate_intersection(u_hit_line, v_hit_line)


def get_hit_point_candidates(fishing_rp, multi_lines_dict):
    hit_point_candidates = []  # List of 3D points

    for u_line in multi_lines_dict[fishing_rp][U_DIRECTION]:
        for v_line in multi_lines_dict[fishing_rp][V_DIRECTION]:
            u_hits = multi_lines_dict[fishing_rp][U_DIRECTION][u_line]
            v_hits = multi_lines_dict[fishing_rp][V_DIRECTION][v_line]

            hit_point_candidate = calculate_hit_point_candidate(u_hits, v_hits)
            hit_point_candidates.append(hit_point_candidate)

    return hit_point_candidates

##################
#                #
##################

class FittingResult:
    def __init__(self, objective, hit_lines, hit_lines_number):
        self.objective = objective
        self.hit_line = hit_lines
        self.hit_lines_number = hit_lines_number
        self.avg_objective = objective / hit_lines_number

# def get_combination_avg_solution_dictionary(multi_track_records, multi_lines_dict):
#     combi_avg_solution_dictionary = {}
#
#     for multi_track_record in multi_track_records:
#         combination = multi_track_record.combination
#         hit_lines_number = 0
#
#         for combi_tuple in combination:
#             rp_id, direction, line_no = combi_tuple
#             hit_lines_number = hit_lines_number + len(multi_lines_dict[rp_id][direction][line_no])
#
#         avg_solution = multi_track_record.solution.fun / hit_lines_number
#
#         combi_avg_solution_dictionary[combination] = avg_solution
#
#     return combi_avg_solution_dictionary
