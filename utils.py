from PIL import ImageGrab
import cv2
import ctypes
import logging

logging.basicConfig(level=logging.INFO)

def take_picture():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Failed to open camera")
        return
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("picture.png", frame)
        logging.info("Picture taken and saved as picture.png")
    else:
        logging.error("Failed to capture image")
    cap.release()
    cv2.destroyAllWindows()

def take_screenshot():
    try:
        screenshot = ImageGrab.grab()
        screenshot.save("screenshot.png")
        logging.info("Screenshot taken and saved as screenshot.png")
    except Exception as e:
        logging.error(f"Failed to take screenshot: {e}")

def lock_screen():
    logging.info("Locking screen")
    ctypes.windll.user32.LockWorkStation()

def lock_input(mode=True):
    logging.info("Unlocking input")
    ctypes.windll.user32.BlockInput(mode)

def locker():
    lock_input()
    logging.info("Locker activated")
    take_picture()
    take_screenshot()
    lock_input(False)n
    lock_screen()