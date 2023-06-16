from heads import *
import g
exec(open('impo.py').read())
 
    
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
    g.regions = newRegions
    print( len (g.regions) )
    g.LC = 0
    for g.LC in range(1, 10) :
        if pow( len(g.letterList) , g.LC) >= len(g.regions) :
            break
    print(g.LC)
    g.keypList = []
    for i in range(0, len(g.regions) ) :
        p = g.regions [i]
        xmax, ymax = np.amax(p, axis=0)
        xmin, ymin = np.amin(p, axis=0)
        pointX = (xmax+xmin)//2
        pointY = (ymax+ymin)//2
        keyp = []
        for j in range(0, g.LC) :
            l = str ( g.letterList[ int( i / pow( len(g.letterList), j) ) % pow( len(g.letterList), j+1) ] ) 
            keyp.insert (0, l)
        g.keypList.append( {
            "keyp": keyp, 
            "cord": [pointX, pointY]
            } )
        # print("i=%d, keyp=%s" % (i, ''.join(keyp) ) )
    g.keypListFiltered = g.keypList
    
    
def resetRegions() :
    g.LC = 0
    g.regions = []
    g.keypList = []
    g.keypListFiltered = g.keypList
  

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
    g.regions, _ = mser.detectRegions(imgInput)
    
    imgOutput = bgImg
    
    for p in g.regions:
        xmax, ymax = np.amax(p, axis=0)
        xmin, ymin = np.amin(p, axis=0)
        cv2.rectangle(imgOutput, (xmin,ymax), (xmax,ymin), (0, 0, 180), 1)
    
    return imgOutput, g.regions
    


