#!/usr/bin/env python3

import time
from pynput import keyboard

import numpy as np
import cv2 as cv

cv2 = cv

from PIL import ImageGrab, ImageTk
import tkinter as tk

from pynput.mouse import Button, Controller

mouse = Controller()

screenW = 1300
screenH = 600
wd = None

letterList = list('ABCDEFGHJKLMNOPQRSTUVWXYZ234789[;/')

keypList = []
LC = 0

prsdKeys = []
keypListFiltered = []

def main():
    
    # fetch_screen_size()
    
    keyListener = keyboard.Listener( on_press=on_press, on_release=on_release)
    keyListener.start()
    
    global wd
    while True :
        time.sleep(9)

def resetKeyPrsd() :
    print("resetKeyPrsd()")
    global  prsdKeys, keypListFiltered
    prsdKeys = []
    keypListFiltered = keypList
    
def processKeyChar(char) :
    print(char)
    global  prsdKeys, keypListFiltered
    char = char.upper()
    
    prsdKeys.append(char)
    print(prsdKeys)
    
    hasMatch = False
    matchKeyp = None
    
    N = len(prsdKeys)-1
    
    keypListFiltered = [x for x in keypListFiltered if x['keyp'][N] == char]
    # print("\n keypListFiltered:")
    # print(keypListFiltered)
    print( len(keypListFiltered) )
    
    if not len(keypListFiltered) > 0 :
        resetKeyPrsd()
    
    if len(keypListFiltered) == 1  :
        hasMatch = True
        matchKeyp = keypListFiltered[0]
    
        print("hasMatch")
        print(matchKeyp)
        
        destroyWindow()
        
        resetKeyPrsd()
        
        x = matchKeyp['cord'][0]
        y = matchKeyp['cord'][1]
        mouse.position = (x, y)
        



def fetch_screen_size() :
    global screenW, screenH
    root = tk.Tk()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    screenW = w
    screenH = h
    root.destroy();

def putLabel(text,   x, y, window=None, canvas=None) :
    
    text_item = canvas.create_text(x, y , text=text, fill='#000000', font=('"" 10 bold'))
    bbox = canvas.bbox(text_item)
    rect_item = canvas.create_rectangle(bbox, fill="#f3e48c", outline="#0000ff")
    canvas.tag_raise(text_item,rect_item)
    # return label


def destroyWindow () :
    print("destroyWindow()")
    global showingKeyps, keypList
    global wd
    showingKeyps = False
    keypList = []
    try:
        wd.destroy()
        wd=None
    except:
        # print("ERROR destroying window")
        pass
    
def createWindow(w, h) :

    root = tk.Tk()

    root.overrideredirect(True) # no border
    root.geometry("%dx%d" % (w,h ) )


    root.attributes('-topmost', 1)
    root.attributes('-alpha', 0.7)
    root.wait_visibility(root)
    root.wm_attributes('-alpha',0.7)
    
        
    return root


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
    


startKeysStatus = 0
showingKeyps = False

clickKeysStatus = 0

def on_press(key):
    global startKeysStatus, clickKeysStatus, showingKeyps
    global wd
    global keypList
    
    if key == keyboard.Key.ctrl and startKeysStatus == 0 :
        startKeysStatus = 1
    elif startKeysStatus == 1 and key == keyboard.Key.cmd  :
        screen_do()
        showingKeyps = True
        startKeysStatus = 0
        return
        
    if key == keyboard.Key.cmd and clickKeysStatus == 0 and not showingKeyps :
        clickKeysStatus = 1
    elif clickKeysStatus == 1 and key == keyboard.Key.ctrl  and not showingKeyps:
        clickKeysStatus = 2
        return
        
        
    if key == keyboard.Key.esc and wd != None :
        wd.update()
        destroyWindow()
        return
    
    if showingKeyps :
        char = 0
        try:
            char = key.char
        except:
            # print("key no char")
            pass
    
        if char :
            processKeyChar(char)
    

def on_release(key):
    global startKeysStatus, clickKeysStatus, showingKeyps
    
    if clickKeysStatus == 2 and key == keyboard.Key.ctrl and not showingKeyps :
        do_click()
        clickKeysStatus = 0
        
    startKeysStatus = 0
    
    if key != keyboard.Key.cmd :
        clickKeysStatus = 0


def do_click() :
    print("do_click()")
    mouse.click(Button.left, 1)




def screen_do() :
    global keypList, keypListFiltered , LC
    global wd
    
    try:
        destroyWindow()
    except:
        pass
    
    
    
    ss_img = ImageGrab.grab((0, 0, screenW, screenH))
    ss_img.save("/tmp/s.jpg")

    imgOrig = np.asarray(ss_img)
    imgGray = cv2.cvtColor(imgOrig, cv2.COLOR_BGR2GRAY)
    
    #  C>0 以 白底黑字 方式做二值 输出是 白底黑字+反色的被描边
    imgThrW = cv2.adaptiveThreshold(imgGray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY , 3 ,  3)
    cv2.imwrite('/tmp/2thrw.png' , imgThrW)
    
    # 输入 是 白底黑字(w) or 黑底白字(b)
    worb_input = 'w'  # w or b
    
    if worb_input == 'w':
        imgUsedForDlting = invImg ( imgThrW )
    else :
        imgUsedForDlting = imgThrB
    
    # cv.dilate 默认情况下应 输入 黑底白字 的图 输出也是 黑底白字
    imgDlt = cv.dilate( imgUsedForDlting, cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3,1)) )
    cv2.imwrite('/tmp/3dlt.png' , imgDlt)
    
        
    # 默认情况closing操作应输入 黑底白字 的图 输出也是 黑底白字
    imgCls = cv2.morphologyEx(imgDlt, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3,1)) )
    cv2.imwrite('/tmp/4cls.png' , imgCls)
    
 



    imgMser, regions = mserImg(invImg(imgCls) , imgOrig)
    
    print( len (regions) )
    
    LC = 0
    for LC in range(1, 10) :
        if pow( len(letterList) , LC) >= len(regions) :
            break
        
    print(LC)
    
    keypList = []
    
    
    wd = createWindow(screenW, screenH)
    
    wdBgImg = ImageTk.PhotoImage(ss_img)
    
    canvas = tk.Canvas(wd, width= screenW, height= screenH)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, image=wdBgImg, anchor=tk.NW)
    
    for i in range(0, len(regions) ) :
        p = regions [i]
        
        xmax, ymax = np.amax(p, axis=0)
        xmin, ymin = np.amin(p, axis=0)
        
        pointX = (xmax+xmin)/2
        pointY = (ymax+ymin)/2
    
        keyp = []
        for j in range(0, LC) :
            l = str ( letterList[ int( i / pow( len(letterList), j) ) % pow( len(letterList), j+1) ] ) 
                
            keyp.insert (0, l)
            
        
        keypList.append( {
            "keyp": keyp, 
            "cord": [pointX, pointY]
            } )
        putLabel(''.join(keyp) ,  pointX , pointY , canvas = canvas)
        # putLabel(str(i) , wd, (xmax+xmin)/2, (ymax+ymin)/2 )
        # print("i=%d, keyp=%s" % (i, ''.join(keyp) ) )
    
    keypListFiltered = keypList
    wd.update()
    # print(keypList)
    # wd.mainloop()
    
if __name__ == '__main__':
    main()
    
