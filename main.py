#!/usr/bin/env python3

# Licensed under GPL 3.0
# Copyright Garywill (github.com/garywill)   
#   copyright 2023 - 




from heads import *
import g
exec(open('impo.py').read())


def main():
    # uncomment this to do for whole screen
    # fetch_screen_size()
    
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
       