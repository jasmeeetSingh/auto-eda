import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def count_nulls_column(df, column):
    return df[column].isnull().sum()


def percentage_nulls_column(df, column):
    return (count_nulls_column(df, column)/len(df)) * 100


def calculate_nulls(df, column_list, verbosity):

    no_nulls = []
    for i in column_list:
        count_nulls = count_nulls_column(df, i)
        per_nulls = percentage_nulls_column(df, i)

        num_distinct_values = len(df[i].value_counts())

        if (per_nulls > 0):
            print(f"Number of nulls in {i} is : {count_nulls}")
            print(f"Percentage of nulls in {i} is : {per_nulls}")

            # If there are too many distinct values, we can't directly impute them
            if (num_distinct_values > 0.10 * len(df)):
                print(
                    f"There are too many distinct values to fill for column {i}, avoid filling missing values with mean, median or mode. Drop the missing values if possible")

        else:
            if (verbosity == 1):
                print(f"No nulls in {i}")
            else:
                no_nulls.append(i)

        if (verbosity == 1):
            if (per_nulls == 0):
                print("No updates needed as, percentage of nulls = 0%, we can proceed")
            elif (per_nulls < 10):
                print(
                    "No updates needed as, percentage of nulls <10%, we can drop the null rows")
            elif (per_nulls < 40):
                print(
                    "Missing values need to be updated, call fill_missing_values() to do imputations based on ML models")
            elif (per_nulls < 60):
                print(
                    "Missing values are more than 60%,call fill_missing_values_majority() to do imputations based on column distribution")
            else:
                print(
                    ">60% nulls, need to drop the column, use df.drop() to drop the column")

    if (verbosity == 0):
        print(f"No nulls present in {[i for i in no_nulls]}")


def check_nulls(df, column_list=None, verbosity=0):

    if (column_list == None):
        column_list = df.columns

    calculate_nulls(df, column_list, verbosity)


def fill_missing_values(df, column_name):

    if (column_name == None):
        raise Exception("Column name is required")


def print_missing_values(column_name, method):
    print(f"Filling the column {column_name} with {method}")


def get_uncorelated_columns_for_modelling(df, column_name):
    
    corr_matrix = df.corr(method = 'kendall')
    columns_all_df = corr_matrix[column_name].reset_index()
    columns_all_df = columns_all_df[abs(columns_all_df[column_name]) < 0.1]
    
    return list(columns_all_df['index'].values)

def drop_nulls_imputation(model_df, column_names_imputation):
    for col in column_names_imputation:
        if(percentage_nulls_column(model_df, col) < 20):
            model_df = model_df.dropna(how = 'any', axis = 0)
        else:
            model_df = model_df.drop(axis = 1, columns = [col])
            
    return model_df


def fill_missing_values_interpolation_impl(df, column_name):
    '''
    Filling missing values with interpolation
    '''
    df[column_name] = df[column_name].interpolate()
    return df


def fill_missing_values_interpolation(df, column_name, inplace):
    '''
    Filling missing values with interpolation
    '''
    if (inplace == True):
        fill_missing_values_interpolation_impl(df, column_name)
    else:
        return fill_missing_values_interpolation_impl(df.copy(), column_name)


def fill_missing_values_descriptive_impl(df, column_name, method, verbosity):
    '''
    Filling missing values with descriptive statistics - mean, median or mode
    '''
    if (method == 'mean'):
        column_mean = df[column_name].mean()
        df[column_name] = df[column_name].fillna(column_mean)

    if (method == 'median'):
        column_median = df[column_name].median()
        df[column_name] = df[column_name].fillna(column_median)

    if (method == 'mode'):
        column_mode = df[column_name].mode()[0]
        df[column_name] = df[column_name].fillna(column_mode)

    if (verbosity == 1):
        print_missing_values(column_name, method)
    return df


def fill_missing_values_descriptive(df, column_name, method, verbosity, inplace):
    '''
    Filling missing values with descriptive statistics - mean, median or mode
    '''
    if (inplace == True):
        fill_missing_values_descriptive_impl(df, column_name, method, verbosity)
    else:
        return fill_missing_values_descriptive_impl(df.copy(), column_name, method, verbosity)
