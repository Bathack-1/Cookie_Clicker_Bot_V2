import time
import pyautogui
import json
import multiprocessing
import concurrent.futures
import keyboard


#klasse som brukes for å finen statiske elementer som hovedkjeksen og nyhetene
class KalibreringsVerktøy:

    """
    finne hoved kjeksen
    finne nyhets vindu
    finne buy all upgrades
    finne oppgraderinger

    en hoved funksjon: finne_element_via_bilde()
    """


    def finne_senter_til_element_via_bilde(self, fil_navn, skjermbilde=pyautogui.screenshot(), sikkerhet=0.4):
        fil_bane = f"Bilder/{fil_navn}"
        element_posisjon = pyautogui.locate(fil_bane, skjermbilde, confidence=sikkerhet)

        element_posisjon = pyautogui.center(element_posisjon)
        element_informasjon = {
            "x_posisjon": int(element_posisjon[0]),
            "y_posisjon": int(element_posisjon[1])
        }

        element_navn = fil_navn.split(".")[0]
        """
        "filnavn.png" => ["filnavn", "png"] => "filnavn
        """
        #returnerer et dictonary med filnavnet som navn, og posisjonen som element
        return {element_navn: element_informasjon}


    def finne_kjøp_alle_posisjon(self, fil_navn, skjermbilde=pyautogui.screenshot(), sikkerhet=0.4):
        fil_bane = f"Bilder/{fil_navn}"
        element_posisjon = pyautogui.locate(fil_bane, skjermbilde, confidence=sikkerhet)

        #litt lettere å bruke denne infoen når det er i en liste
        element_informasjon = {
            "x_posisjon": int(element_posisjon[0]),
            "y_posisjon": int(element_posisjon[1]),
            "bredde": int(element_posisjon[2]),
            "høyde": int(element_posisjon[3])
        }

        #en liste for å lagre alle fargene til en rute med oppgradering
        alle_farger = []

        #Gå over alle rutene for å finne fargen dems
        for x in range(1, 6):
            oppgraderings_rute = (
                element_informasjon["x_posisjon"] + (x * int(element_informasjon["bredde"] / 10)),
                element_informasjon["y_posisjon"] + int(1.5 * element_informasjon["høyde"]) + int(element_informasjon["høyde"] / 10)

            )
            alle_farger.append(skjermbilde.getpixel(oppgraderings_rute)[2])

        alle_farger.sort() #sorterer så største verdi kommer på toppen

        #litt klønete måte å gjøre det på, men da får fila et hirarki
        oppgradering_informasjon = {
            "x_posisjon": element_informasjon["x_posisjon"] + int(element_informasjon["bredde"]/10),
            "y_posisjon": element_informasjon["y_posisjon"] + int(1.5 * element_informasjon["høyde"]),
            "farge": alle_farger[0], #legger til den høyeste fargen til lista
            "kjøp_alle_knapp": element_informasjon
        }
        return {"oppgradere": oppgradering_informasjon}


    def kalibrer(self):
        start = time.time()
        json_tekst = {}
        skjermbilde = pyautogui.screenshot()

        #alle funksjonene og bildene som skal brukes i kallebreringen
        funksjoner_og_bilder = [
            #funksjon                                   #bilde navn
            (self.finne_senter_til_element_via_bilde, "hoved_kjeks.png"),
            (self.finne_senter_til_element_via_bilde, "nyheter.png"),
            (self.finne_kjøp_alle_posisjon, "alle_oppgraderinger_knapp.png")
        ]

        #svart magi løsning (litt kjappere)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(funksjon, bilde, skjermbilde) for funksjon, bilde in funksjoner_og_bilder]
            for future in concurrent.futures.as_completed(futures):
                json_tekst.update(future.result())

        #siste som alltid skal gjøres, skrive posisjonene til json filen
        with open("statiske_posisjoner.json", "w") as json_fil:
            json.dump(json_tekst, json_fil, indent=4)

        slutt = time.time()
        print(f"brukte {slutt - start} sekunder")
