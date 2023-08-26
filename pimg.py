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
    
    len_of_letterList = len(g.letterList)
    len_of_regions = len(g.regions)
    
    print( len (g.regions) , 'regions')
    g.LC = 0
    for g.LC in range(1, 10) :
        if pow( len_of_letterList , g.LC) >= len_of_regions :
            break
    print('LC=', g.LC)
    g.keypList = []
    
    
    
    
    
    
    keyps = []
    for i in range(0, len_of_regions ) :
        keyp = []
        for j in range(0, g.LC) :
            n = int( i / pow( len_of_letterList, j) ) % pow( len_of_letterList, j+1) 
            letter = str ( g.letterList[n] ) 
            keyp.append(letter)
        keyps.append(''.join(keyp))
    for i in range(0, len_of_regions ) :
        keyp = keyps[i]
        
        similars = keyps
        for k in range(0, len(keyp) ):
            letter = keyp[k]
            similars = [x for x in similars if ( len(x) >= k and x[k] == letter ) ]
            if len(similars) <= 1:
                keyps[i] = keyp[0:k+1]
                break
            
    
    for i in range(0, len_of_regions ) :
        p = g.regions [i]
        xmax, ymax = np.amax(p, axis=0)
        xmin, ymin = np.amin(p, axis=0)
        pointX = (xmax+xmin)//2
        pointY = (ymax+ymin)//2

        g.keypList.append( {
            "keyp": keyps [ i ], 
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
        min_area = 20,
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
    


