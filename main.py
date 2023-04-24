from Bot.Kalibrering import kalibrerings_verktøy
from Bot.spiller import Spiller

def main():
    kalibrerings_verktøy().kalibrer()
    Spiller().AI()

    """
    while not keyboard.is_pressed("å"):
        while keyboard.is_pressed("q"):
            pyautogui.click(kjeks_posisjon)
        time.sleep(1/60)"""



if __name__ == '__main__':
    main()
