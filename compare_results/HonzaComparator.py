from geometry_classes.Line import *
from dataframes.DfUtility import *

import numpy as np

EVENT = 'Event'
GROUP = 'Group'
RP = 'RP'

class HonzaComparator:

    def __init__(self, multitrack_df, honza_lines_df):
        self.multitrack_df = multitrack_df
        self.honza_lines_df = honza_lines_df

    def get_compare_results_df(self):
        compare_data = []

        for idx, honza_row in self.honza_lines_df.iterrows():
            event_id = honza_row[EVENT]
            group_id = honza_row[GROUP]
            rp_id = honza_row[RP]

            print("event: {}, group: {}, rp: {}".format(event_id, group_id, rp_id))

            honza_x, honza_y, honza_z = self.get_honza_xyz(honza_row)

            multitrack_line = self.get_multitrack_line(honza_row)
            multitrack_x, multitrack_y = multitrack_line.xy_on_z(honza_z)

            x_diff = abs(honza_x - multitrack_x)
            y_diff = abs(honza_y - multitrack_y)

            hits_diff = np.sqrt(x_diff**2 + y_diff**2)

            compare_data.append([event_id, group_id, rp_id,
                                 honza_z, honza_x, multitrack_x, honza_y, multitrack_y,
                                 float(x_diff), float(y_diff), float(hits_diff)])

        return DfUtility.get_df(compare_data, self.compare_result_column_names())

    def compare_result_column_names(self):
        return ['Event', 'Group', 'RP',
                'rp z [mm]', 'honza_x [mm]', 'multitrack_x [mm]', 'honza_y [mm]', 'multitrack_y [mm]',
                'x_diff [mm]', 'y_diff [mm]', 'hits_diff [mm]']

    def get_honza_xyz(self, honza_row):
        x = honza_row['x']
        y = honza_row['y']
        z = honza_row['z']

        return x, y, z

    def get_multitrack_line(self, honza_row):
        event_id = honza_row[EVENT]
        group_id = honza_row[GROUP]

        multitrack_row = self.multitrack_df[(self.multitrack_df[EVENT] == event_id)
                                            & (self.multitrack_df[GROUP] == group_id)]

        x = float(multitrack_row['x [mm]'])
        y = float(multitrack_row['y [mm]'])
        z = float(multitrack_row['z [mm]'])
        dx = float(multitrack_row['dx'])
        dy = float(multitrack_row['dy'])
        dz = float(multitrack_row['dz'])

        return Line(x, y, z, dx, dy, dz)
