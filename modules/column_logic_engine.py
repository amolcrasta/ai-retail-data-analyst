import numpy as np


class ColumnLogicEngine:

    def __init__(self):

        self.allowed_functions = {
            "abs": np.abs,
            "sqrt": np.sqrt,
            "log": np.log,
            "round": np.round,
            "floor": np.floor,
            "ceil": np.ceil,
            "clip": np.clip,
            "where": np.where,
        }


    def apply_logic(self, df, new_column, expression):

        local_dict = {}

        # add dataset columns
        for col in df.columns:
            local_dict[col] = df[col]

        # add allowed functions
        for k, v in self.allowed_functions.items():
            local_dict[k] = v

        df[new_column] = eval(expression, {"__builtins__": {}}, local_dict)

        return df