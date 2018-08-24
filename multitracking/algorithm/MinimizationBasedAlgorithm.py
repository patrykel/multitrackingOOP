from multitracking.algorithm.MultitrackingAlgorithm import MultitrackingAlgorithm
from multitracking.algorithm.HitLinesProvider import *
from dataframes.DfRepositoryProvider import *
from dataframes.Configuration import *

class MinimizationBasedAlgorithm(MultitrackingAlgorithm):
    # Jego zadanie:
    # Input: ...
    # Output: SolutionRecordList

    def __init__(self):
        self.df_repository = DfRepositoryProvider.provide()
        self.hit_lines_provider = HitLinesProvider()
        self.event_group_list = self.setup_event_group_list()
        self.track_record_list = []

    def setup_event_group_list(self):
        self.event_group_list = []
        single_uv_lines_df = self.df_repository.get(Configuration.SINGLE_HITS_3RP_DF)

        for index, row in single_uv_lines_df.iterrows():
            event_id, group_id = row['eventID'], row['groupID']
            self.event_group_list.append(tuple([eventID, groupID]))

    def run(self):
        for event, group in self.event_group_list:
            track_record = self.compute_track_record(event_id, group_id)
            self.trackRecordList.append(track_record)

    def compute_track_record(self, event_id, group_id):
        hit_lines_df = HitLinesProvider.provide(event_id, group_id)