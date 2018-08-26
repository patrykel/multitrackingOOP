from compare_results.HonzaComparator import *
from multitracking.algorithm.MinimizationBasedAlgorithm import *
from multitracking.algorithm.LeastSquaresBasedAlgorithm import *
from multitracking.track_dataframes.TrackDfProvider import *
from honza_lines.HonzaLinesProvider import *

import pandas as pd

# algorithm = MinimizationBasedAlgorithm()
algorithm = LeastSquaresBasedAlgorithm()

print("Running algorithm...")
algorithm.run()

tracks_df_provider = TrackDfProvider.get_track_df_provider()
track_df = tracks_df_provider.provide()

print("Computing honza lines...")
honza_lines_provider = HonzaLinesProvider()
honza_lines_provider.compute_all_event_lines()

honza_lines_df_provider = HonzaLinesDfProvider.get_honza_lines_df_provider()
honza_lines_df = honza_lines_df_provider.provide()

print("Comparing honza and multitrack_lines....")
honza_comparator = HonzaComparator(track_df, honza_lines_df)
compare_df = honza_comparator.get_compare_results_df()

compare_df.to_csv('compare_ALL_least_sqare_honza_df.csv')

print("The end")

'''
Now I want to compare differences between honza and my lines:
event_id, group_id, rp_id -->

Need to count what is
    x, y
on particular z --> on RP z
'''


