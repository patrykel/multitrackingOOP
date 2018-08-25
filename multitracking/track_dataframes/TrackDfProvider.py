from multitracking.algorithm.HitLinesProviderConfig import *
from multitracking.track_dataframes.TrackDfProviderUtility import *
from multitracking.track_dataframes.TrackRecord import *

import pandas as pd

class TrackDfProvider:
    # It is done to take set of solution records and to create beautiful dataframe :)

    @staticmethod
    def get_track_df_provider():
        return track_df_provider_singleton

    def __init__(self):
        self.track_df_rows = []

    def provide(self):
        return pd.concat(self.track_df_rows, ignore_index=True)

    def add_track_df_row(self, track_record, hit_lines):
        solution            = track_record.solution

        event_id            = track_record.event_id
        group_id            = TrackProviderDfUtility.get_group_name(track_record.group_id)
        method              = track_record.method
        exec_time_ms        = track_record.exec_time_ms
        dist_max            = TrackProviderDfUtility.get_dist_max(solution, hit_lines)
        dist_sum            = TrackProviderDfUtility.get_dist_sum(solution, hit_lines)
        chi2                = TrackProviderDfUtility.get_chi2(solution, hit_lines)
        chi2_N              = TrackProviderDfUtility.get_chi2_N(solution, hit_lines)
        x, y, z, dx, dy, dz = TrackProviderDfUtility.get_track_params(solution)
        dx_dz_angle         = TrackProviderDfUtility.get_mili_rad_angle(dx, dz)
        dy_dz_angle         = TrackProviderDfUtility.get_mili_rad_angle(dy, dz)
        tracks_in_det_no    = TrackProviderDfUtility.get_tracks_in_det_no(solution, hit_lines)
        tracks_out_det_no   = len(hit_lines) - tracks_in_det_no

        track_data = [HitLinesProviderConfig.ADDITIONAL_TRANSLATION,
                      event_id, group_id, method, exec_time_ms, dist_sum, dist_max, solution.success, chi2, chi2_N,
                      x, y, z,
                      "{:.10f}".format(dx), "{:.10f}".format(dy), "{:.10f}".format(dz),
                      dx ** 2 + dy ** 2 + dz ** 2, dx_dz_angle, dy_dz_angle,
                      tracks_in_det_no, tracks_out_det_no]

        track_df_row = get_row_df(track_data)
        self.track_df_rows.append(track_df_row)

# my singleton
track_df_provider_singleton = TrackDfProvider()


def get_column_names():
    track_data_columns = ['Translate', 'Event', 'Group', 'Method', 'TIME', 'DistSum', 'MDH', 'Success', 'Chi', 'ChiN',
                        'x [mm]', 'y [mm]', 'z [mm]', 'dx', 'dy', 'dz',
                        'dx2+dy2+dz2', 'dx/dz angle [mili rad]', 'dy/dz angle [mili rad]',
                        'track_in_dets', 'track_out_dets']

    return track_data_columns


def get_row_data_dict(row_data):
    result = {}
    columns = get_column_names()

    for i, (key, val) in enumerate(zip(columns, row_data)):
        result[key] = [val]

    return result


def get_row_df(row_data):
    row_data_dict   = get_row_data_dict(row_data)
    columns         = get_column_names()

    return pd.DataFrame(row_data_dict, columns=columns)
