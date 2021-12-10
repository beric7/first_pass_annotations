# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 13:17:04 2021

@author: Eric Bianchi
"""
import math
import numpy as np

def GaussArea(pts):  
    length = len(pts)
    p1 = 0
    p2 = 0
    
    for i in range(0,length-1):
        pt1 = pts[i][0]
        pt2 = pts[i+1][1]
        
        p1 = (pt1*pt2) + p1
        
    for i in range(0,length-1):
        pt3 = pts[i+1][0]
        pt4 = pts[i][1]
        
        p2 = (pt3*pt4) + p2
    
    ptFinal1 = pts[i+1][0]
    ptFinal2 = pts[0][1]
    pFinal1 = ptFinal1*ptFinal2
    
    ptFinal3 = pts[0][0]
    ptFinal4 = pts[i+1][1]
    pFinal2 = ptFinal3*ptFinal4
    
    p1 = p1 + pFinal1
    p2 = p2 + pFinal2
        
    p3 = abs(p1 - p2)

        
    area = 0.5*p3   
    return area;

def onePassDCE(ctrIn):
    k = np.zeros((len(ctrIn)), dtype=np.float64)
    trimmedContour = []
    length = len(ctrIn)-1
    for i in range (0,len(ctrIn)):
        
        if (i == 0):
            x1Diff = ctrIn[length][1] - ctrIn[i][1]
            y1Diff = ctrIn[length][0] - ctrIn[i][0]
            x2Diff = ctrIn[i][1] - ctrIn[i+1][1]
            y2Diff = ctrIn[i][0] - ctrIn[i+1][0]
            
            y0 = ctrIn[length][0]
            y1 = ctrIn[i][0]
            y2 = ctrIn[i+1][0]
            
            x0 = ctrIn[length][1]
            x1 = ctrIn[i][1]
            x2 = ctrIn[i+1][1]
        elif (0 < i < len(ctrIn)-1):
            x1Diff = ctrIn[i-1][1] - ctrIn[i][1]
            y1Diff = ctrIn[i-1][0] - ctrIn[i][0]
            x2Diff = ctrIn[i][1] - ctrIn[i+1][1]
            y2Diff = ctrIn[i][0] - ctrIn[i+1][0]
            
            y0 = ctrIn[i-1][0]
            y1 = ctrIn[i][0]
            y2 = ctrIn[i+1][0]
            
            x0 = ctrIn[i-1][1]
            x1 = ctrIn[i][1]
            x2 = ctrIn[i+1][1]
        else:
            x1Diff = ctrIn[i-1][1] - ctrIn[i][1]
            y1Diff = ctrIn[i-1][0] - ctrIn[i][0]
            x2Diff = ctrIn[i][1] - ctrIn[0][1]
            y2Diff = ctrIn[i][0] - ctrIn[0][0]
            
            y0 = ctrIn[i-1][0]
            y1 = ctrIn[i][0]
            y2 = ctrIn[0][0]
            
            x0 = ctrIn[i-1][1]
            x1 = ctrIn[i][1]
            x2 = ctrIn[0][1]
                
        L_1 = ((x1Diff)**2+(y1Diff)**2)**0.5
        L_2 = ((x2Diff)**2+(y2Diff)**2)**0.5        
                    
        atan1 = math.atan2((y1-y0),(x1-x0))
        atan2 = math.atan2((y2-y1),(x2-x1))
        
        rot_i =  atan1 - atan2                              
        
        k_i = abs(rot_i*L_1*L_2)/(L_1+L_2)
        
        k[i] = k_i
    minVal = np.amin(k, axis=0)
    
    for i in range(0, len(k)):
        if k[i] == minVal:
            minVal = -1
        else:
            trimmedContour.append([ctrIn[i][0], ctrIn[i][1]])
    return trimmedContour

def convert_contour_to_list(contour):
    list_array = []
    temp_list = []
    for i in range(0,len(contour)):
        temp_list = [contour[i][0][0], contour[i][0][1]]
        list_array.append(temp_list)
    
    return list_array

def list_to_contour(list_array):
    contour = np.zeros((len(list_array), 1, 2), dtype=np.int32)
    for i in range(0, len(list_array)):
        contour[i][0][0] = list_array[i][0]
        contour[i][0][1] = list_array[i][1]
    
    return contour

def dce_area(dce_pass, contour_cv2):
    contour = convert_contour_to_list(contour_cv2)
    original_area = GaussArea(contour)
    #condition = True
    for step in range(dce_pass):
        numLoops = math.floor(len(contour)/2)
        if numLoops >= 2:
            for idx in range(numLoops):
                contour_temp = contour
                # print("Original area: ", original_area)
                contour = onePassDCE(contour)
                new_area = GaussArea(contour)
                # print("New area: ", new_area)
                percent_change = (original_area - new_area) / (original_area)
                if percent_change > 0.1:
                    contour = contour_temp
                    # print("too much change!")
                    break
        # print("STEP "+str(step)+":", numLoops, len(contour), GaussArea(contour))
    return list_to_contour(contour)