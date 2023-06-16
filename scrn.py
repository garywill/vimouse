from heads import *
import g
exec(open('impo.py').read())



def destroyWindow () :
    print("destroyWindow()")
    
    hideWindow()
    
    g.wdapp.pub_quit.emit()
    g.wdapp = None

    
def hideWindow() :
    if g.wdapp:
        g.wdapp.pub_hide.emit()
    else:
        print('WARN: hideWindow() called but no g.wdapp')
        
    g.showingScreen = False
    g.keypList = []
    
    
def showWindow() :
    print('showWindow()')
    if g.wdapp:
        g.wdapp.pub_show.emit()
    else:
        print('create thread for QtApplication')
        qtthread = Thread(target=createWindow, args=(g.scrX, g.scrY, g.scrW, g.scrH) )
        qtthread.start()
    
    
def createWindow(x, y, w,h):        
    if g.wdapp:
        print('ERROR: createWindow() called but g.wdapp is not None')
        return
    
    g.wdapp = WdApp([x, y, w, h])
    
    g.wdapp.pub_show.connect(g.wdapp.show)
    g.wdapp.pub_hide.connect(g.wdapp.hide)
    g.wdapp.pub_quit.connect(g.wdapp.slot_quit)
    
    g.wdapp.pub_show.emit()
    
    g.wdapp.exec_()
    print('after app.exec_()')









def screen_away() :
    g.showingScreen = False
    hideWindow()
    resetKeyPrsd()
    resetRegions()

def screen_do(scrType) :
    g.showingScreen = scrType

    resetKeyPrsd()
    
    imgScrn = take_screenshot(g.scrX, g.scrY, g.scrW, g.scrH)
    
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

    imgMser, g.regions = mserImg(invImg(imgCls) , imgOrig)
    
    updateRegions(g.regions)
    showWindow()

def take_screenshot(x, y, w, h):
    sc = None
    needCreate = False
    
    if g.wdapp:
        sc = g.wdapp
    else:
        needCreate = True
        sc = QApplication([])
        
    # QScreen.grabWindow( sc.primaryScreen(), QApplication.desktop().winId() ) .save(filename, 'png') 
    imgScrn = QScreen.grabWindow( sc.primaryScreen(), QApplication.desktop().winId() , g.scrX, g.scrY, g.scrW, g.scrH).toImage()

    if needCreate:
        sc.quit()
    
    return imgScrn


def get_desktop_size() :
    tmpapp = QGuiApplication([])
    screens = QGuiApplication.screens()

    total_geometry = QRect()
    for s in screens:
        total_geometry = total_geometry.united(s.geometry())

    print(total_geometry.x(), total_geometry.y(), total_geometry.width(), total_geometry.height())    
    
    w = total_geometry.width()
    h = total_geometry.height()


    tmpapp.quit()
    
    return [0, 0, w, h]
    
    