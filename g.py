  

# for debug not cover whole screen
scrX = 200
scrY = 100
scrW = 1100
scrH = 500
# enable 'fetch_screen_size' in main() if you want it to cover whole screen


fontsize = 11

# whether to do a click after moving the mouse cursor to a position
autoClick = True
# the window need some time to disappear
autoClickDelay = 0.1 # unit: second

screenshotDelay = 100 # unit: ms 

# --------------------------






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

