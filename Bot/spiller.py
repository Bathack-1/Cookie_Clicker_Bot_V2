import json
import time
import pyautogui
import keyboard
import concurrent.futures
import threading

"""
Spiller klasse:
    en bot som søker etter gullkjeks
    en bot som trykker på hoved kjeksen
    en bot som ser etter oppgraderinger
    en bot som ser om jeg kan kjøpe mer av noe
"""

class Spiller:

    def start(self):
        #fikse hoved kjeks info
        with open("statiske_posisjoner.json", "r") as json_fil:
            hoved_kjeks_info = json.load(json_fil)["hoved_kjeks"]
            self.hoved_kjeks_posisjon = (hoved_kjeks_info["x_posisjon"], hoved_kjeks_info["y_posisjon"])
            self.kjør = False

        #fikse gullkjeks info
        self.gull_kjeks_filbane = "Bilder/gull_kjeks.png"

        #fikse rødkjeks info
        self.rød_kjeks_filbane = "Bilder/rød_kjeks.png"

    def trykke_hoved_kjeks(self):
        while not keyboard.is_pressed("å"):
            if keyboard.is_pressed("q"):
                self.kjør = True
            if keyboard.is_pressed("w"):
                self.kjør = False
            if self.kjør:
                pyautogui.click(self.hoved_kjeks_posisjon)

    def finne_gull_kjeks(self):
        skjermbilde = self.skjermbilde
        kjeks_posisjoner = pyautogui.locateAll(self.gull_kjeks_filbane, skjermbilde, confidence=0.4)
        for posisjon in kjeks_posisjoner:
            if posisjon is not None:
                trykke_posisjon = pyautogui.center(posisjon)
                pyautogui.click(trykke_posisjon)

    def finne_rød_kjeks(self):
        skjermbilde = self.skjermbilde
        kjeks_posisjoner = pyautogui.locateAll(self.rød_kjeks_filbane, skjermbilde, confidence=0.4)
        for posisjon in kjeks_posisjoner:
            if posisjon is not None:
                trykke_posisjon = pyautogui.center(posisjon)
                pyautogui.click(trykke_posisjon)

    def AI(self):

        #Skaffe all informasjon for å kjøre programmet
        self.start()

        #Alle funksjonene som skal kjøre parrallelet
        funksjoner = [
            self.finne_gull_kjeks,
            self.finne_rød_kjeks
        ]

        #for å alltid trykke på hoved kjeksen
        trykke_hoved_kjeks_tråd = threading.Thread(target=self.trykke_hoved_kjeks, daemon=True)
        trykke_hoved_kjeks_tråd.start()

        while not keyboard.is_pressed("å"):
            self.skjermbilde = pyautogui.screenshot()

            # svart magi løsning (litt kjappere)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(funksjon) for funksjon in funksjoner]
                for future in concurrent.futures.as_completed(futures):
                    print(f"ferdig med {future}")

            time.sleep(1 / 60)
