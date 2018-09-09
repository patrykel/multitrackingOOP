from geometry_classes.Point2D import Point2D
from geometry_classes.Direction2D import Direction2D
from geometry_classes.RPSilicon import RPSilicon
from dataframes.Configuration import *
from dataframes.DfRepositoryProvider import *
from multitracking.algorithm.HitLinesProviderConfig import *

import numpy as np

df_repository = DfRepositoryProvider.provide()


class RPSiliconInclusionTest:

    @staticmethod
    def det_contains_track(det_id, track_line):
        rp_silicon = get_rp_silicon(det_id)
        track_silicon_hit_point = get_track_silicon_hit_point(det_id, track_line)

        return rp_silicon.contains(track_silicon_hit_point)


# GETTING RP SILICON INSTANCE
def get_plane_info(det_id):
    geom_df = df_repository.get(Configuration.GEOM_SILICON_DF)
    return geom_df.loc[(geom_df['detId'] == det_id)].iloc[0]


def get_rp_silicon(det_id):
    plane_info = get_plane_info(det_id)
    plane_center = Point2D(x=plane_info['x'], y=plane_info['y'])
    plane_readout_direction = Direction2D(dx=plane_info['dx'], dy=plane_info['dy'])

    return RPSilicon(plane_center, plane_readout_direction, det_id)


# GETTING POINT WHERE SILICON WAS HIT BY TRACK
def get_det_z_translated(det_id):
    plane_info = get_plane_info(det_id)

    plane_z_mm = plane_info['z'] * 1000
    plane_z_translated = plane_z_mm - HitLinesProviderConfig.LOWEST_ABS_SILICON_Z_MM

    return plane_z_translated + HitLinesProviderConfig.ADDITIONAL_TRANSLATION * \
                                np.sign(HitLinesProviderConfig.LOWEST_ABS_SILICON_Z_MM)


def get_track_silicon_hit_point(det_id, track_line):
    # TODO: Change it so the track is already based in x,y,z at the first silicon Z :)

    '''
    Want to get point in which track is going through detector plane.

    :param det_id:
    :param track_line:
        x, y, z, dx, dy, dz

        0 < x << 1
        0 < y << 1
        0 = z
        0 <     dx  << 1
        0 <     dy  << 1
        0 <<    dz  <  1
    :param geom_df:
    :return:
    '''

    det_z_translated = get_det_z_translated(det_id)
    k = det_z_translated / track_line.dz

    p = Point2D()
    p.x = track_line.x + k * track_line.dx
    p.y = track_line.y + k * track_line.dy

    return p


