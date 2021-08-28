import pandas as pd
import numpy as np


t_DataFrame = type(pd.DataFrame())
t_Series = type(pd.Series)

# Forma correcta y sin errores de sustituir valores en una columna de un df o una Series

# Old version
"""
def replace_Series_values(df: t_DataFrame, col: str, old_value: any, new_value: any):
    n = 0
    for i in df[col]:
        if (i == old_value):
            df.at[n, col] = new_value
        n += 1
    return df[col]
"""

# New version

def replace_Series_values(df: t_DataFrame, col: str, old_value: any, new_value: any):
    return df[col].apply(lambda x: new_value if x == old_value else x)

