import pytest
import pandas as pd
import numpy as np
from sympy import maximum

from utils import get_relation, maximum_unique_mapping, maximum_unique_mappings

@pytest.fixture
def test_data():
    test_data = {'121_col1': {0: 'A1', 1: 'A2', 2: 'A2', 3: 'A3', 4: 'A3', 5: 'A4'},
 '121_col2': {0: 'A1', 1: 'A2', 2: 'A2', 3: np.nan, 4: 'A3', 5: 'A4'},
 '12m_col1': {0: 'B1', 1: 'B1', 2: 'B1', 3: 'B2', 4: 'B2', 5: 'B2'},
 '12m_col2': {0: 'B11', 1: 'B12', 2: 'B13', 3: 'B21', 4: 'B21', 5: 'B22'},
 'm2m_col1': {0: 'D1', 1: 'D2', 2: 'D3', 3: 'D1', 4: 'D2', 5: 'D3'},
 'm2m_col2': {0: 'D1', 1: 'D1', 2: 'D1', 3: 'D2', 4: 'D2', 5: 'D2'},
 '121_col1_int': {0: 1, 1: 2, 2: 2, 3: 3, 4: 3, 5: 4},
 '121_col2_int': {0: 1.0, 1: 2.0, 2: 2.0, 3: np.nan, 4: 3.0, 5: 4.0}}

    test_data = pd.DataFrame(test_data)
    return test_data

def test_one_to_one(test_data):
    col1 = "121_col1"
    col2 = "121_col2"
    relationship = get_relation(test_data, col1, col2)
    relationship_reversed = get_relation(test_data, col2, col1)
    assert relationship == "one-to-one"
    assert relationship_reversed == "one-to-one"
    
    
def test_one_to_many(test_data):
    col1 = "12m_col1"
    col2 = "12m_col2"
    relationship = get_relation(test_data, col1, col2)
    relationship_reversed = get_relation(test_data, col2, col1)
    assert relationship == "one-to-many"
    assert relationship_reversed == "many-to-one"

def test_many_to_many(test_data):
    col1 = "m2m_col1"
    col2 = "m2m_col2"
    relationship = get_relation(test_data, col1, col2)
    relationship_reversed = get_relation(test_data, col2, col1)
    assert relationship == "many-to-many"
    assert relationship_reversed == "many-to-many"


def test_one_to_one_int(test_data):
    col1 = "121_col1_int"
    col2 = "121_col2_int"
    relationship = get_relation(test_data, col1, col2)
    relationship_reversed = get_relation(test_data, col2, col1)
    assert relationship == "one-to-one"
    assert relationship_reversed == "one-to-one"
    
def test_one_to_one_with_na(test_data):
    col1 = "121_col1"
    col2 = "121_col2"
    relationship = get_relation(test_data, col1, col2, ignore_na=False)
    relationship_reversed = get_relation(test_data, col2, col1, ignore_na=False)
    assert relationship == "one-to-many"
    assert relationship_reversed == "many-to-one"

def test_single_unique_mapping(test_data):
    col1 = "121_col1"
    col2 = "121_col2"
    max_value = maximum_unique_mapping(test_data, col1, col2)
    max_value_reversed = maximum_unique_mapping(test_data, col1, col2)
    assert max_value == 1
    assert max_value_reversed == 1
    
def test_single_unique_mapping_with_na_replace(test_data):
    col1 = "121_col1"
    col2 = "121_col2"
    test_data = test_data.fillna("-1") #only col2 has an NaN value, so should only impact max_value variable
    max_value = maximum_unique_mapping(test_data, col1, col2)
    max_value_reversed = maximum_unique_mapping(test_data, col2, col1)
    assert max_value == 2
    assert max_value_reversed == 1
    
def test_number_unique_mappings(test_data):
    returned_df = maximum_unique_mappings(test_data)

    val1 = returned_df.loc["12m_col1", "12m_col2"]
    assert val1 == 3

    val2 = returned_df.loc["12m_col2", "12m_col1"] 
    assert val2 == 1

def test_ignore_cols_reduces_df_size(test_data):

    #pick 1 column
    col = test_data.columns[0]
    returned_df = maximum_unique_mappings(test_data, ignore_cols=[col])
    assert test_data.shape[1] == returned_df.shape[1] + 1