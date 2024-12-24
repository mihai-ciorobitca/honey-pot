from pynput import mouse, keyboard
import threading
import sys
import ctypes
import logging
from utils import locker

class Listener:
    def __init__(self):
        self.timer = None
        self.locking = False
        self.mouse_listener = None
        self.keyboard_listener = None

    def lock_input(self):
        logging.info("Blocking input")
        value = ctypes.windll.user32.BlockInput(True)
        print(value) 

    def finish_timer(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        self.locking = True

    def start_timer(self):
        print("Timer started")
        self.lock_input()
        self.timer = threading.Timer(3.0, self.finish_timer)
        self.timer.start()

    def on_move(self, x, y):
        print(f"Mouse moved to ({x}, {y})")
        if x <= 0 and y <= 0:
            print("Timer cancelled")
            self.timer.cancel()
            self.mouse_listener.stop()
            sys.exit()
        elif not self.timer:
            self.start_timer()
            self.keyboard_listener.stop()

    def on_press(self, key):
        print(f"Key {key} pressed")
        self.start_timer()
        self.keyboard_listener.stop()

    def start_listener(self):
        with keyboard.Listener(on_press=self.on_press) as self.keyboard_listener, \
             mouse.Listener(on_move=self.on_move) as self.mouse_listener:
            self.keyboard_listener.join()
            self.mouse_listener.join()
    

if __name__ == "__main__":
    listener = Listener()
    listener.start_listener()
    if listener.locking:
        locker()
