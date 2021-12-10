# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 19:04:04 2021

@author: Admin
"""
import os
import cv2
from contouring_semantic_segmentation import*
from txt_to_json import text_to_json
from keypoints_to_txt import keypoints_to_text
from tqdm import tqdm

# ignore the background since we do not want to contour the background!
# This assumes that it is jpeg
class_dictionary = {'fair':1, 'poor':2, 'severe':3}

def make_ohev_list(one_hot_encoded_vector_dir):
    ohev_list_array = []
    for image_name in os.listdir(one_hot_encoded_vector_dir):
        ohev_list_array.append(image_name)
    return ohev_list_array

ohev_directory = './sample_data/ohev/'
image_dir = './sample_data/Masks/'
destination = './output_files/contours_3_pass/'
text_dest = './output_files/text_3_pass/'
json_dest = './output_files/json_3_pass/'
AREA = True

# NUMBER OF DCE PASSES, WE RECCOMEND (3) IF NOT MORE...
# EACH DCE PASS REDUCES THE NUMBER OF POINTS BY 1/2, UNLESS THE AREA CHANGES
# TOO MUCH (if the original area changes by 5%).
dce_pass = 3

if not os.path.exists(text_dest): # if it doesn't exist already
    os.makedirs(text_dest)

if not os.path.exists(json_dest): # if it doesn't exist already
    os.makedirs(json_dest)


ohev_list_array = make_ohev_list(ohev_directory)

# expects a jpeg for the image file-type, but could easily be modified for a png
for image_name in tqdm(ohev_list_array): 
    complete_contours = {}
    ohev_file_name = ohev_directory + image_name
    image_file_name = image_dir + image_name.split('.')[-2]+'.png'
    for class_name in class_dictionary:
        complete_class_contours = contour_class(dce_pass, ohev_file_name, image_file_name, destination, image_name, class_dictionary[class_name], class_name, AREA)
        if complete_class_contours == None:
            # print(class_name + ': not present on image')
            continue
        else:
            complete_contours[class_name] = complete_class_contours
    # ------------------------------------------------------------------------   
    # TODO:
    # CONVERT complete_contours TO JSON
    # ------------------------------------------------------------------------
    #print(complete_contours)
    img = cv2.imread(image_file_name)
    base_image_name = image_name.split('.')[-2]
    
    base_image_name_jpeg = base_image_name + '.jpeg'
    output_textfile_destination = text_dest + base_image_name+".txt"
    
    keypoints_to_text(output_textfile_destination, complete_contours, img, base_image_name_jpeg)
    text_to_json(json_dest + base_image_name+".json", output_textfile_destination)
    
        
    