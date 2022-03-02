import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import skimage.io
import functools

from GEN_Utils import FileHandling
from loguru import logger

logger.info('Import OK')

# define location parameters
input_folder = f'exp51/python_results/pixel_collection/'
output_folder = f'exp51/python_results/compiled_data/'

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# read in calculated pixel data
file_list = [filename for filename in os.listdir(input_folder) if '.csv' in filename]
pixels = {filename.replace('.csv', ''): pd.read_csv(f'{input_folder}{filename}') for filename in file_list}

# generate summary df for mask, channel of interest
pixels_compiled = pd.concat(pixels.values())
pixels_compiled.drop([col for col in pixels_compiled.columns.tolist() if 'Unnamed: ' in col], axis=1, inplace=True)

# clean compiled pixel data with only channels needed
cleaned_pixels = pixels_compiled.copy()[['image_name', 'mask_type', 'cell_number', 'x', 'y', 'channel_0', 'channel_2', 'channel_4', 'channel_5']]
cleaned_pixels.rename(columns= {'channel_0':'before_highPMT', 'channel_2':'before_lowPMT', 'channel_4':'after_lowPMT', 'channel_5':'after_highPMT'}, inplace=True)

# create new df for each mutant based off image_name
cleaned_pixels['mutant_name'] = cleaned_pixels['image_name'].str.split("_ ").str[0]
for mutant, data in cleaned_pixels.groupby(['mutant_name']):
    mutant
    dataframes = {mask: df for mask, df in data.groupby('mask_type')}
    # Save each mutant as separate excel file with separate sheets for cell, cytoplasm and nucleus
    # FileHandling.df_to_excel(
    #     output_path=f'{output_folder}{mutant}_pixels.xlsx', 
    #     sheetnames=list(dataframes.keys()), 
    #     data_frames=list(dataframes.values()))
    # Save each mutant and mask_type as a csv file 
    [df.to_csv(f'{output_folder}{mutant}_{key}.csv') for key, df in dataframes.items()]
