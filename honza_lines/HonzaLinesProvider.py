from dataframes.DfRepositoryProvider import *
from geometry_classes.Line import *
from honza_lines.HonzaLinesDfProvider import *
from honza_lines.UVCoordinateSystemSkeleton import *


class HonzaLinesProvider():

    def __init__(self):
        self.honza_lines_provider = HonzaLinesDfProvider.get_honza_lines_df_provider()
        self.df_repository = DfRepositoryProvider.provide()

        self.hits_df = self.df_repository.get(Configuration.HIT_LINES_DF)   # For now there are only single tracking
        self.det_avg_geom_df = self.df_repository.get(Configuration.AVG_DET_GEOM_DF)
        self.rp_geom_df = self.df_repository.get(Configuration.GEOM_RP_DF)

        self.uv_skeleton = UVCoordinateSystemSkeleton()

        self.setup_event_group_list()

    def setup_event_group_list(self):
        self.event_group_list = []
        single_uv_lines_df = self.df_repository.get(Configuration.HIT_LINES_SINGLE_3RP_DF)

        for index, row in single_uv_lines_df.iterrows():
            event_id, group_id = row['eventID'], row['groupID']
            self.event_group_list.append(tuple([event_id, group_id]))


    def compute_all_event_lines(self):
        for event_id, group_id in self.event_group_list:
            # if event_id > 5:
            #     break

            print("event: {} group: {}".format(event_id, group_id))
            honza_lines = self.compute_group_lines(event_id, group_id)
            self.honza_lines_provider.add_honza_lines(honza_lines, event_id, group_id)


    def compute_group_lines(self, event_id, group_id):
        hansa_lines = []
        group_hits_df = self.get_group_hits_df(event_id, group_id)
        rp_ids = self.get_rp_numbers(group_hits_df)

        for rp_id in rp_ids:
            rp_hits_df = self.get_rp_hits_df(rp_id, group_hits_df)
            hansa_lines.append(self.compute_line(rp_id, rp_hits_df))

        return hansa_lines

    def compute_line(self, rp_id, rp_hits_df):
        self.uv_skeleton.setup(rp_id, rp_hits_df, self.det_avg_geom_df, self.rp_geom_df)
        pt0 = self.uv_skeleton.get_pt0()
        pt1 = self.uv_skeleton.get_pt1()

        return Line(start=pt0, end=pt1, silicon_id=rp_id*10)


    # FOR EXTRACTING CURRENT (wrt. EventId, GroupId and RpId) HITS AND RP ID
    def get_rp_hits_df(self, rp_id, group_hits_df):
        return group_hits_df.loc[group_hits_df['rpID'] == rp_id]

    def get_group_hits_df(self, event_id, group_id):
        return self.hits_df.loc[(self.hits_df['eventID'] == event_id) &
                                (self.hits_df['groupID'] == group_id)]

    def get_rp_numbers(self, current_hits_df):
        return current_hits_df.rpID.unique().tolist()
