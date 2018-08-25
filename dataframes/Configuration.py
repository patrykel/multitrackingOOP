
class Configuration():

    # DATAFRAMES CREATED FROM FILES
    GEOM_RP_DF = "geom_rp_df"
    GEOM_SILICON_DF = "geom_silicon_df"
    HIT_LINES_DF = "hit_lines_df"

    DF_FILE_NAMES = [GEOM_RP_DF, GEOM_SILICON_DF, HIT_LINES_DF]

    FILES_TO_READ_DF = {
        GEOM_RP_DF: "dataframes/data_files/geom_rp.csv",
        GEOM_SILICON_DF: "dataframes/data_files/geom_silicon.csv",
        HIT_LINES_DF: "dataframes/data_files/hit_lines_18ev.csv"
    }

    @staticmethod
    def get_df_files_names():
        return Configuration.DF_FILE_NAMES

    @staticmethod
    def get_filename(df_name):
        return Configuration.FILES_TO_READ_DF[df_name]

    # DATAFRAMES COMPUTED
    HIT_LINES_SINGLE_3RP_DF = "hit_lines_single_3rp_df"

    COMPUTED_DF_NAMES = [HIT_LINES_SINGLE_3RP_DF]