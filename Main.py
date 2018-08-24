
df_repository = DfRepository()  # initialize dataframe repository
                                # może nie jest to potrzebne ;)

ml = MultitrackingAlgorithm() # tu musze dać jakiś kontrakt -->
htp = HonzaTrackProivder()

multitrack_df = ml.tracks_as_df()
honza_tracks_df = htp.tracks_as_df()