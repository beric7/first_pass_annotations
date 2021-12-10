# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 14:09:05 2021

@author: Admin
"""
from tqdm import tqdm
import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, jaccard_score, confusion_matrix
import numpy as np
import os
import cv2
import itertools
from scipy.sparse import diags

def process_im(image_path):
    
    image = cv2.imread(image_path)
    img = image.transpose(2,0,1)
    
    return img

def mask_to_ohev(input_mask_path, mask_name, ohev_dest):
    
    # image
    input_mask_processed = process_im(input_mask_path)
    input_shape = input_mask_processed.reshape(1,3,512,512)
    _, channels, height, width = input_shape.shape
    input_mask = torch.empty(height, width, dtype=torch.long)
    
    
    mapping = {(0,0,0): 0, (0,0,128): 1, (0,128,0): 2, (0,128,128): 3}
    input = torch.from_numpy(input_mask_processed)
        
    for k in mapping:
         # Get all indices for current class
         idx_input = (input==torch.tensor(k, dtype=torch.uint8).unsqueeze(1).unsqueeze(2))
         
         validx_input = (idx_input.sum(0) == 3)  # Check that all channels match
         
         input_mask[validx_input] = torch.tensor(mapping[k], dtype=torch.long)

    y_input = input_mask.data.unsqueeze(0).cpu().numpy()
    
    np.save(ohev_dest + mask_name + '.npy', y_input)