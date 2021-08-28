import pandas as pd
import warnings


# important types

t_Dataframe = type(pd.DataFrame())
t_Series = pd.Series


# validate the main fields.
# register columns names with null values.

def create_df_nulls_series(df: t_Dataframe):
    nulls_series = df.isnull().sum()
    return nulls_series

def register_columns_with_nulls(df: t_Dataframe, df_obligatory_fields: list):
    nulls_series = create_df_nulls_series(df)
    columns_names_with_nulls = []
    for i in df_obligatory_fields:
        if (nulls_series[i] != 0):
            columns_names_with_nulls.append(i)
    return columns_names_with_nulls

def create_nulls_warn_file(df_id: int, df: t_Dataframe, df_obligatory_fields: list):
    col_with_nulls = register_columns_with_nulls(df, df_obligatory_fields)
    if (len(col_with_nulls) > 0):
        row_nulls = df.loc[:, col_with_nulls].isnull()
        df_nulls_file = pd.DataFrame()
        for i in col_with_nulls:
            df_nulls_file = df_nulls_file.append(df[row_nulls[i] == True].fillna('( NULL )'))
        df_nulls_file = df_nulls_file.reset_index().drop_duplicates(subset='index', keep='first')
        df_nulls_file = df_nulls_file.rename(columns={'index': 'Nro Registro'})

        warns = "Los siguientes campos obligatorios contienen valores nulos: "
        warnings.warn("Los siguientes campos obligatorios contienen valores nulos: {}".format(col_with_nulls))
        if (df_id == 0):
            df_nulls_file.to_csv('CamposNulosPami.csv')
        elif (df_id == 1):
            df_nulls_file.to_csv('CamposNulosSQL.csv')


# general procedure: add leading zeros to each value of a column.

def float_to_str(df: t_Dataframe, col: str):
    df[col] = df[col].convert_dtypes()       # cast to int64Dtype (supportes pd.NA) to remove decimal points.
    df[col] = df[col].apply(str)             # cast to str.
    return df[col]

def add_zeros_to_left(df: t_Dataframe, col: str, digits: int):
    if (df[col].dtype == float):
        df[col] = float_to_str(df, col)
    if (df[col].dtype == int):
        df[col] = df[col].apply(str)
    if (df[col].dtype == object):
        n = 0
        for i in df[col]:          
            df.at[n, col] = i.zfill(digits)      # add leading zeros to each value.
            n += 1
    return df[col]
