#!/usr/bin/env python3

# Licensed under GPL 3.0
# Copyright Garywill (github.com/garywill)   
#   copyright 2023 - 




from heads import *
import g
exec(open('impo.py').read())


def main():
    print('vimouse')
    print('  alpha preview version. User can edit g.py to customize')
    
    if not g.autoGetDesktopSize :
        print('autoGetDesktopSize not enabled. Running with only a part of user screen for debug purpose')
        
    print('')
    
    if g.autoGetDesktopSize :
        [g.scrX, g.scrY, g.scrW, g.scrH] = get_desktop_size()
    
    
    g.cells = genCells(g.scrX, g.scrY, g.scrW, g.scrH, g.n_rows, g.n_cols)
    
    print("starting key listener..")
    keyListenerStart(False)
    
    print("listening. Hit ctrl+win to start")
    
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
        



 
if __name__ == '__main__':
    main()
       