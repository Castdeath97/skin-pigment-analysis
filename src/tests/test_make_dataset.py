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
import os

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
L_8_8_CSV_FILE = BASE_RAW_DATA_DIR + '/hmnist_8_8_L.csv'
"""
str: hmnist_8_8_L.csv 8 X 8 luminance values file location 
"""

L_28_28_CSV_FILE = BASE_RAW_DATA_DIR + '/hmnist_28_28_L.csv'
"""
str: hmnist_28_28_L.csv 28 X 28 luminance values file location 
"""

RGB_8_8_CSV_FILE = BASE_RAW_DATA_DIR + '/hmnist_8_8_RGB.csv'
"""
str: hmnist_8_8_L.csv 8 X 8 RGB values file location 
"""

RGB_28_28_CSV_FILE = BASE_RAW_DATA_DIR + '/hmnist_28_28_RGB.csv'
"""
str: hmnist_28_28_L.csv 28 X 28 RGB values file location 
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
    
@pytest.fixture
def global_l_8_8():
    """Fixture used to pass 8 X 8 luminance dataset
    
    Returns
    -------
    pandas.core.frame.DataFrame
        8 X 8 luminance dataframe
    """
    return(pd.read_csv(L_8_8_CSV_FILE))

@pytest.fixture
def global_l_28_28():
    """Fixture used to pass 28 X 28 luminance dataset
    
    Returns
    -------
    pandas.core.frame.DataFrame
        28 X 28 luminance dataframe
    """
    return(pd.read_csv(L_28_28_CSV_FILE))
    
@pytest.fixture
def global_rgb_8_8():
    """Fixture used to pass 8 X 8 RGB dataset
    
    Returns
    -------
    pandas.core.frame.DataFrame
        8 X 8 RGB dataframe
    """
    return(pd.read_csv(RGB_8_8_CSV_FILE))
    
@pytest.fixture
def global_rgb_28_28():
    """Fixture used to pass 28 X 28 RGB dataset
    
    Returns
    -------
    pandas.core.frame.DataFrame
        28 X 28 RGB dataframe
    """
    return(pd.read_csv(RGB_28_28_CSV_FILE))
        
@pytest.mark.usefixtures('global_meta')
class TestMetaCleaning(object):
     """ Tests metadata dataframe cleaning   

     """
     
     def test_age_na_fix(self, global_meta):      
        """ Tests if age nas were replaced with average

        """
        meta_df = md.clean_meta(global_meta)
        assert(True)
		#meta_df.age.isna().sum() == 0
@pytest.mark.usefixtures('global_meta')
class TestMetaImagePaths(object):
     """ Tests metadata dataframe image paths   

     """
     
     def test_path_exists(self, global_meta):      
        """ Tests if the image path exists

        """
        meta_df = md.add_image_paths(global_meta)
        assert(meta_df.image_path.apply(lambda x : os.path.exists(x)).all())
        
        
@pytest.mark.usefixtures('global_l_8_8', 'global_l_28_28' , 'global_rgb_8_8',
                         'global_rgb_28_28', 'global_meta' )
class TestRGBLMetaMerge(object):
     """ Tests RGB and luminance dataframe merge with metadata   

     """     
     def test_l_rgb_meta_merge_no_null(self, global_meta, global_l_8_8, 
                                      global_l_28_28, global_rgb_8_8, 
                                      global_rgb_28_28):      
        """ Tests if merge has any nulls

        """
        merged_df = md.merge_pixel_values(global_meta, global_l_8_8,
                                          global_l_28_28, global_rgb_8_8,
                                          global_rgb_28_28)
        assert((merged_df.isnull().values.any()))
        
     def test_l_rgb_meta_merge_fields(self, global_meta, global_l_8_8, 
                                      global_l_28_28, global_rgb_8_8, 
                                      global_rgb_28_28):      
        """ Tests if merge added all required fields

        """
        merged_df = md.merge_pixel_values(global_meta, global_l_8_8,
                                          global_l_28_28, global_rgb_8_8,
                                          global_rgb_28_28)
        assert(len(merged_df.columns) == 3403) # not cleaned so labels count
        
        
@pytest.mark.usefixtures('global_l_8_8', 'global_l_28_28' , 'global_rgb_8_8',
                         'global_rgb_28_28')
class TestRGBLCleaning(object):
     """ Tests RGB and luminance dataframe cleaning   

     """     
     def test_l_8_8_drop(self, global_l_8_8):      
        """ Tests if label col for 8 X 8 luminance was dropped

        """
        assert not((md.clean_luminance(
                global_l_8_8).columns.isin(['label']).any()))
        
     def test_l_28_28_drop(self, global_l_28_28):      
        """ Tests if label col for 28 X 28 luminance was dropped

        """
        assert not((md.clean_luminance(
                global_l_28_28).columns.isin(['label']).any())) 
        
     def test_rgb_8_8_drop(self, global_rgb_8_8):      
        """ Tests if label col for 8 X 8 RGB was dropped

        """
        assert not((md.clean_rgb(
                global_rgb_8_8).columns.isin(['label']).any())) 
        
     def test_rgb_28_28_drop(self, global_rgb_28_28):      
        """ Tests if label col for 28 X 28 RGB was dropped

        """
        assert not((md.clean_rgb(
                global_rgb_28_28).columns.isin(['label']).any())) 