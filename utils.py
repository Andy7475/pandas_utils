import pandas as pd
import pandas_flavor as pf

@pf.register_dataframe_method
def get_relation(df, col1, col2, ignore_na=True, na_replace_value="-1"):
    """Returns the type of relationship between the two columns. one-to-one, one-to-many, many-to-one or many-to-many
    option for ignoring missing values. If na is not ignored, then nan's are replaced with the na_replace_value before the
    relationship is determined
    
    Returns a string of the type of relationship from the list of 4 options"""
    df_temp = df.copy() 
    if ignore_na == False:
        df_temp[[col1, col2]] = df[[col1, col2]].fillna(na_replace_value)
        
    max_values_from_col1 = df_temp[[col1, col2]].groupby(col1).nunique().max().values
    max_values_from_col2 = df_temp[[col1, col2]].groupby(col2).nunique().max().values
    
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



@pf.register_dataframe_method
def maximum_unique_mapping(df, col1, col2):
    """returns the maximum number of unique values in col2 that map to a single value in col1
    So col1, col2
       A, duck
       A, goat
       B, chicken
       
    would yield a value of 2, as both duck and goat map to a single value in column 1, and that number (2) is 
    higher than the single value (chicken) that maps to B"""
    
    max_unique_values = pd.pivot_table(df.drop_duplicates([col1, col2]), index=[col1], aggfunc="count", values=col2).max()
    return int(max_unique_values)

@pf.register_dataframe_method
def maximum_unique_mappings(df, ignore_cols=[]):
    """Returns an n x n dataframe where n = len(df.columns). The values in each cell are the maximum number of values that
map to a single value in another column. The index columns being the reference"""
    
    cols_to_use = [col for col in list(df.columns) if col not in ignore_cols]
    blank_df = pd.DataFrame(index = cols_to_use, columns = cols_to_use)
    for col1 in cols_to_use:
        for col2 in cols_to_use:
            if col1 == col2:
                continue
            blank_df.loc[col1, col2] = maximum_unique_mapping(df, col1, col2)
    return blank_df