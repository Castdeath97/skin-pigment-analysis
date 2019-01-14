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
import numpy as np

META_CSV_FILE = 'data/raw/HAM10000_metadata.csv'
"""
str: HAM1000_metadata.csv metadata file location 
"""

PROCESSED__CSV_FILE = 'data/processed/processed.csv'
"""
str: HAM1000_metadata.csv metadata file location 
"""

def clean_meta(meta_df):
    """ Cleans metadata dataframe by filling age NAs with the mean

    Parameters
    ----------
    meta_df
        meta_df to clean

    Returns
    -------
    pandas.core.frame.DataFrame
        Cleaned meta dataframe

    """
    return(meta_df['age'].fillna((meta_df['age'].mean())))


def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    
        
    # Read datasets in
    
    meta_df = pd.read_csv(META_CSV_FILE)
    
    # clean meta dataset
    
    meta_df = clean_meta(meta_df)
    
    # save datasets
    
    meta_df.to_csv()
    
if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]
    
    main()
