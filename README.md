# ViScreen

Use keyboard to click anywhere on screen. OpenCV based. 

- Dependencies:
  - python3
  - opencv
  - tkinter
  - pillow (with pillow-tk)
  - numpy
  - pynput


Status: Early. Usable. Developed on Linux X11. Theoretically runs cross-platform.

**Usage**:

1. `ctrl + meta` to find and show keys (meta key = win key = super key)
2. Press some keys to move mouse to a position
3. `meta + ctrl` to click

There're some known issues. Apparently there're many we can do to improve it (share your idea, open for discussion) :

- Mouse wheel sometimes goes strange
- You're not seeing real-time screen change when the keys are shown,  it's actually showing a half-transparent screenshoted image fullscreen window
- Due to above one, defautly it moves mouse cursor to a position and  you to decide whether to do click (by keyboard) 
- It needs to be faster. The GUI library may be replaced in the future
