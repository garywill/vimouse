#!/usr/bin/env python3

# Licensed under GPL 3.0
# Copyright Garywill (github.com/garywill)   
#   copyright 2023 - 




from heads import *
import g
exec(open('impo.py').read())


def main():
    if g.autoGetDesktopSize :
        [g.scrX, g.scrY, g.scrW, g.scrH] = get_desktop_size()
    
    
    g.cells = genCells(g.scrX, g.scrY, g.scrW, g.scrH, g.n_rows, g.n_cols)
    
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
        



 
if __name__ == '__main__':
    main()
       