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

L_28_28_CSV_FILE = BASE_RAW_DATA_DIR + '/hmnist_28_28_L.csv'
"""
str: hmnist_28_28_L.csv 28 X 28 luminance values file location 
"""

RGB_28_28_CSV_FILE = BASE_RAW_DATA_DIR + '/hmnist_28_28_RGB.csv'
"""
str: hmnist_28_28_RGB.csv 28 X 28 RGB values file location 
"""

PROCESSED_CSV_FILE = BASE_PROCESSED_DATA_DIR + '/processed.csv'
"""
str: HAM1000_metadata.csv metadata file location 
"""

lesions_dict = {
    'nv': 'Melanocytic nevi',
    'mel': 'Melanoma',
    'bkl': 'Benign keratosis-like lesions ',
    'bcc': 'Basal cell carcinoma',
    'akiec': 'Actinic keratoses',
    'vasc': 'Vascular lesions',
    'df': 'Dermatofibroma'
}
"""
dict: a dictionary used to store the conditions full names
"""

def clean_meta(meta_df):
    """ Cleans metadata dataframe by filling age NAs (mean) and adding
    lesion text and ids

    Parameters
    ----------
    meta_df
        metadata dataframe to clean

    Returns
    -------
    pandas.core.frame.DataFrame
        Cleaned meta dataframe

    """    
    # adding new lesion fields
    
    meta_df['lesion_type'] = meta_df['dx'].map(lesions_dict.get)
    meta_df['lesion_type_idx'] = pd.Categorical(meta_df['lesion_type']).codes
    
    # Drop redudant and unecessary fields
    
    meta_df.drop(['dx', 'lesion_id', 'image_id'], axis = 1, inplace = True)
    
    # Replacing/filling NAs
    
    meta_df.age = meta_df.age.fillna(meta_df.age.mean())
    
    return(meta_df)
       
def merge_pixel_values(meta_df, l_28_28_df, rgb_28_28_df):
    """ Merges metadata dataframe with RGB and luminance pixel values dfs

    Parameters
    ----------
    meta_df
        metadata dataframe
    
    l_28_28_df
        28 X 28 luminance dataframe

    rgb_28_28_df
        28 X 28 RGB dataframe

    Returns
    -------
    pandas.core.frame.DataFrame
        Merged dataframe

    """
    
    # Add suffix to names to ensure they are unique after merge
    
    l_28_28_df.columns = [str(col) + '_l_28_28'
                            for col in l_28_28_df.columns]
    rgb_28_28_df.columns = [str(col) + '_rgb_28_28'
                            for col in rgb_28_28_df.columns]
    
    # Merge first with luminance then rgb using append with transpose
    # Transpose makes sure axis direction is correct
    
    merged_df_l = (l_28_28_df.T.append(meta_df.T, sort=False)).T
    merged_df_l_rgb = (rgb_28_28_df.T.append(merged_df_l.T, sort=False)).T
    
    return(merged_df_l_rgb)
    
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

def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
        
    # Read datasets in
    
    meta_df = pd.read_csv(META_CSV_FILE)
    l_28_28_df = pd.read_csv(L_28_28_CSV_FILE)
    rgb_28_28_df = pd.read_csv(RGB_28_28_CSV_FILE)
    
    # clean meta dataset
    
    meta_df = clean_meta(meta_df)
    
    # clean rgb and luminance datasets
    
    l_28_28_df = clean_luminance(l_28_28_df)
    rgb_28_28_df = clean_rgb(rgb_28_28_df)
    
    # Merge datasets
        
    merged_df = merge_pixel_values(meta_df, l_28_28_df, rgb_28_28_df)
            
    # save merged dataset
    
    merged_df.to_csv(PROCESSED_CSV_FILE)
    
if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]
    
    main()
