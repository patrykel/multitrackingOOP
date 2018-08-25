from geometry_classes.Point3D import *

import math

V_DIRECTION = 'v'
U_DIRECTION = 'u'

DIRECTION_PARITY = {
    V_DIRECTION : 0,
    U_DIRECTION : 1
}

class UVCoordinateSystemSkeleton():
    def __init__(self):
        self.reset()

    def reset(self):
        # Line representing projections of Track to Uz and Vz planes
        self.line_u_a = None
        self.line_u_b0 = None
        self.line_v_a = None
        self.line_v_b0 = None

        # U|V Readout directions
        self.u_dx = None
        self.u_dy = None
        self.v_dx = None
        self.v_dy = None

        # Beginnings of Uz Vz coordinate systems
        self.z = None

        # Computed stuff
        self.line_u_b1 = None
        self.line_v_b1 = None
        self.pt0 = None
        self.pt1 = None

    def setup(self, rp_id, rp_hits_df, det_avg_geom_df, rp_geom_df):
        self.reset()
        self.setup_lines(rp_id, rp_hits_df)
        self.setup_directions(rp_id, det_avg_geom_df)
        self.setup_rp_z(rp_id, rp_geom_df)

        # compute
        self.compute_line_uv_b1()
        self.compute_pt0()
        self.compute_pt1()

    def setup_lines(self, rp_id, rp_hits_df):
        u_direction_row_df = rp_hits_df.loc[rp_hits_df['siliconID'] % 2 == DIRECTION_PARITY[U_DIRECTION]].iloc[0]
        v_direction_row_df = rp_hits_df.loc[rp_hits_df['siliconID'] % 2 == DIRECTION_PARITY[V_DIRECTION]].iloc[0]

        self.line_u_a = u_direction_row_df['uv_line_a']
        self.line_u_b0 = u_direction_row_df['uv_line_b']

        self.line_v_a = v_direction_row_df['uv_line_a']
        self.line_v_b0 = v_direction_row_df['uv_line_b']

    def setup_directions(self, rp_id, det_avg_geom_df):
        u_det_avg_df = det_avg_geom_df.loc[(det_avg_geom_df['rpId'] == rp_id) &
                                           (det_avg_geom_df['direction'] == U_DIRECTION)].iloc[0]

        v_det_avg_df = det_avg_geom_df.loc[(det_avg_geom_df['rpId'] == rp_id) &
                                           (det_avg_geom_df['direction'] == V_DIRECTION)].iloc[0]

        self.u_dx = u_det_avg_df['dx']
        self.u_dy = u_det_avg_df['dy']

        self.v_dx = v_det_avg_df['dx']
        self.v_dy = v_det_avg_df['dy']

    def setup_rp_z(self, rp_id, rp_geom_df):
        rp_row_df = rp_geom_df.loc[rp_geom_df['rpID'] == rp_id].iloc[0]
        self.rp_z = rp_row_df['z'] * 1000 # [mm]

    def compute_line_uv_b1(self):
        self.line_u_b1 = self.line_u_b0 + math.tan(self.line_u_a) * 1  # tangens while a is in [rad]
        self.line_v_b1 = self.line_v_b0 + math.tan(self.line_v_a) * 1  # check if angle is appropriate :)

    def compute_pt0(self):
        pt0_x = self.line_u_b0 * self.u_dx + self.line_v_b0 * self.v_dx
        pt0_y = self.line_u_b0 * self.u_dy + self.line_v_b0 * self.v_dy
        pt0_z = self.rp_z

        self.pt0 = Point3D(pt0_x, pt0_y, pt0_z)

    def compute_pt1(self):
        pt1_x = self.line_u_b1 * self.u_dx + self.line_v_b1 * self.v_dx
        pt1_y = self.line_u_b1 * self.u_dy + self.line_v_b1 * self.v_dy
        pt1_z = self.rp_z + 1

        self.pt1 = Point3D(pt1_x, pt1_y, pt1_z)

    def get_pt0(self):
        return self.pt0

    def get_pt1(self):
        return self.pt1
