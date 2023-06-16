#!/usr/bin/env python3

# Licensed under GPL 3.0
# Copyright Garywill (github.com/garywill)   
#   copyright 2023 - 



# --------------------------

 

# for debug not cover whole screen
screenW = 1300
screenH = 500
# enable 'fetch_screen_size' in main() if you want it to cover whole screen


fontsize = 11

# whether to do a click after moving the mouse cursor to a position
autoClick = True
# the window need some time to disappear
autoClickDelay = 0.1 # unit: second


# --------------------------


import time, sys
from pynput import keyboard
from pynput.mouse import Button, Controller
mouse = Controller()

import numpy as np
import cv2 as cv
cv2 = cv



from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from threading import Thread

keyListener = None


wdapp = None


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
    global wdapp
    
    # uncomment this to do for whole screen
    fetch_screen_size()
    
    print("starting key listener..")
    keyListenerStart(False)
    
    print("listening")
    
    while True :
        try:
            time.sleep(100)

        except KeyboardInterrupt :
            break

    print('trying to exit window')
    try:
        destroyWindow()
    except:
        pass
    
    sys.exit(0)
        

def keyListenerStart(suppress=False) :
    global keyListener
    
    keyListener = keyboard.Listener( on_press=on_press, on_release=on_release, suppress = suppress)
    keyListener.start()
    if suppress:
        print('key listener: NOW BLOCKING KEY EVENTS BEING SENT TO OTHER APPS, until key badges dismiss')

def keyListenerStop() :
    global keyListener
    keyListener.stop()
    print('key listener stop or reset...')

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






def destroyWindow () :
    print("destroyWindow()")
    global showingScreen, keypList
    global wdapp
    
    
    hideWindow()
    
    wdapp.pub_quit.emit()
    wdapp = None

    
def hideWindow() :
    showingScreen = False
    keypList = []
    
    if not wdapp:
        print('ERROR: hideWindow() called but no wdapp')
        return
    
    wdapp.pub_hide.emit()
    

    
def showWindow() :
    print('showWindow()')
    if wdapp:
        wdapp.pub_show.emit()
    else:
        print('create qt thread and qtapplication')
        qtthread = Thread(target=createWindow, args=(screenW, screenH) )
        qtthread.start()
    
    
def createWindow(w,h):        
    global wdapp
    
    if wdapp:
        print('ERROR: createWindow() called but wdapp is not None')
        return
    
    wdapp = WdApp([w, h])
    
    wdapp.pub_show.connect(wdapp.show)
    wdapp.pub_hide.connect(wdapp.hide)
    wdapp.pub_quit.connect(wdapp.slot_quit)
    
    wdapp.pub_show.emit()
    
    wdapp.exec_()
    print('after app.exec_()')


class WdApp(QApplication) :
    pub_show = pyqtSignal()
    pub_hide = pyqtSignal()
    pub_quit = pyqtSignal()
    
    def __init__(self, argv):
        super().__init__([])
        
        self.wd = TransparentWidget(argv[0], argv[1])
        
        
    def hide(self):
        self.wd.hide()
        self.wd.refreshTimer.stop()
        
    def show(self):
        self.wd.refresh()
        self.wd.show()
        self.wd.refreshTimer.start()
        
    def slot_quit(self):
        self.wd.refreshTimer.stop()
        self.wd.close()
        self.quit()


class TransparentWidget(QWidget):
    def __init__(self,w,h):
        print('QWidget subclass __init__', w,h)
        
        super().__init__()
        

        
        
        
        # https://doc.qt.io/qt-5.15/qt.html#WidgetAttribute-enum
        
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.setWindowFlags(Qt.WindowTransparentForInput
                            |Qt.X11BypassWindowManagerHint
                            |Qt.WindowStaysOnTopHint
                            |Qt.FramelessWindowHint
                            # |Qt.WindowDoesNotAcceptFocus
                            |Qt.CoverWindow
                            )
        
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        # self.setAttribute(Qt.WA_AlwaysStackOnTop, True)


        # # # 获取屏幕大小并设置窗口大小
        # screen = QGuiApplication.primaryScreen()
        # if screen is not None:
        #     rect = screen.availableGeometry()
        #     print(rect)
        #     self.setGeometry(rect)
            
        self.setGeometry(QRect(0,0,w,h))
        
        

        # 定时器每秒触发一次重绘
        self.refreshTimer = QTimer(self)
        self.refreshTimer.timeout.connect(self.refresh)
        self.refreshTimer.start(2000)
        
        print('QWidget subclass __init__ finish')

    def refresh(self) :
        print('refresh()')
        self.raise_()
        self.update()
        
        # self.close()
        # self.destroy()
        # self.refreshTimer.stop()
        # QApplication.quit()

    def paintLabel(self, text, x, y):
        qp = QPainter(self)
        
        qp.setFont ( QFont('Arial', fontsize, QFont.Bold) )
        
        metrics = qp.fontMetrics()
        
        w = metrics.width(text)
        h = metrics.height()
        # w=len(text)*8
        h=fontsize
        # print(w,h)
        w_ex = 1
        h_ex = 1
        
        ### pen外，brush内
        
        b_color = QColor(243,228,140, 180) #背景
        r_color = QColor(0,0,255,100) #框
        t_color=QColor(0,0,0, 200) # 字
        
        # 背景
        # qp.setPen(b_color) 
        qp.setBrush(b_color) 
        qp.fillRect( x-w/2-w_ex  , y-h/2-h_ex , w+2*w_ex, h+2*h_ex  , b_color )
        
        # 框
        qp.setPen(r_color)  
        qp.setBrush(Qt.transparent)  
        qp.drawRect( x-w/2-w_ex  , y-h/2-h_ex , w+2*w_ex, h+2*h_ex  )
        
        
        qp.setPen(QPen(t_color))
        qp.setBrush(QBrush(t_color))
        qp.drawText( x-w/2       , y+h/2      ,      text)
        
        
        
        
    def paintEvent(self, event):
        print('QWidget subclass paintEvent')
        
        painter = QPainter(self)
        
        # 绘制矩形网格
        width, height = self.width(), self.height()
        n_rows, n_cols = 5, 6
        n_rows, n_cols = 4, 8
        cell_width, cell_height = width // n_cols, height // n_rows
        pen = QPen(QColor(255,170,0, 127))
        painter.setPen(pen)
        painter.drawRect(0, 0, width - 1, height - 1)
        for i in range(1, n_rows):
            y = i * cell_height
            painter.drawLine(0, y, width, y)
        for j in range(1, n_cols):
            x = j * cell_width
            painter.drawLine(x, 0, x, height)
        
        
        for kpc in keypList :
            self.paintLabel(''.join(kpc['keyp']) ,  kpc['cord'][0] ,  kpc['cord'][1] )

    def bye(self):
        print("QWidget subclass bye()")
        self.refreshTimer.stop()
        self.close()
        QApplication.quit()

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
    
    showingScreen = True

    resetKeyPrsd()
    
    imgScrn = take_screenshot(0, 0, screenW, screenH)
    
    imgOrig = convertQImageToMat(imgScrn)
    
    # imgOrig = np.asarray(imgScrn)
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

def take_screenshot(x, y, w, h):
    sc = None
    needCreate = False
    
    if wdapp:
        sc = wdapp
    else:
        needCreate = True
        sc = QApplication([])
        
    # QScreen.grabWindow( sc.primaryScreen(), QApplication.desktop().winId() ) .save(filename, 'png') 
    imgScrn = QScreen.grabWindow( sc.primaryScreen(), QApplication.desktop().winId() , x, y, screenW, screenH).toImage()

    if needCreate:
        sc.quit()
    
    return imgScrn
    
def convertQImageToMat(incomingImage):
    '''  Converts a QImage into an opencv MAT format  '''

    incomingImage = incomingImage.convertToFormat(4)

    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.bits()
    ptr.setsize(incomingImage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    return arr

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
    

    tmpapp = QGuiApplication([])
    screens = QGuiApplication.screens()

    total_geometry = QRect()
    for s in screens:
        total_geometry = total_geometry.united(s.geometry())

    print(total_geometry.x(), total_geometry.y(), total_geometry.width(), total_geometry.height())    
    
    w = total_geometry.width()
    h = total_geometry.height()
    screenW = w
    screenH = h

    tmpapp.quit()

if __name__ == '__main__':
    main()
    
