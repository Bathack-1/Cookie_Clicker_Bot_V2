import time
import pyautogui
import json
import multiprocessing
import concurrent.futures
import keyboard


#klasse som brukes for å finen statiske elementer som hovedkjeksen og nyhetene
class kalibrerings_verktøy:

    """
    finne hoved kjeksen
    finne nyhets vindu
    finne buy all upgrades
    finne oppgraderinger

    en hoved funksjon: finne_element_via_bilde()
    """

    @staticmethod
    def finne_element_via_bilde(fil_navn, skjermbilde=pyautogui.screenshot(), område=None,  sikkerhet=0.4):
        fil_bane = f"Bilder/{fil_navn}"
        element_posisjon = pyautogui.locate(fil_bane, skjermbilde, confidence=sikkerhet)

        #hvis du bare trenger posisjonen til et element
        if område is None or område == "senter":
            element_posisjon = pyautogui.center(element_posisjon)
            element_informasjon = {
                "x_posisjon": int(element_posisjon[0]),
                "y_posisjon": int(element_posisjon[1])
            }

        #hvis du tregner posisjonen og størrelsen på et element
        else:
            element_informasjon = {
                "x_posisjon": int(element_posisjon[0]),
                "y_posisjon": int(element_posisjon[1]),
                "bredde": int(element_posisjon[2]),
                "høyde": int(element_posisjon[3])
            }
        element_navn = fil_navn.split(".")[0]
        """
        "filnavn.png" => ["filnavn", "png"] => "filnavn
        """
        #returnerer et dictonary med filnavnet som navn, og posisjonen som element
        return {element_navn: element_informasjon}

    #den fuksjonen her brukes hvis du bruker multiprossesing
    """
    @staticmethod
    def finne_element_parallelt(args):
        metode, bilde, skjermbilde, område = args
        return metode(bilde, skjermbilde, område)
    """

    def kalibrer(self):
        start = time.time()
        json_tekst = {}
        skjermbilde = pyautogui.screenshot()

        #alle bildene som skal brukes i kallebreringen
        bilder = [
            ("hoved_kjeks.png", "senter"),
            ("nyheter.png", "senter"),
            ("alle_oppgraderinger_knapp.png", "hele")
        ]

        #multiprocessing løsning
        """""
        with multiprocessing.Pool() as basseng:
            resultater = basseng.map(self.finne_element_parallelt,  [(self.finne_element_via_bilde, bilde, skjermbilde, område) for bilde, område in bilder])

        for resultat in resultater:
            json_tekst.update(resultat)"""""


        #svart magi løsning (litt kjappere)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.finne_element_via_bilde, bilde, skjermbilde, område) for bilde, område in bilder]
            for future in concurrent.futures.as_completed(futures):
                json_tekst.update(future.result())

        with open("statiske_posisjoner.json", "w") as json_fil:
            json.dump(json_tekst, json_fil, indent=4)

        slutt = time.time()
        print(f"brukte {slutt - start} sekunder")
