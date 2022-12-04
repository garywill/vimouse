# ViScreen

Use keyboard to click anywhere on screen. OpenCV based. 

> The name **Vi** here can mean "Vim", "Vimium", or "Vision" or whatever

- Dependencies:
  - python3
  - opencv
  - tkinter (tk/tcl)
  - pillow (with pillow-tk)
  - numpy
  - pynput

Theoretically works cross-platform. Tested on Linux X11 and Windows.

**This is early, usable and experimental. Anything could need or be rewritten and changed, including the programming language used.**

## Usage

1. Hit `ctrl + meta` to find clickable objects on screen and show keys (meta key = win key = super key)
2. Press some keys to move mouse to that position
3. Defaultly `autoClick=False` , so hit `meta + ctrl` to trigger a click

> Open the file and configure for your need: whole screen, autoClick ...

There're some known issues. Apparently there're many we can do to improve it (open for discussion) :

- You're not seeing real-time screen change when the keys are shown,  it's actually showing a half-transparent screenshoted image fullscreen window
- Due to above one, defautly it moves mouse cursor to a position and  you to decide whether to click (by keyboard) (you can change that by setting `autoClick=True`)
- It needs to be faster
- Algorithm (filtering, recognizing,  parameters... ) . If you don't have a high contrast GUI, or some icons or buttons don't have clear contour, it may fail to recognize them.

