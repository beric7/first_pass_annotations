# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 10:23:17 2021

@author: Eric Bianchi
"""

import cv2
import numpy as np
import torch
import os
from trim_contour import dce

def un_pad_contour(contour):
    contour = contour - 5
    return contour
        
def centeroidnp(arr):
    length = arr.shape[0]
    arr = arr.squeeze(1)
    x = arr[:, 0]
    y = arr[:, 1]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return sum_x/length, sum_y/length

def closest_node(node, nodes):
    dist_2 = np.sum((nodes - node)**2, axis=1)
    index = np.argmin(dist_2)
    return index


def isolate_color(mask, class_coloring):
    
    # image, expects a jpeg, but could be modified for a png...
    target = torch.from_numpy(mask)

    channels, height, width = mask.shape

    new_bn = np.zeros((1, mask.shape[1], mask.shape[2]))
    new_bn[mask == class_coloring] = class_coloring
    numpy_img = np.asarray(new_bn, dtype=np.uint8)
    numpy_img = numpy_img.squeeze(0)
    _, bin_img =  cv2.threshold(numpy_img, 0, 255, cv2.THRESH_BINARY)

    return bin_img

def contour_class(ohev_file_name, image_file_name, destination, image_name, class_coloring, class_name):
    
    if not os.path.exists(destination): # if it doesn't exist already
        os.makedirs(destination)

    image_name = image_name.split('.')[-2]
    image_name_with_class = class_name + '_' + image_name 
    
    # isolate the colors
    np_binary_mask_prep = np.load(ohev_file_name) # convert from tensor to numpy
    isolated_binary_mask = isolate_color(np_binary_mask_prep, class_coloring)
    color_image = cv2.imread(image_file_name)
    img_padded = cv2.copyMakeBorder(isolated_binary_mask, 5, 5, 5, 5, cv2.BORDER_CONSTANT)
    original_color_image = cv2.copyMakeBorder(color_image, 5, 5, 5, 5, cv2.BORDER_CONSTANT)
    
    # Contours:
    contours, hierarchy = cv2.findContours(img_padded, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    try: 
        hierarchy = hierarchy.squeeze(0)
        # Contours: 
        # -1 signifies drawing all contours 
        # cv2.drawContours(img_padded, contours, -1, (255, 255, 0), 1) 
        
        # dictionary of parent contours
        parent_contours = {}
        for i in range(len(contours)):
            if hierarchy[i][3] < 0:
               parent_contours.update({i:contours[i]})
    
        parent_holes_dict = {}
        for i in parent_contours:
            holes_temp = []
            for ii in range(len(hierarchy)):
                if hierarchy[ii][3] == i:
                    holes_temp.append(contours[ii])
            try: 
                parent_holes_dict.update({i:holes_temp})
            except:
                continue
            
        complete_contours = []
        for i in parent_contours:
            holes = parent_holes_dict[i]
            parent_contour = parent_contours[i]
            new_contour_path_, img_padded = add_child_contours(parent_contour, holes, img_padded)
            new_contour_path_ = un_pad_contour(new_contour_path_)
            
            if len(new_contour_path_) > 2:
                trimmed_contour = dce(new_contour_path_)
                complete_contours.append(trimmed_contour)
             
        img_unpadded = original_color_image[5:(original_color_image.shape[0]-5),5:(original_color_image.shape[1]-5)]
        cv2.drawContours(img_unpadded, complete_contours, -1, (128, 128, 0), 1)
        cv2.imwrite(destination + image_name_with_class + '.png',img_unpadded)
        
        # print("Number of Contours found = " + str(len(contours))) 
        centered_contours = complete_contours 
        return complete_contours
    except:
        return None
    
def add_child_contours(parent_contour, holes, img_padded):
    centroid_list = []
    for hole in holes:
        centroid = centeroidnp(hole)
        centroid_list.append((centroid[0], centroid[1]))
    
    # create a list of nodes which are closest to the centroids of the sub-contours.
    exterior_node_list = []
    exterior_coord_list = []
    parent_contour = np.asarray(parent_contour).squeeze(1)
    for centroid in centroid_list:
        node_number = closest_node(centroid, parent_contour)
        exterior_node_list.append(node_number)
        exterior_coord_list.append(parent_contour[node_number])
    
    # create a list of the nodes which are closest to identified exterior nodes. 
    interior_node_list = []
    interior_coord_list = []
    for i in range(len(exterior_node_list)):
        hole = np.asarray(holes[i]).squeeze(1)
        node_number = closest_node(parent_contour[exterior_node_list[i]], hole)
        interior_node_list.append(node_number)
        interior_coord_list.append(hole[node_number])
    # Show on image
    # =========================================
    # loop through and make the 'mega' contour by attaching any interior contour 
    # to the exterior contour
    for i in range(len(interior_node_list)): 
        coord = holes[i][interior_node_list[i]]
         #print(coord[0])
        img_padded = cv2.circle(img_padded, (coord[0][0], coord[0][1]), 3, [255,255,255], -1)
    
    # loop through and make the 'mega' contour by attaching any interior contour 
    # to the exterior contour
    for point in exterior_node_list:  
        coord = parent_contour[point]
        img_padded = cv2.circle(img_padded, (coord[0], coord[1]), 3, [255,255,255], -1)
    
    # cv2.imwrite('IMG_7315_contour_locations.png',img_padded)
    # =========================================
    
    from itertools import islice, dropwhile, cycle
    import pandas as pd
    
    combined = list(zip(exterior_node_list, exterior_coord_list, interior_node_list, interior_coord_list, holes))
    coordinate_pairs = pd.DataFrame(combined, columns = ['exterior_index',
                                                         'exterior_coordinates',
                                                         'interior_index',
                                                         'interior_coordinates', 
                                                         'interior_list'])
    
    coordinate_pairs_sorted = coordinate_pairs.sort_values(by=['exterior_index'])
    coordinate_pairs_sorted = coordinate_pairs_sorted.reset_index()
    # print(coordinate_pairs_sorted.head())
    
    new_contour_path = []
    count = 0
    g = len(parent_contour)
    for i in range(len(parent_contour)):
        # print(i)
        try:
            if i == coordinate_pairs_sorted['exterior_index'][count]:
                # print(count)
                # print(coordinate_pairs_sorted['exterior_index'][count])
                coordinate = parent_contour[i]
                # t = np.expand_dims(np.asarray(coordinate), axis=0)
                new_contour_path.append(np.asarray(np.expand_dims(np.asarray(coordinate), axis=0))) # initialize starting position
                hole_coord_list = coordinate_pairs_sorted['interior_list'][count]
                start_position = coordinate_pairs_sorted['interior_index'][count]
                cycled_hole_list = [] 
                for iii in range(len(hole_coord_list)): 
                    cycled_hole_list.append(hole_coord_list[start_position % len(hole_coord_list)]) 
                    start_position = start_position + 1
                for ii in range(len(cycled_hole_list)):
                    new_contour_path.append(np.expand_dims(np.asarray(cycled_hole_list[ii]), axis=0)) 
                end_coord_position = coordinate_pairs_sorted['interior_coordinates'][count]
                new_contour_path.append(np.expand_dims(np.asarray(end_coord_position), axis=0))
                start_exterior_position = coordinate_pairs_sorted['exterior_coordinates'][count]
                new_contour_path.append(np.expand_dims(np.asarray(start_exterior_position), axis=0))
                count = count + 1   
            else:
                coordinate = parent_contour[i]
                new_contour_path.append(np.expand_dims(np.asarray(coordinate), axis=0))
        except:
            coordinate = parent_contour[i]
            new_contour_path.append(np.expand_dims(np.asarray(coordinate), axis=0))
            
    # np.asarray(new_contour_path, dtype=np.float32)
    new_contour_path_ = np.zeros((len(new_contour_path),1,2), dtype='int32')
    for i in range(0,len(new_contour_path)):
        new_contour_path_[i] = new_contour_path[i]
    new_contour_path_ = np.asarray(new_contour_path_)

    return new_contour_path_, img_padded