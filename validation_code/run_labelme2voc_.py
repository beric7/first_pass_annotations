# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 12:25:00 2020

@author: Eric Bianchi
"""

import sys

from labelme2voc_ import createMasks
# from image_utils import extension_change

input_dir = './PATH TO FOLDER OF BOTH IMAGES AND JSON FILES/'
output_dir = './output_files/VOC_output/'

# THIS MUST BE CHANGED TO LABELS GIVEN
label_txt_file = 'labels_corrosion_segmentation_.txt'

createMasks(input_dir, output_dir, label_txt_file)