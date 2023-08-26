  
########## user can edit #####

# the window need some time to disappear
screenshotDelay = 100 # unit: ms 

# for debug not cover whole screen
scrX = 0
scrY = 0
scrW = 1100
scrH = 500

# enable this if you want to. 
autoGetDesktopSize = False
# autoGetDesktopSize = True
# If it doesn't fetch your desktop size correctly, 
# disable it and manually fill your resolution into above


fontsize = 11

# whether to do a click after moving the mouse cursor to a position
autoClick = True
autoClickDelay = 0.1 # unit: second


# --------------------------
# it's NOT recommended user to edit below

n_rows = 5
n_cols = 6
# n_rows, n_cols = 4, 8


cells = {
    # 'A': {'x': 150, 'y': 200, 'w': 120, 'h': 120}, 
    # 'B': ...
}
curCellX=0
curCellY=0
curCellW=0
curCellH=0


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




letterList = list('ABCDEFGHJKLMNOPQRSTUVWXYZ234789')

