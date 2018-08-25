from multitracking.algorithm.MultitrackingAlgorithm import MultitrackingAlgorithm
from multitracking.algorithm.OptimizationConfig import *
from multitracking.algorithm.HitLinesProvider import *
from multitracking.algorithm.SolutionNormalizator import *
from multitracking.track_dataframes.TrackRecord import *
from multitracking.track_dataframes.TrackDfProvider import *
from dataframes.DfRepositoryProvider import *
from dataframes.Configuration import *
from scipy.optimize import minimize
import time

class MinimizationBasedAlgorithm(MultitrackingAlgorithm):
    # Jego zadanie:
    # Input: ...
    # Output: TrackRecordList

    def __init__(self):
        self.df_repository = DfRepositoryProvider.provide()
        self.hit_lines_provider = HitLinesProvider()
        self.track_df_provider = TrackDfProvider.get_track_df_provider()
        self.setup_event_group_list()

    def setup_event_group_list(self):
        self.event_group_list = []
        single_uv_lines_df = self.df_repository.get(Configuration.HIT_LINES_SINGLE_3RP_DF)

        for index, row in single_uv_lines_df.iterrows():
            event_id, group_id = row['eventID'], row['groupID']
            self.event_group_list.append(tuple([event_id, group_id]))

    def run(self):
        for event_id, group_id in self.event_group_list:
            if event_id > 5:
                break

            print("event: {} group: {}".format(event_id, group_id))
            track_record = self.compute_track_record(event_id, group_id)
            self.track_df_provider.add_track_df_row(track_record, HIT_LINES)

    def compute_track_record(self, event_id, group_id):
        global HIT_LINES
        HIT_LINES = self.hit_lines_provider.provide(event_id, group_id)
        arm_id = get_arm_id()

        minimize_methods = OptimizationConfig.get_minimize_methods()
        x0 = OptimizationConfig.get_x0(arm_id)
        constraints = OptimizationConfig.get_constraints()
        bounds = OptimizationConfig.get_minimize_bounds()

        solution, method, exec_time = compute_solution_track(x0, constraints, bounds, minimize_methods)

        # Normalize solution track and hit lines to come back to real coordinate system (not translated)
        SolutionNormalizator.normalize(solution)    # normalize vector, move solution x,y to z = lowest_det_z
        self.hit_lines_provider.normalize(HIT_LINES)

        return TrackRecord(event_id, group_id, solution, method, exec_time)


HIT_LINES = []


def get_arm_id():
    return int(HIT_LINES[0].silicon_id / 1000)


def objective(params):
    x, y, dx, dy, dz = params
    line = Line(x=x, y=y, dx=dx, dy=dy, dz=dz)                    # Assume z = 0
    return np.sum([line.distance(other) for other in HIT_LINES])  # Sum of distances


def compute_solution_track(x0, constraints, bounds, minimize_methods):
    start_time = time.time()
    for method in minimize_methods:
        solution = minimize(objective, x0, method=method, constraints=constraints, bounds=bounds)

        if solution.success:
            break

    exec_time = time.time() - start_time

    return solution, method, exec_time