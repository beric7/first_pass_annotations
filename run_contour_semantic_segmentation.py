# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 19:04:04 2021

@author: Admin
"""
import os
import json
import cv2
from contouring_semantic_segmentation import*
from txt_to_json import*
from keypoints_to_txt import*

# ignore the background since we do not want to contour the background!
# This assumes that it is jpeg
class_dictionary = {'concrete':1, 'steel':2, 'metal decking':3}

output_textfile_destination = "output.txt"


def make_ohev_list(one_hot_encoded_vector_dir):
    ohev_list_array = []
    for image_name in os.listdir(one_hot_encoded_vector_dir):
        ohev_list_array.append(image_name)
    return ohev_list_array

ohev_directory = './ohev/'
image_dir = './masks/'

ohev_list_array = make_ohev_list(ohev_directory)
complete_contours = {}

# expects a jpeg for the image file-type, but could easily be modified for a png
for image_name in ohev_list_array: 
    ohev_file_name = ohev_directory + image_name
    image_file_name = image_dir + image_name.split('.')[-2]+'.png'
    for class_name in class_dictionary:
        complete_class_contours = contour_class(ohev_file_name, image_file_name, image_name, class_dictionary[class_name], class_name)
        if complete_class_contours == None:
            print(class_name + ': not present on image')
        else:
            complete_contours[class_name] = complete_class_contours
    # ------------------------------------------------------------------------   
    # TODO:
    # CONVERT complete_contours TO JSON
    # ------------------------------------------------------------------------
    #print(complete_contours)
    
        
    
    img = cv2.imread(image_file_name)
    keypoints_to_text(output_textfile_destination, complete_contours, img, image_file_name)
    text_to_json("out.json", "output.txt")
    
        
    