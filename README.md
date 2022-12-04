# viScreenMouse

Use keyboard to click anywhere of screen. OpenCV based screenshot visual recognition. 

> The **vi** in the name here can mean "Vim", "Vimium", or "Vision" or whatever

Dependencies:
  - python3 , opencv , tkinter (tk/tcl) , pillow (with pillow,tk) , numpy , pynput

Theoretically works cross-platform. Tested on Linux X11 and Windows.

**This is early, usable, simple and experimental currently. Anything could need or be rewritten and changed, including the programming language used.**

## Usage

1. Hit `ctrl + meta` to find clickable objects on screen and show keys (meta key = win key = super key)
2. Press some keys to move mouse to that position
3. It triggers click (if `autoClick=True`. Otherwise hit `meta + ctrl` to trigger click)

> Open the file and configure for your need: whole screen, autoClick ...

There're some known issues. Apparently there're many we can do to improve it (open for discussion) :

- You're not seeing real-time screen change when the keys are shown,  it's actually showing a half-transparent screenshoted image borderless window
- Algorithm (filtering, recognizing,  parameters... ) . If you don't have a high contrast GUI, or some icons or buttons don't have clear contour, it may fail to recognize them.
- It's better to make it faster

