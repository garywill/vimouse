#!/usr/bin/env python3

import time

from PIL import ImageGrab


screenW = 1300
screenH = 600


def main():
    
    
    ss_img = ImageGrab.grab((0, 0, screenW, screenH))
    ss_img.save("/tmp/s.jpg")

 
    
if __name__ == '__main__':
    main()
    
