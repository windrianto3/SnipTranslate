import os
import pyautogui
import win32gui
import win32ui
from ctypes import windll
from PIL import Image

class ScreenCapHelper():
    def __init__(self):
        pass
        
    def list_window_names(self):
        toplist, winlist = [], []
        def enum_cb(hwnd, results):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
                winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, toplist)
        return winlist

    def saveDesktopScreenScreenshot(self):
        screenshot = pyautogui.screenshot()
        #os.chdir("..")
        #fpath=os.path.join("./screenshots/desktop.png")
        #screenshot.save(fp=fpath)
        return screenshot

    def saveWindow(self, windowstr, save_path):
        winlist = self.list_window_names()
        window = [(hwnd, title) for hwnd, title in winlist if windowstr in title.lower()]
        print(window)
        # just grab the hwnd for first window match
        hwnd = window[0]
        hwnd = hwnd[0]

        windll.user32.SetProcessDPIAware()

        # Change the line below depending on whether you want the whole window
        # or just the client area. 
        #left, top, right, bot = win32gui.GetClientRect(hwnd)
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        # Change the line below depending on whether you want the whole window
        # or just the client area. 
        #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)
        #print(result)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

        #if result == 1:
            #PrintWindow Succeeded
            #im.save(save_path)
            #im.show()

        return im

    # todo: func for capturing specific rectangle from desktop
