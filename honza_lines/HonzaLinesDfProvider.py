from honza_lines.HonzaLinesDfUtility import *

import pandas as pd

class HonzaLinesDfProvider:

    @staticmethod
    def get_honza_lines_df_provider():
        return honza_lines_df_provider_singleton

    def __init__(self):
        self.honza_lines_df_rows = []


    def add_honza_lines(self, honza_lines, event_id, group_id):
        honza_next_group_df = HonzaLinesDfUtility.get_honza_next_group_dfs(honza_lines, event_id, group_id)
        self.honza_lines_df_rows.append(honza_next_group_df)

    def provide(self):
        return pd.concat(self.honza_lines_df_rows, ignore_index=True)


# my singleton
honza_lines_df_provider_singleton = HonzaLinesDfProvider()