# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 19:19:42 2021

@author: Admin
"""

def keypoints_to_text(destination, keypoints, img, image_file_name):
    #width, height = image.shape[0:2]
    #condense_array_to_oneline = str(keypoints).replace('\n', '').replace(" ", "").replace("'", "").replace("array", "").replace("(", "").replace(")", "")                                
    VERSION_NUMBER = "4.5.6"
    with open(destination, 'w') as f:

        f.write("version:4.5.6\n")
        f.write("shapes:\n")
        for index in keypoints:
            pars = keypoints[index]

            for i in range(len(pars)):
                f.write("label:")
                f.write(index)
                f.write("\n")
                f.write("points:")
                for entry in pars[i]:
                    for x,y in entry:
                        f.write("[")
                        f.write(str(x))
                        f.write(",")
                        f.write(str(y))
                        f.write("]")
                f.write("\n")

                f.write("group_id:null\n")
                f.write("shape_type:polygon\n")
                f.write("flags:{}\n")

        f.write("imagePath:")
        f.write(image_file_name)
        f.write("\n")
        f.write("imageData:")
        f.write('null\n')
        width,height,channels = img.shape
        f.write("imageHeight:")
        f.write(str(height))
        f.write("\n")
        f.write("imageWidth:")
        f.write(str(width))
        f.write("\n")
        f.close()
        
    