from geometry_classes.Line import *
from geometry_classes.RPSiliconInclusionTest import *

import numpy as np

SIGMA = 0.0659 / np.sqrt(2)

DETECTOR_GROUP_MAP = {
    1 : "L-TOP",
    2 : "L-BOT",
    3 : "L-HOR",
    4 : "R-TOP",
    5 : "R-BOT",
    6 : "R-HOR"
}

class TrackProviderDfUtility:

    @staticmethod
    def get_group_name(group_id):
        return DETECTOR_GROUP_MAP[group_id]

    # DISTANCES
    @staticmethod
    def get_distances(solution, hit_lines):
        track = Line(params=solution.x)
        return [track.distance(line) for line in hit_lines]

    @staticmethod
    def get_dist_sum(solution, hit_lines):
        distances = TrackProviderDfUtility.get_distances(solution, hit_lines)
        return sum(distances)

    @staticmethod
    def get_dist_max(solution, hit_lines):
        distances = TrackProviderDfUtility.get_distances(solution, hit_lines)
        return max(distances)

    # CHI_2
    @staticmethod
    def get_chi2(solution, hit_lines):
        track = Line(params=solution.x)  # CREATING FITTED TRACK
        return sum([(track.distance(hit_line) / SIGMA) ** 2 for hit_line in hit_lines])  # SUM OF DISTANCES

    @staticmethod
    def get_chi2_N(solution, hit_lines):
        return TrackProviderDfUtility.get_chi2(solution, hit_lines) / (len(hit_lines) - len(solution.x))

    # TRACK PARAMS
    @staticmethod
    def get_track_params(solution):
        x, y, z, dx, dy, dz = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        if len(solution.x) == 5:
            x, y, dx, dy, dz = solution.x
        elif len(solution.x) == 6:
            x, y, z, dx, dy, dz = solution.x

        return [x, y, z, dx, dy, dz]

    # ATAN
    @staticmethod
    def get_mili_rad_angle(da, dz):
        return 1000 * np.arctan(da / dz)

    # INSIDE SILICON TEST
    @staticmethod
    def get_silicon_id_list(hit_lines):
        return [line.silicon_id for line in hit_lines]

    @staticmethod
    def get_det_with_track_list(silicon_id_list, track_line):
        return [silicon_id for silicon_id in silicon_id_list
                if RPSiliconInclusionTest.det_contains_track(silicon_id, track_line)]

    @staticmethod
    def get_tracks_in_det_no(solution, hit_lines):
        track_line = Line(params=solution.x)
        silicon_id_list = TrackProviderDfUtility.get_silicon_id_list(hit_lines)
        det_with_track = TrackProviderDfUtility.get_det_with_track_list(silicon_id_list, track_line)

        return len(det_with_track)
