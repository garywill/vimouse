#!/usr/bin/env python3

import time

from PIL import ImageGrab


screenW = 1300
screenH = 600


def main():
    
    
    ss_img = ImageGrab.grab((0, 0, screenW, screenH))
    ss_img.save("/tmp/s.jpg")

    imgOrig = np.asarray(ss_img)
    imgGray = cv2.cvtColor(imgOrig, cv2.COLOR_BGR2GRAY)
    imgThrW = cv2.adaptiveThreshold(imgGray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY , 3 ,  3)
    cv2.imwrite('/tmp/2thrw.png' , imgThrW)
    
 
    
if __name__ == '__main__':
    main()
    
