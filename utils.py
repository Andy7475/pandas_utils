import pandas as pd
import pandas_flavor as pf

def get_relation(df, col1, col2, ignore_na=True, na_replace_value="-1"):
    """Returns the type of relationship between the two columns. one-to-one, one-to-many, many-to-one or many-to-many
    option for ignoring missing values. If na is not ignored, then nan's are replaced with the na_replace_value before the
    relationship is determined
    
    Returns a string of the type of relationship from the list of 4 options"""
    
    if ignore_na == False:
        df[[col1, col2]] = df[[col1, col2]].fillna(na_replace_value)
        
    max_values_from_col1 = df[[col1, col2]].groupby(col1).nunique().max().values
    max_values_from_col2 = df[[col1, col2]].groupby(col2).nunique().max().values
    
    if max_values_from_col2 == 1: #then it is 1-to-something
        if max_values_from_col1 == 1:
            return "one-to-one"
        else:
            return "one-to-many"
    else: #then it is many-to-something
        if max_values_from_col1 == 1:
            return "many-to-one"
        else:
            return "many-to-many"
    