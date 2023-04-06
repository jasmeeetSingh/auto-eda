import pandas as pd


def get_catecorical_cols(df):
    return [col for col in list(df.columns) if df[col].dtype == 'O']

def get_numerical_cols(df):
    int_cols = [col for col in list(df.columns) if 'int' in str(df[col].dtype) ]
    float_cols = [col for col in list(df.columns) if 'float' in str(df[col].dtype) ]
    return int_cols + float_cols

