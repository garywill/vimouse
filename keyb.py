from heads import *
import g
exec(open('impo.py').read())
 
 
def delay_do_click():
    time.sleep(g.autoClickDelay)
    do_click()
 
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
            
        if len(g.keypListFiltered) > 1:
            g.wdapp.pub_refresh.emit()
        
        if len(g.keypListFiltered) == 1  :
            print("hasMatch")
            
            matchKeyp = g.keypListFiltered[0]
            print(matchKeyp)
            
            
            
            x = g.curCellX + matchKeyp['cord'][0]
            y = g.curCellY + matchKeyp['cord'][1]
            mouse.position = (g.scrX+x, g.scrY+y)
            
            # screen_away()
            
            resetKeyPrsd()
            
            if g.autoClick :
                th = Thread(target=delay_do_click, args=() )
                th.start()

            screen_do('grid')
            
        
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
    # print(key)
    if not g.showingScreen and ( key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l ) and g.startKeysStatus == 0 :
        g.startKeysStatus = 1
    elif not g.showingScreen and g.startKeysStatus == 1 and key == keyboard.Key.cmd  :
        keyListenerStop()
        screen_do('grid')
        g.startKeysStatus = 0
        keyListenerStart(True)
        return
        
    if key == keyboard.Key.cmd and g.clickKeysStatus == 0  :
        g.clickKeysStatus = 1
    elif g.clickKeysStatus == 1 and ( key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l )  :
        g.clickKeysStatus = 2
        return
        
        
    if (key == keyboard.Key.esc or key == keyboard.KeyCode(char=',')) and g.showingScreen :
        keyListenerStop()
        screen_away()
        keyListenerStart(False)
        return
    
    if key == keyboard.Key.backspace and g.showingScreen == 'keys':
        # screen_away()
        resetKeyPrsd()
        screen_do('grid')
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
    if g.clickKeysStatus == 2 and ( key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l ) :
        do_click()
        g.clickKeysStatus = 0
        
    g.startKeysStatus = 0
    
    if key != keyboard.Key.cmd :
        g.clickKeysStatus = 0




