import pandas as pd
import matplotlib.pyplot as plt
from column_type import *

def get_histogram_bar(df, cols=None):
    if cols == None:
        cols = list(df.columns)
    cat_cols = get_catecorical_cols(df)
    num_cols = get_numerical_cols(df)
    for c in cols:
        print(c)
        if c in cat_cols:
            categories = df[c].value_counts().index
            counts = df[c].value_counts().values
            plt.bar(categories, counts)
        elif c in num_cols:
            plt.hist(df[c])
        else:
            print(f'{c} is ghh')
        plt.xticks(rotation=50)
        plt.xlabel(c)
        plt.ylabel('# Occurrences')
        plt.show()

