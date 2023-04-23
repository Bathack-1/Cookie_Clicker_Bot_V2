import time
import keyboard
import pyautogui
import json
from Bot.Kalibrering import kalibrerings_verktøy

def main():
    kalibrerings_verktøy().kalibrer()
    """
    while not keyboard.is_pressed("å"):
        while keyboard.is_pressed("q"):
            pyautogui.click(kjeks_posisjon)
        time.sleep(1/60)"""



if __name__ == '__main__':
    main()
