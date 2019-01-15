"""
Introduction
--------------

This python file contains the source code used to carry the data preparation
process

Code
------

"""
# -*- coding: utf-8 -*-
import logging
from pathlib import Path
import pandas as pd
import os
from glob import glob

BASE_RAW_DATA_DIR = 'data/raw'
"""
str: Base raw data directory
"""

BASE_PROCESSED_DATA_DIR = 'data/processed'
"""
str: Base processed data directory
"""

META_CSV_FILE = BASE_RAW_DATA_DIR + '/HAM10000_metadata.csv'
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

PROCESSED_CSV_FILE = BASE_RAW_DATA_DIR + '/processed.csv'
"""
str: HAM1000_metadata.csv metadata file location 
"""

def clean_meta(meta_df):
    """ Cleans metadata dataframe by filling age NAs with the mean

    Parameters
    ----------
    meta_df
        metadata dataframe to clean

    Returns
    -------
    pandas.core.frame.DataFrame
        Cleaned meta dataframe

    """
    meta_df.age = meta_df.age.fillna(meta_df.age.mean())
    return(meta_df)
    
def clean_luminance(l_df):
    """ Cleans a luminance dataframe by removing uneeded label field

    Parameters
    ----------
    l_df
        luminance dataframe (8X8 or 28X28) to clean

    Returns
    -------
    pandas.core.frame.DataFrame
        Cleaned luminance dataframe

    """
    l_df.drop(columns='label', inplace=True)
    return(l_df)
    
def clean_rgb(rgb_df):
    """ Cleans a rgb dataframe by removing uneeded label field

    Parameters
    ----------
    rgb_df
        RGB dataframe (8X8 or 28X28) to clean

    Returns
    -------
    pandas.core.frame.DataFrame
        Cleaned rgb dataframe

    """
    rgb_df.drop(columns='label', inplace=True)
    return(rgb_df)
       
def merge_pixel_values(meta_df, l_8_8_df, l_28_28_df,
                       rgb_8_8_df, rgb_28_28_df):
    """ Merges metadata dataframe with RGB and luminance pixel values dfs

    Parameters
    ----------
    meta_df
        metadata dataframe
    
    l_8_8_df
        8 X 8 luminance dataframe
    
    l_28_28_df
        28 X 28 luminance dataframe
        
    rgb_8_8_df
        8 X 8 RGB dataframe

    rgb_28_28_df
        28 X 28 RGB dataframe

    Returns
    -------
    pandas.core.frame.DataFrame
        Merged dataframe

    """
    
    # Add suffix to names to ensure they are unique after merge
    
    l_8_8_df.columns = [str(col) + '_l_8_8' for col in l_8_8_df.columns]
    l_28_28_df.columns = [str(col) + '_l_28_28'
                            for col in l_28_28_df.columns]
    rgb_8_8_df.columns = [str(col) + '_rgb_8_8' for col in rgb_8_8_df.columns]
    rgb_28_28_df.columns = [str(col) + '_rgb_28_28'
                            for col in rgb_28_28_df.columns]

    frames = [meta_df, l_8_8_df, l_28_28_df, rgb_8_8_df, rgb_28_28_df]
    merged_df = pd.concat(frames, sort=False, axis=1)
    return(merged_df)

def add_image_paths(meta_df):
    """ Adds image path to image meta data

    Parameters
    ----------
    meta_df
        meta_df to add path to

    Returns
    -------
    pandas.core.frame.DataFrame
        meta dataframe updated with paths

    """
    
    # Find image paths
    
    image_paths = {os.path.splitext(os.path.basename(x))[0]: x
                         for x in glob(
                                 os.path.join(BASE_RAW_DATA_DIR, '*', '*.jpg'))}

    # link image paths to ids using map
    
    meta_df['image_path'] = meta_df.image_id.map(image_paths.get)
    
    return(meta_df)
    

def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
        
    # Read datasets in
    
    meta_df = pd.read_csv(META_CSV_FILE)
    l_8_8_df = pd.read_csv(L_8_8_CSV_FILE)
    l_28_28_df = pd.read_csv(L_28_28_CSV_FILE)
    rgb_8_8_df = pd.read_csv(RGB_8_8_CSV_FILE)
    rgb_28_28_df = pd.read_csv(RGB_28_28_CSV_FILE)

    # clean meta dataset
    
    meta_df = clean_meta(meta_df)
    
    # clean pixel datasets
    
    l_8_8_df = clean_luminance(l_8_8_df)
    l_28_28_df = clean_luminance(l_28_28_df)
    rgb_8_8_df = clean_rgb(rgb_8_8_df)
    rgb_28_28_df = clean_rgb(rgb_28_28_df)
	
	# Add image paths
    
    meta_df = add_image_paths(meta_df)
    
    # Merge datasets
    merged_df = merge_pixel_values(meta_df, l_8_8_df, l_28_28_df, rgb_8_8_df,
                                   rgb_28_28_df)
    merged_df.shape
    # save merged dataset
    
    merged_df.to_csv(PROCESSED_CSV_FILE)
    
if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]
    
    main()
