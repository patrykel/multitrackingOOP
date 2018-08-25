from multitracking.track_dataframes.TrackDfProviderUtility import *
from dataframes.DfUtility import *


class HonzaLinesDfUtility:

    @staticmethod
    def get_honza_column_names():
        return ['Event', 'Group', 'RP', 'x', 'y', 'z', 'dx', 'dy', 'dz',
                'dx2+dy2+dz2', 'dx/dz angle [mili rad]', 'dy/dz angle [mili rad]']

    @staticmethod
    def get_honza_data_2D(hansa_solution_lines, event_id, group_id):
        honza_data_2D = []

        for line in hansa_solution_lines:
            dx_dz_angle = TrackProviderDfUtility.get_mili_rad_angle(line.dx, line.dz)
            dy_dz_angle = TrackProviderDfUtility.get_mili_rad_angle(line.dy, line.dz)
            group = TrackProviderDfUtility.get_group_name(group_id)

            line_data = [event_id, group, int(line.silicon_id / 10),
                         line.x, line.y, line.z,
                         "{:.10f}".format(line.dx), "{:.10f}".format(line.dy), "{:.10f}".format(line.dz),
                         line.dx ** 2 + line.dy ** 2 + line.dz ** 2,
                         dx_dz_angle, dy_dz_angle]

            honza_data_2D.append(line_data)

        return honza_data_2D

    @staticmethod
    def get_honza_next_group_dfs(honza_solution_lines, event_id, group_id):
        data_2d = HonzaLinesDfUtility.get_honza_data_2D(honza_solution_lines, event_id, group_id)
        column_names = HonzaLinesDfUtility.get_honza_column_names()
        return DfUtility.get_df(data_2d, column_names)