from dataframes.DfRepository import *

class DfRepositoryProvider:

    DF_REPOSITORY = DfRepository()

    @staticmethod
    def provide():
        return DfRepositoryProvider.DF_REPOSITORY
