# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 19:19:56 2021

@author: Admin
"""
import json

def check_null(value):
    if value == 'null':
        value = None
    else:
        value = value
        
    return value


def text_to_json(destination, text_file):
    dictionary = {}
    shape_dict = {}
    
    with open(text_file) as tr:
        for line in tr:
            key,data = line.strip().split(":",1)
            # print(key, " = ", data)
            if key == "version":
                dictionary[key] = data
            elif key == "shapes":
                dictionary.setdefault("shapes",[])
            elif key == "points":
                ## TODO fix points to be int instead of string
                #data = data.replace("[", "").replace("]", "")
                points_list = data.replace("[","").split("]")
                points_list.pop()
                points = []
                for item in points_list:
                    x,y = item.split(",")
                    points.append([float(x),float(y)])
                shape_dict[key] = points
            elif key == "group_id":
                shape_dict[key] = check_null(data)
            elif key == "flags":
                # shape_dict[key] = data
                shape_dict[key] = {}
                dictionary["shapes"].append(shape_dict)
                shape_dict = {}
            elif key == "imagePath":
                dictionary[key] = data
            elif key == "imageData":
                dictionary[key] = check_null(data)
            elif key == "imageHeight":
                dictionary[key] = int(data)
            elif key == "imageWidth":
                dictionary[key] = int(data)
            else:
                shape_dict[key] = data
            
        out_file = open(destination, "w") 
        json.dump(dictionary, out_file, indent = 4, sort_keys = False)
        out_file.close() 