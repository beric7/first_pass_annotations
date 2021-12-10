# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 14:20:49 2021

@author: Admin
"""

from mask_to_ohev import*
import os

mask_dir = './sample_data/masks/'
ohev_dest = './ohev/'

if not os.path.exists(ohev_dest): # if it doesn't exist already
    os.makedirs(ohev_dest)

for mask in os.listdir(mask_dir):
    input_mask_path = mask_dir + mask
    mask_name = os.path.basename(mask).split('.')[0]
    mask_to_ohev(input_mask_path, mask_name, ohev_dest)

