'''
Mainly it is a dictionary:
{
    df_name : pd.Dataframe
}

DfNames can be find in dataframes.Configuration.py

Access by:
    get(df_name)
'''

import pandas as pd
from dataframes.Configuration import *


class DfRepository():
    def __init__(self):
        self.repository = {}
        self.setup_repository()

    def setup_repository(self):
        self.setup_from_files()
        self.setup_by_computing()

    def setup_from_files(self):
        for df_name in Configuration.get_df_files_names():
            filename = Configuration.get_filename(df_name)
            self.repository[df_name] = pd.read_csv(filename)

    def setup_by_computing(self):
        self.repository[Configuration.HIT_LINES_SINGLE_3RP_DF] = self.compute_hit_lines_single_3rp_df()

    def compute_hit_lines_single_3rp_df(self):
        hit_lines_df = self.repository[Configuration.HIT_LINES_DF]

        hit_lines_single_df = hit_lines_df[['eventID', 'groupID', 'rpID']] \
            .drop_duplicates() \
            .groupby(['eventID', 'groupID']) \
            .size() \
            .reset_index(name='counts')

        return hit_lines_single_df.loc[(hit_lines_single_df['counts'] == 3)]

    def get(self, df_name):
        return self.repository[df_name]
