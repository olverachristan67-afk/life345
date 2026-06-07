import ctypes
import time
import sys
import signal
import threading
import keyboard

user32 = ctypes.windll.user32

def create_invisible_cursor():
    and_mask = b'\xff' * 128
    xor_mask = b'\x00' * 128
    return user32.CreateCursor(0, 0, 0, 32, 32, and_mask, xor_mask)

def hide_cursor():
    hCursor = create_invisible_cursor()
    if not hCursor:
        sys.exit(1)
    
    cursor_ids = [
        32512, 32513, 32514, 32515, 32516,
        32640, 32641, 32642, 32643, 32644,
        32645, 32646, 32648, 32649, 32650, 32651
    ]
    
    for cursor_id in cursor_ids:
        user32.SetSystemCursor(hCursor, cursor_id)

def restore_cursor():
    user32.SystemParametersInfoW(0x0057, 0, None, 0)
    sys.exit(0)

def signal_handler(sig, frame):
    restore_cursor()

# Handle termination signals
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Secret hotkey to restore - Ctrl+Alt+F12
keyboard.add_hotkey('ctrl+alt+f12', restore_cursor)

hide_cursor()

# Run for 2 hours max then auto restore
timeout = 7200
elapsed = 0
while elapsed < timeout:
    time.sleep(1)
    elapsed += 1

restore_cursor()
