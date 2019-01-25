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

BASE_RAW_DATA_DIR = 'data/raw'
"""
str: Base raw data directory
"""

BASE_PROCESSED_DATA_DIR = 'data/processed'
"""
str: Base processed data directory
"""

META_CSV_FILE = 'data/raw/HAM10000_metadata.csv'
"""
str: HAM1000_metadata.csv metadata file location 
"""

L_28_28_CSV_FILE = BASE_RAW_DATA_DIR + '/hmnist_28_28_L.csv'
"""
str: hmnist_28_28_L.csv 28 X 28 luminance values file location 
"""

RGB_28_28_CSV_FILE = BASE_RAW_DATA_DIR + '/hmnist_28_28_RGB.csv'
"""
str: hmnist_28_28_L.csv 28 X 28 RGB values file location 
"""

lesions_list = ['Melanocytic nevi', 'dermatofibroma',
                'Benign keratosis-like lesions ', 'Basal cell carcinoma',
                'Actinic keratoses', 'Vascular lesions', 'Dermatofibroma']
"""
list: a list used to store the conditions full names
"""



@pytest.fixture
def global_meta():
    """Fixture used to pass metadata dataset
    
    Returns
    -------
    pandas.core.frame.DataFrame
        metadata dataframe
    """
    
    META_DF = pd.read_csv(META_CSV_FILE)
    return(META_DF.copy())

@pytest.fixture
def global_l_28_28():
    """Fixture used to pass 28 X 28 luminance dataset
    
    Returns
    -------
    pandas.core.frame.DataFrame
        28 X 28 luminance dataframe
    """

    L_28_28_DF = pd.read_csv(L_28_28_CSV_FILE)
    return(L_28_28_DF.copy())
    
@pytest.fixture
def global_rgb_28_28():
    """Fixture used to pass 28 X 28 RGB dataset
    
    Returns
    -------
    pandas.core.frame.DataFrame
        28 X 28 RGB dataframe
    """
    RGB_28_28_DF = pd.read_csv(RGB_28_28_CSV_FILE)
    return(RGB_28_28_DF.copy())
    
@pytest.fixture
def global_lesions_list():
    """Fixture used return list of skin lesions
    
    Returns
    -------
    list
        skin lesion textual conditions
    """
    return(lesions_list)
    
@pytest.fixture
def global_merge_col_count():
    """Fixture used return expected columns count after merge
    
    Returns
    -------
    int
        column count (expected)
    """
    return(3145)
        
@pytest.mark.usefixtures('global_meta', 'global_lesions_list')
class TestMetaCleaning(object):
     """ Tests metadata dataframe cleaning   

     """
     
     def test_lesion_id_drop(self, global_meta):      
        """ Tests if lesion_id was dropped

        """
        meta_df = md.clean_meta(global_meta)
        assert not(meta_df.columns.isin(['lesion_id']).any())
    
     def test_image_id_drop(self, global_meta):      
        """ Tests if image_id was dropped

        """
        meta_df = md.clean_meta(global_meta)
        assert not(meta_df.columns.isin(['image_id']).any())
     
     def test_age_na_fix(self, global_meta):      
        """ Tests if age nas were replaced with average

        """
        meta_df = md.clean_meta(global_meta)
        assert not (meta_df.age.isnull().values.any())
        
     def test_dx_num(self, global_meta):
        """ Tests skin lesion diagnosis replacement with
        numerical category field
        
        """
        meta_df = md.clean_meta(global_meta)
        assert(meta_df['lesion_type_idx'].between(0,6).any())
        
     def test_lesion_text(self, global_meta, global_lesions_list):
        """ Tests skin lesion text addition
        
        """
        meta_df = md.clean_meta(global_meta)
        
        # Check if lesion types are in the list
        
        assert(meta_df['lesion_type'].isin(global_lesions_list).any())
        
@pytest.mark.usefixtures('global_l_28_28', 'global_rgb_28_28', 'global_meta', 
                         'global_merge_col_count')
class TestRGBLMetaMerge(object):
     """ Tests RGB and luminance dataframe merge with metadata   

     """     
     def test_l_rgb_meta_merge_no_null(self, global_meta, global_l_28_28, 
                                      global_rgb_28_28):      
        """ Tests if merge has any nulls

        """
        merged_df = md.merge_pixel_values(global_meta, global_l_28_28, 
                                          global_rgb_28_28)
        assert((merged_df.isnull().values.any()))
        
     def test_l_rgb_meta_merge_fields(self, global_meta, global_l_28_28,
                                      global_rgb_28_28, global_merge_col_count):
        """ Tests if merge added all required fields

        """
        merged_df = md.merge_pixel_values(global_meta, global_l_28_28, 
                                          global_rgb_28_28)
        # not cleaned so labels count
        assert(len(merged_df.columns) == global_merge_col_count) 
        
        
@pytest.mark.usefixtures('global_l_28_28', 'global_rgb_28_28')
class TestRGBLCleaning(object):
     """ Tests RGB and luminance dataframe cleaning   

     """     
        
     def test_l_28_28_drop(self, global_l_28_28):      
        """ Tests if label col for 28 X 28 luminance was dropped

        """
        assert not((md.clean_luminance(
                global_l_28_28).columns.isin(['label']).any())) 
        
     def test_rgb_28_28_drop(self, global_rgb_28_28):      
        """ Tests if label col for 28 X 28 RGB was dropped

        """
        assert not((md.clean_rgb(
                global_rgb_28_28).columns.isin(['label']).any())) 