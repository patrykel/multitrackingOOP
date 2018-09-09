from multitracking.algorithm.Combinatorics import *
from multitracking.algorithm.Fitting import *
from multitracking.algorithm.Fishing import *
from multitracking.algorithm.MultitrackingAlgorithm import MultitrackingAlgorithm
from multitracking.algorithm.OptimizationConfig import *
from multitracking.algorithm.HitLinesProvider import *
from multitracking.algorithm.SolutionNormalizator import *
from multitracking.track_dataframes.TrackDfProvider import *
from dataframes.DfRepositoryProvider import *
from dataframes.Configuration import *
from scipy.optimize import least_squares
import time


class LeastSquaresMultitrackingAlgorithm(MultitrackingAlgorithm):

    def __init__(self):
        self.df_repository = DfRepositoryProvider.provide()
        self.hit_lines_provider = HitLinesProvider()
        self.track_df_provider = TrackDfProvider.get_track_df_provider()
        self.multitrack_df = self.df_repository.get(Configuration.MULTI_TRACK_DF)
        self.setup_event_group_list()

    def setup_event_group_list(self):
        self.event_group_list = []
        for event_id in self.multitrack_df.eventID.unique():
            event_df = self.multitrack_df.loc[(self.multitrack_df['eventID'] == event_id)]
            for group_id in event_df.groupID.unique():
                self.event_group_list.append(tuple([event_id, group_id]))




    def run(self):
        for event_id, group_id in self.event_group_list:
            # if event_id > 5:
            #     break

            group_df = self.get_group_hits(event_id, group_id)  # THESE WILL BE TAKEN ALL FOR RECONSTRUCTION
            # OK DOLINO MUMINKOW...
            # JEZELI CHCEMY TUTAJ SIE BAWIC TO NAJPIERW USTAWIAMY
            self.set_lowest_abs_silicon_z_mm(group_df)


            if this_is_multitrack(group_df):
                print("event: {} group: {} MULTI".format(event_id, group_id, group_df))
                self.run_multitrack(event_id, group_id, group_df)
            else:
                print("event: {} group: {} SINGLE".format(event_id, group_id))
                self.run_single_track(event_id, group_id)

            track_record = self.compute_track_record(event_id, group_id)
            self.track_df_provider.add_track_df_row(track_record, HIT_LINES)

    def get_group_hits(self, event_id, group_id):
        group_df =  self.multitrack_df[(self.multitrack_df['eventID'] == event_id) &
                                       (self.multitrack_df['groupID'] == group_id)]
        # Remove lines which have very different position (HEURISTIC :))
        idxs_to_drop = get_idxs_to_drop(group_df)
        return group_df.drop(idxs_to_drop)

    def run_multitrack(self, event_id, group_id, group_df):


        '''
        multi_lines_dict
        {
            rp_id {
                u_direction {
                    line_no : [hit_lines]
                }
            }
        }
        '''
        # Ok we need to get better lines  --> investigate it.. Be couragous
        multi_lines_dict = self.hit_lines_provider.provide_multitrack_lines_dict(event_id, group_id, group_df)
        if len(list(multi_lines_dict)) < 3:
            print("To few RPs... 3 required :(")

        # COMBINATORICS
        fishing_rp, fitting_rps = get_fishing_fitting_rps(multi_lines_dict)
        combinations = get_combinations(fitting_rps, multi_lines_dict)
        '''
        Combinations:
        [(125, 'u', 0), (125, 'v', 0), (105, 'u', 0), (105, 'v', 0)]
        ...
        [(125, 'u', 0), (125, 'v', 0), (105, 'u', 0), (105, 'v', 1)]
        '''

        # FITTING
        multi_track_records = []
        for combination in combinations:
            multi_track_record = compute_track_record(event_id, group_id, combination, multi_lines_dict)
            multi_track_records.append(multi_track_record)

        '''
        Multitrack records:
        [MultiTrackRecord(event_id, group_id, combination, hit_lines, solution, method, exec_time)]
        '''

        ###############################################
        # REMEMBER TO DO TRACK AND HITS NORMALIZATION #
        ###############################################

        # FISHING

        # Decide which multitrack to decline (Optional)
        fishing_dictionary = create_fishing_dictionary(fishing_rp, multi_track_records, multi_lines_dict)

        '''
        fishing dictionary
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

    def set_lowest_abs_silicon_z_mm(self, group_df):
        lowest_silicon_id = get_lowest_silicon_id(group_df)
        geom_silicon_df = self.df_repository.get(Configuration.GEOM_SILICON_DF)
        silicon_info = geom_silicon_df[(geom_silicon_df['detId'] == lowest_silicon_id)].iloc[0]
        HitLinesProviderConfig.LOWEST_ABS_SILICON_Z_MM = silicon_info['z'] * 1000

    def compute_track_record(self, event_id, group_id):
        global HIT_LINES
        HIT_LINES = self.hit_lines_provider.provide(event_id, group_id)
        arm_id = get_arm_id()

        minimize_methods = OptimizationConfig.get_minimize_methods()
        x0 = OptimizationConfig.get_x0(arm_id)
        bounds = OptimizationConfig.get_least_squares_bounds()

        solution, method, exec_time = compute_solution_track(x0, bounds)

        # Normalize solution track and hit lines to come back to real coordinate system (not translated)
        SolutionNormalizator.normalize(solution)  # normalize vector, move solution x,y to z = lowest_det_z
        self.hit_lines_provider.normalize(HIT_LINES)

        return TrackRecord(event_id, group_id, solution, method, exec_time)


HIT_LINES = []


def get_arm_id():
    return int(HIT_LINES[0].silicon_id / 1000)


def objective(params):
    x, y, dx, dy, dz = params
    line = Line(x=x, y=y, dx=dx, dy=dy, dz=dz)  # Assume z = 0
    return np.sum([line.distance(other) for other in HIT_LINES])  # Sum of distances


def compute_solution_track(x0, bounds):
    method = 'trf (least squares method)'

    start_time = time.time()
    solution = least_squares(objective, x0, bounds=bounds, jac='2-point', method='trf')
    exec_time = time.time() - start_time

    return solution, method, exec_time


##################
# MULTI TRACKING #
##################
def this_is_multitrack(group_hits):
    multi_df = group_hits.loc[(group_hits['uLineNo'] > 1) | (group_hits['vLineNo'] > 1)]
    return multi_df.size > 0


def get_idxs_to_drop(group_df):
    idxs_to_drop = []
    for rp_id in group_df.rpID.unique():
        rp_df = group_df.loc[group_df['rpID'] == rp_id]
        for direction in rp_df.direction.unique():
            direction_df = rp_df.loc[rp_df['direction'] == direction]
            for line_no in direction_df.line_no.unique():
                line_df = direction_df.loc[direction_df['line_no'] == line_no]

                max_position = line_df.position.max()
                min_position = line_df.position.min()

                if (max_position - min_position > 1.0):
                    idxs_to_drop = idxs_to_drop + line_df.index.tolist()

    return idxs_to_drop


def get_lowest_silicon_id(group_df):
    min_rp_id = group_df.rpID.min()
    rp_df = group_df[(group_df['rpID'] == min_rp_id)]
    min_silicon_id = rp_df.siliconID.min()

    return min_rp_id * 10 + min_silicon_id
