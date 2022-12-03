#!/usr/bin/env python3

import time

from PIL import ImageGrab
import numpy as np
import cv2 as cv

cv2 = cv

screenW = 1300
screenH = 600

def invImg(img) :
    return cv2.bitwise_not(img)


def mserImg(img, bgImg) :
    
    
    imgInput = img 
    mser = cv2.MSER_create(
        edge_blur_size = 1
        )
    regions, _ = mser.detectRegions(imgInput)
    
    imgOutput = bgImg
    
    for p in regions:
        xmax, ymax = np.amax(p, axis=0)
        xmin, ymin = np.amin(p, axis=0)
        cv2.rectangle(imgOutput, (xmin,ymax), (xmax,ymin), (0, 0, 180), 1)
    
    return imgOutput, regions
    



def main():
    
    
    ss_img = ImageGrab.grab((0, 0, screenW, screenH))
    ss_img.save("/tmp/s.jpg")

    imgOrig = np.asarray(ss_img)
    imgGray = cv2.cvtColor(imgOrig, cv2.COLOR_BGR2GRAY)
    imgThrW = cv2.adaptiveThreshold(imgGray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY , 3 ,  3)
    cv2.imwrite('/tmp/2thrw.png' , imgThrW)
    
    worb_input = 'w'  # w or b
    
    if worb_input == 'w':
        imgUsedForDlting = invImg ( imgThrW )
    
    imgDlt = cv.dilate( imgUsedForDlting, cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3,1)) )
    cv2.imwrite('/tmp/3dlt.png' , imgDlt)
    
        
    imgCls = cv2.morphologyEx(imgDlt, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3,1)) )
    cv2.imwrite('/tmp/4cls.png' , imgCls)
    
 



    imgMser, regions = mserImg(invImg(imgCls) , imgOrig)
    
    print( len (regions) )
    
    
if __name__ == '__main__':
    main()
    
