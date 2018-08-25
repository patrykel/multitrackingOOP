import pandas as pd


class DfUtility:
    @staticmethod
    def get_row_df(row_data, column_names):
        row_data_dict = {}
        for i, (key, val) in enumerate(zip(column_names, row_data)):
            row_data_dict[key] = [val]

        return pd.DataFrame(row_data_dict, columns=column_names)

    @staticmethod
    def get_df(data2D, column_names):
        # WE ASSUME DATA IS 2D ARRAY
        row_dfs = []
        for row_data in data2D:
            row_dfs.append(DfUtility.get_row_df(row_data, column_names))

        return pd.concat(row_dfs, ignore_index=True)