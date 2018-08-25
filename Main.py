
from multitracking.algorithm.MinimizationBasedAlgorithm import *
from multitracking.algorithm.LeastSquaresBasedAlgorithm import *
from multitracking.track_dataframes.TrackDfProvider import *

from honza_lines.HonzaLinesProvider import *


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

print("The end")
