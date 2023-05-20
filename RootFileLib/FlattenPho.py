
""""
This module hasn't been completed.
xAna.cpp has solved the flatten problem.

"""


from RootFileLib.Progress import print_progress
import dask

@dask.delayed
def expand_row(row):
    import pandas as pd 
    branches = list(row.index)
    df_mini = pd.DataFrame(columns=row.index)
    nPho = row["nPho"]
    for i in range(nPho):
        for col in branches:
            if col[:3] == "pho":
                df_mini.loc[i, col] = row[col][i]
            else:
                df_mini.loc[i, col] = row[col]
    return df_mini
                

@dask.delayed
def flatten_pho(df):
    import pandas as pd
    df_new = pd.DataFrame(columns=df.columns)
    for idx in range(len(df)):
        if idx % 1000 == 0:
            print_progress(idx, len(df))
        df_new = dask.delayed(pd.concat)([df_new, expand_row(df.iloc[idx])])
    return df_new