#!/usr/bin/env python3

# Licensed under GPL 3.0
# Copyright Garywill (github.com/garywill)   
#   copyright 2023 - 



# --------------------------

 

# for debug not cover whole screen
screenW = 1300
screenH = 500
# enable 'fetch_screen_size' in main() if you want it to cover whole screen


fontsize = 10

# whether to do a click after moving the mouse cursor to a position
autoClick = True
# the window need some time to disappear
autoClickDelay = 0.3 # unit: second


# --------------------------


import time
from pynput import keyboard
from pynput.mouse import Button, Controller
mouse = Controller()

import numpy as np
import cv2 as cv
cv2 = cv


from PIL import ImageGrab, ImageTk
import tkinter as tk




keyListener = None


wdShow = False
wd = None
imgScrn = None
imgTk = None
canvas = None


startKeysStatus = 0
clickKeysStatus = 0


showingScreen = False



regions = []
LC = 0
keypList = []


prsdKeys = []
keypListFiltered = []




letterList = list('ABCDEFGHJKLMNOPQRSTUVWXYZ234789[;/')



def main():
    global wd, wdShow
    
    # uncomment this to do for whole screen
    # fetch_screen_size()
    
    print("creating window..")
    createWindow(screenW, screenH)
    print("hiding window..")
    _hideWindow()
    
    print("starting key listener..")
    keyListenerStart(False)
    
    print("listening")
    
    lastWdShow = wdShow
    while True :
        time.sleep(0.05)
        if lastWdShow != wdShow and wd :
            if wdShow :
                _showWindow()
            else:
                _hideWindow()
                
        lastWdShow = wdShow
        

def keyListenerStart(suppress=False) :
    global keyListener
    
    keyListener = keyboard.Listener( on_press=on_press, on_release=on_release, suppress = suppress)
    keyListener.start()

def keyListenerStop() :
    global keyListener
    keyListener.stop()

def resetKeyPrsd() :
    global  prsdKeys, keypListFiltered
    print("resetKeyPrsd()")
    prsdKeys = []
    keypListFiltered = keypList
    
def processKeyChar(char) :
    global LC
    global prsdKeys, keypListFiltered
    
    print("\n\nprocessKeyChar() char=%s" % char)
    char = char.upper()
    
    prsdKeys.append(char)
    print(prsdKeys)
    
    N = len(prsdKeys)-1
    keypListFiltered = [x for x in keypListFiltered if x['keyp'][N] == char]
    # print("\n keypListFiltered:")
    # print(keypListFiltered)
    print( len(keypListFiltered) )
    
    if not len(keypListFiltered) > 0 :
        resetKeyPrsd()
    
    if len(keypListFiltered) == 1  :
        print("hasMatch")
        
        matchKeyp = keypListFiltered[0]
        print(matchKeyp)
        
        keyListenerStop()
        
        
        x = matchKeyp['cord'][0]
        y = matchKeyp['cord'][1]
        mouse.position = (x, y)
        
        screen_away()
        
        resetKeyPrsd()
        
        keyListenerStart(False)
        
        time.sleep(autoClickDelay)
        if autoClick :
            do_click()
        
    
    if len(prsdKeys) >= LC :
        print( "presKeys len >= max")
        resetKeyPrsd()
        return


def on_press(key):
    global startKeysStatus, clickKeysStatus, showingScreen
    
    if not showingScreen and ( key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l ) and startKeysStatus == 0 :
        startKeysStatus = 1
    elif not showingScreen and startKeysStatus == 1 and key == keyboard.Key.cmd  :
        keyListenerStop()
        screen_do()
        startKeysStatus = 0
        keyListenerStart(True)
        return
        
    if key == keyboard.Key.cmd and clickKeysStatus == 0 and not showingScreen :
        clickKeysStatus = 1
    elif clickKeysStatus == 1 and ( key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l )  and not showingScreen:
        clickKeysStatus = 2
        return
        
        
    if key == keyboard.Key.esc and showingScreen :
        keyListenerStop()
        screen_away()
        keyListenerStart(False)
        return
    
    if showingScreen :
        char = 0
        try:
            char = key.char
        except:
            # print("key no char")
            pass
    
        if char :
            processKeyChar(char)
    

def on_release(key):
    global startKeysStatus, clickKeysStatus, showingScreen
    
    if clickKeysStatus == 2 and ( key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l ) and not showingScreen :
        do_click()
        clickKeysStatus = 0
        
    startKeysStatus = 0
    
    if key != keyboard.Key.cmd :
        clickKeysStatus = 0




def putLabel(text,   x, y,  canvas=None) :
    text_item = canvas.create_text(x, y , text=text, fill='#000000', font=('"" %d bold' % fontsize))
    bbox = canvas.bbox(text_item)
    rect_item = canvas.create_rectangle(bbox, fill="#f3e48c", outline="#0000ff")
    canvas.tag_raise(text_item,rect_item)
    # return label


def destroyWindow () :
    print("destroyWindow()")
    global showingScreen, keypList
    global wd
    
    
    showingScreen = False
    keypList = []
    
    if wd :
        wd.destroy()
        wd=None
    else :
        print("no wd")
    
def showWindow() :
    global wdShow
    wdShow = True
    
def hideWindow() :
    global wdShow
    wdShow = False

    
def _hideWindow() :
    wd.withdraw()
    canvas.delete('all')
    
def _showWindow() :
    global keypList
    global imgScrn,  imgTk, canvas
    
    imgTk = ImageTk.PhotoImage(imgScrn)
    canvas.create_image(0, 0, image=imgTk, anchor=tk.NW)

    for kpc in keypList :
        putLabel(''.join(kpc['keyp']) ,  kpc['cord'][0] ,  kpc['cord'][1] , canvas = canvas)

    wd.update()
    wd.deiconify()
    wd.update()
    
def createWindow(w, h) :
    global wd, canvas
    wd = tk.Tk()

    wd.overrideredirect(True) # no border
    wd.geometry("%dx%d" % (w,h ) )
    
    canvas = tk.Canvas(wd, width= screenW, height= screenH)
    canvas.place(x=0, y=0)

    wd.attributes('-topmost', 1)
    wd.attributes('-alpha', 0.7)
    wd.wait_visibility(wd)
    wd.wm_attributes('-alpha',0.7)
    


def invImg(img) :
    return cv2.bitwise_not(img)


def mserImg(img, bgImg) :
    # int  	delta = 5,
    # int  	min_area = 60,
    # int  	max_area = 14400,
    # double  	max_variation = 0.25,
    # double  	min_diversity = .2,
    # int  	max_evolution = 200,
    # double  	area_threshold = 1.01,
    # double  	min_margin = 0.003,
    # int  	edge_blur_size = 5 
    
    imgInput = img 
    mser = cv2.MSER_create(
        # delta = 40,
        # min_area = 4,
        # max_area = 80000,
        # # max_variation = max_variation,
        # # min_diversity = .02,
        # # max_evolution = 20000,
        # # # area_threshold = area_threshold,
        # # min_margin = 0.00003,
        edge_blur_size = 1
        )
    regions, _ = mser.detectRegions(imgInput)
    
    imgOutput = bgImg
    
    for p in regions:
        xmax, ymax = np.amax(p, axis=0)
        xmin, ymin = np.amin(p, axis=0)
        cv2.rectangle(imgOutput, (xmin,ymax), (xmax,ymin), (0, 0, 180), 1)
    
    return imgOutput, regions
    





def do_click() :
    print("do_click()")
    mouse.click(Button.left, 1)


def screen_away() :
    global showingScreen
    showingScreen = False
    hideWindow()
    resetKeyPrsd()
    resetRegions()

def screen_do() :
    global showingScreen
    global imgScrn
    
    showingScreen = True

    resetKeyPrsd()
    
    imgScrn = ImageGrab.grab((0, 0, screenW, screenH))
    
    imgOrig = np.asarray(imgScrn)
    imgGray = cv2.cvtColor(imgOrig, cv2.COLOR_BGR2GRAY)
    
    #  C>0 以 白底黑字 方式做二值 输出是 白底黑字+反色的被描边
    imgThrW = cv2.adaptiveThreshold(imgGray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY , 3 ,  3)
    
    # C<=0 以 黑底白字 方式做二值 输出是 黑底白字+反色的被描边
    # imgThrB = cv2.adaptiveThreshold(imgGray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY , 3 ,  -3)
    
    # 输入 是 白底黑字(w) or 黑底白字(b)
    worb_input = 'w'  # w or b
    
    if worb_input == 'w':
        imgUsedForDlting = invImg ( imgThrW )
    else :
        imgUsedForDlting = imgThrB
    
    # cv.dilate 默认情况下应 输入 黑底白字 的图 输出也是 黑底白字
    imgDlt = cv.dilate( imgUsedForDlting, cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3,1)) )
        
    # 默认情况closing操作应输入 黑底白字 的图 输出也是 黑底白字
    imgCls = cv2.morphologyEx(imgDlt, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(3,1)) )

    imgMser, regions = mserImg(invImg(imgCls) , imgOrig)
    
    updateRegions(regions)
    showWindow()
    
def updateRegions(newRegions) :    
    global regions, LC, keypList, keypListFiltered
    regions = newRegions
    print( len (regions) )
    LC = 0
    for LC in range(1, 10) :
        if pow( len(letterList) , LC) >= len(regions) :
            break
    print(LC)
    keypList = []
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
        # print("i=%d, keyp=%s" % (i, ''.join(keyp) ) )
    keypListFiltered = keypList
    
    
def resetRegions() :
    global LC , regions, keypList, keypListFiltered
    LC = 0
    regions = []
    keypList = []
    keypListFiltered = keypList


def fetch_screen_size() :
    global screenW, screenH
    root = tk.Tk()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    screenW = w
    screenH = h
    root.destroy();


if __name__ == '__main__':
    main()
    
