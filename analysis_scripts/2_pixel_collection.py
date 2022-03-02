import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import skimage.io
import functools
#import napari
# from GEN_Utils.FileHandling import df_to_excel
from loguru import logger

logger.info('Import OK')

# define location parameters
image_folder = f'python_results/initial_cleanup/8ala_hsp40_hsp70/'
mask_folder = f'python_results/cellpose_masking/8ala_hsp40_hsp70/'
output_folder = f'python_results/pixel_collection/8ala_hsp40_hsp70/'

if not os.path.exists(output_folder):
    os.mkdir(output_folder)


# define function to collect pixel location and intensity for a given mask, image combination
def pixel_collector(image_array, mask, mask_type=None, visualise=False):
    pixel_array = np.where(mask == 1, image_array, np.nan)
    # plt.imshow(pixel_array)
    coords = pd.DataFrame(pixel_array).unstack().reset_index().dropna()
    coords.columns = ['x', 'y', 'intensity']

    if mask_type != None:
        coords['mask_type'] = mask_type

    if visualise:
        # test visualisation, compare to plt.show
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.scatterplot(coords['x'], coords['y'], hue=coords['intensity'], palette='magma_r', size=0.5,linewidth=0, alpha = 0.7)
        plt.ylim(1024, 0)
        plt.xlim(0, 1024)

    return coords


# ----------------Initialise file list----------------
file_list = [filename for filename in os.listdir(
    image_folder) if 'npy' in filename]
images = {filename.replace('.npy', ''): np.load(
    f'{image_folder}{filename}') for filename in file_list}

# fails try/except if no masks found therefore skip that image
masks = {}
for image_name, img in images.items():
    logger.info(f'Processing {image_name}')
    try:
       masks[image_name] = {cell_number.replace('.npy', ''): np.load(f'{mask_folder}{image_name}/{cell_number}') for cell_number in os.listdir(f'{mask_folder}{image_name}')}
       logger.info(f'Masks loaded for {len(masks[image_name].keys())} cells')
    except:
        logger.info(f'{image_name} not processed as no mask found')

# ----------------collect pixel information----------------
pixel_information = {}
for image_name, img in images.items():
    image_name
    logger.info(f'Processing {image_name}')
    try:
        channels = []
        for image_channel in range(img.shape[0]):
            image_channel
            logger.info(f'Processing channel {image_channel} pixels')
            # collect only one channel
            image_array = img[image_channel, :, :]
            # for each cell, collect cell, nuc, cyto pixels
            cells = []
            for cell_number, mask_array in masks[image_name].items():
                cell_number
                # collect pixels and coords
                cell_pixels = pd.concat([pixel_collector(image_array, mask_array[:, :, i]) for i, mask_type in enumerate(['cell'])])
                # add identifiers
                cell_pixels['cell_number'] = cell_number
                cell_pixels.rename(columns={'intensity': f'channel_{image_channel}'}, inplace=True)
                cells.append(cell_pixels)
            channels.append(pd.concat(cells))
        channels = functools.reduce(lambda left, right: pd.merge(left, right, on=['x', 'y', 'cell_number'], how='outer'), channels)
        channels['image_name'] = image_name
            
        pixel_information[image_name] = channels
    except:
        logger.info(f'{image_name} not processed as no mask found')
logger.info('Completed pixel collection')

# ----------------save arrays----------------
saved = [df.to_csv(f'{output_folder}{image_name}.csv') for image_name, df in pixel_information.items()]
