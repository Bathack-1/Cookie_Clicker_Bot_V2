import time

import pyautogui
import json
import keyboard


#klasse som brukes for å finen statiske elementer som hoved kjeksen
class kalibrerings_verktøy:

    """
    finne hoved kjeksen
    finne buy all upgrades
    finne tekst vindu
    finne oppgraderinger

    en hoved funksjon: finne_element_via_bilde()
    """

    @staticmethod
    def finne_element_via_bilde(fil_navn, skjermbilde=pyautogui.screenshot(), sikkerhet=0.4, område="senter"):
        fil_bane = f"Bilder/{fil_navn}"
        element_posisjon = pyautogui.locate(fil_bane, skjermbilde, confidence=sikkerhet)

        #hvis du bare trenger posisjonen til et element
        if område == "senter":
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

    def kalibrer(self):
        start = time.time()
        json_tekst = {}
        skjermbilde = pyautogui.screenshot()

        json_tekst.update(self.finne_element_via_bilde("hoved_kjeks.png", skjermbilde))
        json_tekst.update(self.finne_element_via_bilde("nyheter.png", skjermbilde))
        json_tekst.update(self.finne_element_via_bilde("alle_oppgraderinger_knapp.png", skjermbilde, område="hele"))

        with open("statiske_posisjoner.json", "w") as json_fil:
            json.dump(json_tekst, json_fil, indent=4)

        slutt = time.time()
        print(f"brukte {slutt - start} sekunder")
