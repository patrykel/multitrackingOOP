from dataframes.DfRepositoryProvider import *
from dataframes.Configuration import *
from geometry_classes.Line import *
from multitracking.algorithm.HitLinesProviderConfig import *

'''
Main task:
    INPUT: HIT_LINES_SINGLE_3RP_DF
    OUTPUT: Lines in Global Coordinate System, representing hits.
'''

U_DIRECTION = 'u'
V_DIRECTION = 'v'


class HitLinesProvider:
    # TODO: Make these can be two modes --> simply use other all_hit_lines_df
    SINGLE_TRACKING_MODE = "single"
    MULTI_TRACKING_MODE = "multi"

    def __init__(self):
        self.df_repository = DfRepositoryProvider.provide()

        self.all_hit_lines_df = self.df_repository.get(Configuration.HIT_LINES_DF)
        self.multi_track_df = self.df_repository.get(Configuration.MULTI_TRACK_DF)
        self.geom_silicon_df = self.df_repository.get(Configuration.GEOM_SILICON_DF)

    ##################
    # MULTI TRACKING #
    ##################
    def provide_multitrack_lines_dict(self, event_id, group_id, group_df):
        current_multi_hits_df = group_df
        hit_lines_dict = self.create_hit_lines_dict(current_multi_hits_df)
        self.apply_dict_lines_transformations(hit_lines_dict)
        return hit_lines_dict

    def lines_dictionary(self, rp_id, direction, group_hits_df):
        rp_dir_hits_df = group_hits_df.loc[(group_hits_df['rpID'] == rp_id) & (group_hits_df['direction'] == direction)]

        rp_lines_dict = {}
        for line_no in rp_dir_hits_df.line_no.unique():
            rp_lines_dict[line_no] = []

        for i, hit_info in rp_dir_hits_df.iterrows():
            silicon_id = hit_info['rpID'] * 10 + hit_info['siliconID'] # watch out - it is only the last digit -- we need to append rpID
            silicon_info = self.extract_silicon_info(silicon_id)

            line_no = hit_info['line_no']
            hit_position = hit_info['position']

            next_line = compute_line(hit_position, silicon_id, silicon_info)
            rp_lines_dict[line_no].append(next_line)

        return rp_lines_dict

    def create_hit_lines_dict(self, group_hits_df):
        '''
        :param group_hits_df: multitrack hits for given event_id, group_id
        :return: dictionary:
        {
            rp_id {
                u_direction {
                    line_no : [lines]
                }
            }
        }
        '''
        lines_dict = {}
        for rp_id in group_hits_df.rpID.unique():
            lines_dict[rp_id] = {}
            lines_dict[rp_id][U_DIRECTION] = self.lines_dictionary(rp_id, U_DIRECTION, group_hits_df)
            lines_dict[rp_id][V_DIRECTION] = self.lines_dictionary(rp_id, V_DIRECTION, group_hits_df)

        return lines_dict

    def apply_dict_lines_transformations(self, lines_dict):
        for rp_id in lines_dict:
            for direction in lines_dict[rp_id]:
                for line_no in lines_dict[rp_id][direction]:
                    self.apply_transformations(lines_dict[rp_id][direction][line_no])

    ###################
    # SINGLE TRACKING #
    ###################
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
            hit_position = hit_info['position']

            next_line = compute_line(hit_position, silicon_id, silicon_info)
            lines.append(next_line)

        return lines

    def extract_silicon_info(self, det_id):
        return self.geom_silicon_df[(self.geom_silicon_df['detId'] == det_id)].iloc[0]

    def apply_transformations(self, hit_lines):
        if HitLinesProviderConfig.LINES_IN_MM:
            for line in hit_lines:
                line.z = line.z * 1000

        if HitLinesProviderConfig.TRANSLATE_LINES:
            for line in hit_lines:
                line.z = line.z - HitLinesProviderConfig.LOWEST_ABS_SILICON_Z_MM
                line.z = line.z + HitLinesProviderConfig.ADDITIONAL_TRANSLATION * \
                                  np.sign(HitLinesProviderConfig.LOWEST_ABS_SILICON_Z_MM)  # +/- 1

    def normalize(self, hit_lines):
        # For each hit_line, set z = line's related silicon z coordinate (in mm)
        for line in hit_lines:
            silicon_info = self.extract_silicon_info(line.silicon_id)
            line.z = hit_line_z(silicon_info) * 1000


def compute_line(hit_position, silicon_id, silicon_info):
    x = hit_line_x(hit_position, silicon_info)
    y = hit_line_y(hit_position, silicon_info)
    z = hit_line_z(silicon_info)
    dx = hit_line_dx(silicon_info)
    dy = hit_line_dy(silicon_info)
    dz = hit_line_dz()

    return Line(x, y, z, dx, dy, dz, silicon_id=silicon_id)


def compute_silicon_id(hit_info):
    return 10 * hit_info['rpID'] + hit_info['siliconID']


def hit_line_x(hit_position, silicon_info):
    return silicon_info['x'] + hit_position * silicon_info['dx']


def hit_line_y(hit_position, silicon_info):
    return silicon_info['y'] + hit_position * silicon_info['dy']


def hit_line_z(silicon_info):
    return silicon_info['z']


def hit_line_dx(silicon_info):
    return - silicon_info['dy']


def hit_line_dy(silicon_info):
    return silicon_info['dx']


def hit_line_dz():
    return 0.0
