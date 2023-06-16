from heads import *
import g
exec(open('impo.py').read())
 
 
 
def do_click() :
    print("do_click()")
    mouse.click(Button.left, 1)

def keyListenerStart(suppress=False) :
    g.keyListener = keyboard.Listener( on_press=on_press, on_release=on_release, suppress = suppress)
    g.keyListener.start()
    if suppress:
        print('key listener: NOW BLOCKING KEY EVENTS BEING SENT TO OTHER APPS, until key badges dismiss')

def keyListenerStop() :
    g.keyListener.stop()
    print('key listener stop or reset...')

def resetKeyPrsd() :
    print("resetKeyPrsd()")
    g.prsdKeys = []
    g.keypListFiltered = g.keypList
    
def processKeyChar(char) :
    print("\n\nprocessKeyChar() char=%s" % char)
    char = char.upper()
    
    if g.showingScreen == 'keys': 
        g.prsdKeys.append(char)
        print(g.prsdKeys)
        
        N = len(g.prsdKeys)-1
        g.keypListFiltered = [x for x in g.keypListFiltered if x['keyp'][N] == char]
        # print("\n g.keypListFiltered:")
        # print(g.keypListFiltered)
        print( len(g.keypListFiltered) )
        
        if not len(g.keypListFiltered) > 0 :
            resetKeyPrsd()
        
        if len(g.keypListFiltered) == 1  :
            print("hasMatch")
            
            matchKeyp = g.keypListFiltered[0]
            print(matchKeyp)
            
            keyListenerStop()
            
            
            x = g.curCellX + matchKeyp['cord'][0]
            y = g.curCellY + matchKeyp['cord'][1]
            mouse.position = (g.scrX+x, g.scrY+y)
            
            screen_away()
            
            resetKeyPrsd()
            
            keyListenerStart(False)
            
            time.sleep(g.autoClickDelay)
            if g.autoClick :
                do_click()
            
        
        if len(g.prsdKeys) >= g.LC :
            print( "presKeys len >= max")
            resetKeyPrsd()
            return
        
    elif g.showingScreen == 'grid': 
        if char in g.cells.keys() :
            hideWindow()
            
            g.curCellX = g.cells[char] ['x']
            g.curCellY = g.cells[char] ['y']
            g.curCellW = g.cells[char] ['w']
            g.curCellH = g.cells[char] ['h']
            
            time.sleep(g.screenshotDelay/1000)
            screen_do('keys')



def on_press(key):
    if not g.showingScreen and ( key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l ) and g.startKeysStatus == 0 :
        g.startKeysStatus = 1
    elif not g.showingScreen and g.startKeysStatus == 1 and key == keyboard.Key.cmd  :
        keyListenerStop()
        screen_do('grid')
        g.startKeysStatus = 0
        keyListenerStart(True)
        return
        
    if key == keyboard.Key.cmd and g.clickKeysStatus == 0 and not g.showingScreen :
        g.clickKeysStatus = 1
    elif g.clickKeysStatus == 1 and ( key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l )  and not g.showingScreen:
        g.clickKeysStatus = 2
        return
        
        
    if key == keyboard.Key.esc and g.showingScreen :
        keyListenerStop()
        screen_away()
        keyListenerStart(False)
        return
    
    if g.showingScreen :
        char = 0
        try:
            char = key.char
        except:
            # print("key no char")
            pass
    
        if char :
            processKeyChar(char)
    

def on_release(key):
    if g.clickKeysStatus == 2 and ( key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l ) and not g.showingScreen :
        do_click()
        g.clickKeysStatus = 0
        
    g.startKeysStatus = 0
    
    if key != keyboard.Key.cmd :
        g.clickKeysStatus = 0




