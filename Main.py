
from multitracking.algorithm.MinimizationBasedAlgorithm import *
from multitracking.algorithm.LeastSquaresBasedAlgorithm import *
from multitracking.track_dataframes.TrackDfProvider import *

# algorithm = MinimizationBasedAlgorithm()
algorithm = LeastSquaresBasedAlgorithm()

algorithm.run()

tracks_df_provider = TrackDfProvider.get_track_df_provider()
track_df = tracks_df_provider.provide()


print("Code")
print("Works")