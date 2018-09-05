from multitracking.algorithm.Combinatorics import *
from multitracking.algorithm.MultitrackingAlgorithm import MultitrackingAlgorithm
from multitracking.algorithm.OptimizationConfig import *
from multitracking.algorithm.HitLinesProvider import *
from multitracking.algorithm.SolutionNormalizator import *
from multitracking.track_dataframes.TrackRecord import *
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

            group_hits = self.get_group_hits(event_id, group_id)

            if this_is_multitrack(group_hits):
                print("event: {} group: {} MULTI".format(event_id, group_id))
                self.run_multitrack(event_id, group_id)
            else:
                print("event: {} group: {} SINGLE".format(event_id, group_id))
                self.run_single_track(event_id, group_id)

            track_record = self.compute_track_record(event_id, group_id)
            self.track_df_provider.add_track_df_row(track_record, HIT_LINES)

    def get_group_hits(self, event_id, group_id):
        return self.multitrack_df[(self.multitrack_df['eventID'] == event_id) &
                                  (self.multitrack_df['groupID'] == group_id)]

    def run_multitrack(self, event_id, group_id):
        '''
        DATA PREPARATION
        {
            rp_id {
                u_direction {
                    line_no : [hit_lines]
                }
            }
        }
        '''
        multi_lines_dict = self.hit_lines_provider.provide_multitrack_lines_dict(event_id, group_id)
        if len(list(multi_lines_dict)) < 3:
            print("To few RPs... 3 required :(")

        # COMBINATORICS
        fishing_rp, fitting_rps = get_fishing_fitting_rps(multi_lines_dict)
        combinations = get_combinations(fitting_rps, multi_lines_dict):

        # FITTING

        '''
        Here I want:
            - for each combination from combinations:
                - get lines to fit track to
                - fit track
                - store result (scipy.optimize.least_squares.solution)
        '''

        # FISHING

        '''
        Assume we have rp 125 with following combinations:
            [(125, 'u', 0), (125, 'v', 0)]
            [(125, 'u', 0), (125, 'v', 1)]
            [(125, 'u', 1), (125, 'v', 0)]
            [(125, 'u', 1), (125, 'v', 1)]

        and rp 105 with following combinations:
            [(105, 'u', 0), (105, 'v', 0)]
            [(105, 'u', 0), (105, 'v', 1)]
            [(105, 'u', 0), (105, 'v', 2)]
            [(105, 'u', 1), (105, 'v', 0)]
            [(105, 'u', 1), (105, 'v', 1)]
            [(105, 'u', 1), (105, 'v', 2)]

        For each combination of rp125 and rp105 we store solution of fitting
        Now,
        Choose for each combination in rp125 choose one from rp105 where fitting gave best result ---> we will have 4 potential tracks

        Do fishing in rp 121 (3rd one)

            Two ways:
               1. Count points of intersection of u v lines. Set threshold where should track pass crossing point.
               2.  Count best fitting :)
        '''

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







