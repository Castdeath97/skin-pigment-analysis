# -*- coding: utf-8 -*-
"""
Introduction
--------------

This python file contains the source code used to test the data preparation
process

Code
------

"""
import pandas as pd
from src.data import make_dataset as md
import pytest

META_CSV_FILE = 'data/raw/HAM10000_metadata.csv'
"""
str: HAM1000_metadata.csv metadata file location 
"""

@pytest.fixture
def global_meta():
    """Fixture used to pass metadata dataset
    
    Returns
    -------
    pandas.core.frame.DataFrame
        metadata dataframe
    """
    return(pd.read_csv(META_CSV_FILE))

@pytest.mark.usefixtures('global_meta')
class TestMetaCleaning(object):
     """ Tests HAM10000_metadata.csv dataframe cleaning   

     """
     
     def test_age_na_fix(self, global_meta):      
        """ Tests if age nas were replaced with average

        """
        meta_df = md.clean_meta(global_meta)
        assert(meta_df.isna().sum() == 0)