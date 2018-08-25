from dataframes.DfRepositoryProvider import *
from dataframes.Configuration import *
from geometry_classes.Line import *
from multitracking.algorithm.HitLinesProviderConfig import *
'''
Main task:
    INPUT: HIT_LINES_SINGLE_3RP_DF
    OUTPUT: Lines in Global Coordinate System, representing hits.
'''

class HitLinesProvider:

    # TODO: Make these can be two modes --> simply use other all_hit_lines_df
    SINGLE_TRACKING_MODE = "single"
    MULTI_TRACKING_MODE = "multi"

    def __init__(self):
        self.df_repository = DfRepositoryProvider.provide()

        self.all_hit_lines_df = self.df_repository.get(Configuration.HIT_LINES_DF)
        self.geom_silicon_df = self.df_repository.get(Configuration.GEOM_SILICON_DF)

    def provide(self, event_id, group_id):
        current_hits_df = self.extract_current_hits_df(event_id, group_id)
        hit_lines = self.create_lines(current_hits_df)
        self.apply_transformations(hit_lines)
        return hit_lines

    def extract_current_hits_df(self, event_id, group_id):
        return self.all_hit_lines_df[(self.all_hit_lines_df['eventID'] == event_id) &
                                     (self.all_hit_lines_df['groupID'] == group_id)]

    def create_lines(self, current_hits_df):
        lines = []

        for idx, hit_info in current_hits_df.iterrows():
            silicon_id = compute_silicon_id(hit_info)
            silicon_info = self.extract_silicon_info(silicon_id)

            x = hit_line_x(hit_info, silicon_info)
            y = hit_line_y(hit_info, silicon_info)
            z = hit_line_z(silicon_info)
            dx = hit_line_dx(silicon_info)
            dy = hit_line_dy(silicon_info)
            dz = hit_line_dz()

            lines.append(Line(x, y, z, dx, dy, dz, silicon_id=silicon_id))

        return lines

    def extract_silicon_info(self, det_id):
        return self.geom_silicon_df[(self.geom_silicon_df['detId'] == det_id)].iloc[0]

    def apply_transformations(self, hit_lines):
        if HitLinesProviderConfig.LINES_IN_MM:
            for line in hit_lines:
                line.z = line.z * 1000

        if HitLinesProviderConfig.TRANSLATE_LINES:
            set_lowest_abs_silicon_z(hit_lines)

            for line in hit_lines:
                line.z = line.z - HitLinesProviderConfig.LOWEST_ABS_SILICON_Z
                line.z = line.z + HitLinesProviderConfig.ADDITIONAL_TRANSLATION *\
                                  np.sign(HitLinesProviderConfig.LOWEST_ABS_SILICON_Z) # +/- 1


def compute_silicon_id(hit_info):
    return 10 * hit_info['rpID'] + hit_info['siliconID']


def hit_line_x(hit_info, silicon_info):
    return silicon_info['x'] + hit_info['position'] * silicon_info['dx']


def hit_line_y(hit_info, silicon_info):
    return silicon_info['y'] + hit_info['position'] * silicon_info['dy']


def hit_line_z(silicon_info):
    return silicon_info['z']


def hit_line_dx(silicon_info):
    return - silicon_info['dy']


def hit_line_dy(silicon_info):
    return silicon_info['dx']


def hit_line_dz():
    return 0.0


def set_lowest_abs_silicon_z(hit_lines):
    HitLinesProviderConfig.LOWEST_ABS_SILICON_Z = min([line.z for line in hit_lines], key=abs)
