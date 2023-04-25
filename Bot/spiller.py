import json
import time
import pyautogui
import keyboard
import concurrent.futures
import threading
from Bot.Kalibrering import KalibreringsVerktøy

"""
Spiller klasse:
    en bot som søker etter gullkjeks
    en bot som trykker på hoved kjeksen
    en bot som ser etter oppgraderinger
    en bot som ser om jeg kan kjøpe mer av noe
"""

class Spiller:

    def __init__(self, skal_kalibrere=True):
        if skal_kalibrere:
            kalibrering = KalibreringsVerktøy()
            kalibrering.kalibrer()
        self.lås = threading.Lock()

        #Lagre informasjonen som er i Json filen
        with open("statiske_posisjoner.json", "r") as json_fil:
            fil_innhold = json.load(json_fil)
            #all info for å trykke hoved kjeksen
            hoved_kjeks_info = fil_innhold["hoved_kjeks"]
            self.hoved_kjeks_posisjon = (hoved_kjeks_info["x_posisjon"], hoved_kjeks_info["y_posisjon"])
            self.kjør = False

            #all info for å kjøpe oppgraderinger
            oppgraderings_rute = fil_innhold["oppgradere"]
            self.oppgraderings_rute_posisjon = (oppgraderings_rute["x_posisjon"], oppgraderings_rute["y_posisjon"])
            self.oppgraderings_rute_farge = oppgraderings_rute["farge"]

            kjøp_alle_knapp = oppgraderings_rute["kjøp_alle_knapp"]
            self.kjøp_alle_knapp_posisjon = pyautogui.center((kjøp_alle_knapp["x_posisjon"], kjøp_alle_knapp["y_posisjon"], kjøp_alle_knapp["bredde"], kjøp_alle_knapp["høyde"]))

        #fikse gullkjeks info
        self.gull_kjeks_filbane = "Bilder/gull_kjeks.png"

        #fikse rødkjeks info
        self.rød_kjeks_filbane = "Bilder/rød_kjeks.png"

    def trykke_hoved_kjeks(self):   #funksjon som hele tiden kjører
        while not keyboard.is_pressed("å"):
            if keyboard.is_pressed("q"):
                self.kjør = True
            if keyboard.is_pressed("w"):
                self.kjør = False
            if self.kjør:
                with self.lås:
                    pyautogui.click(self.hoved_kjeks_posisjon)

    def kjøpe_oppgraderinger(self):
        skjermbilde = self.skjermbilde
        if skjermbilde.getpixel(self.oppgraderings_rute_posisjon)[2] >= self.oppgraderings_rute_farge:
            with self.lås:
                pyautogui.click(self.kjøp_alle_knapp_posisjon)
        else:
            print(f"på påsisjon {self.oppgraderings_rute_posisjon} finner vi fargen {skjermbilde.getpixel(self.oppgraderings_rute_posisjon)[2]}")

    def finne_gull_kjeks(self):
        skjermbilde = self.skjermbilde
        kjeks_posisjoner = pyautogui.locateAll(self.gull_kjeks_filbane, skjermbilde, confidence=0.4)
        for posisjon in kjeks_posisjoner:
            if posisjon is not None:
                with self.lås:
                    trykke_posisjon = pyautogui.center(posisjon)
                    pyautogui.click(trykke_posisjon)

    def finne_rød_kjeks(self):
        skjermbilde = self.skjermbilde
        kjeks_posisjoner = pyautogui.locateAll(self.rød_kjeks_filbane, skjermbilde, confidence=0.4)
        for posisjon in kjeks_posisjoner:
            if posisjon is not None:
                with self.lås:
                    trykke_posisjon = pyautogui.center(posisjon)
                    pyautogui.click(trykke_posisjon)

    def AI(self):
        #Alle funksjonene som skal kjøre parrallelet
        funksjoner = [
            self.finne_gull_kjeks,
            self.finne_rød_kjeks,
            self.kjøpe_oppgraderinger
        ]

        #for å alltid trykke på hoved kjeksen
        trykke_hoved_kjeks_tråd = threading.Thread(target=self.trykke_hoved_kjeks, daemon=True)
        trykke_hoved_kjeks_tråd.start()

        while not keyboard.is_pressed("å"):
            #et felles skjermbilde, for å spare litt pc-ressurser
            self.skjermbilde = pyautogui.screenshot()

            # kjøre koden asynkront. svart magi løsning
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(funksjon) for funksjon in funksjoner]
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()  # Legg til denne linjen
                    except Exception as e:
                        print(f"Feil i {future}: {e}")  # Legg til denne linjen
                    else:
                        print(f"ferdig med {future}")

            time.sleep(1 / 60)
