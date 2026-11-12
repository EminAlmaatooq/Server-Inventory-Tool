import os
import json
from pathlib import Path
from datetime import datetime
import csv

def hamta_filnamn():
    # Returnerar filnamnet som ska användas för att lagra servrarna. fungerar inte den första så kommer den köras med den andra.
    return os.environ.get("INVENTORY_DATAFIL", "servrar.json")


def ladda_servrar():
    # Läser servrarna från filen och returnerar dem som en lista.
    fil = Path(hamta_filnamn())

    #Om filen inte finns startar vi med en tom lista
    if not fil.exists():
        return []

    # "r" = read. encoding="utf-8" är för att implementera bla nordiska bokstäver
    with open(fil, "r", encoding="utf-8") as f:
        return json.load(f)
        # json.load gör om JSON till en Python-lista


def spara_servrar(servrar):
    # Skriver listan med servrar till filen.
    # Parametern "servrar" är listan som ska sparas. Inget returneras.
    fil = Path(hamta_filnamn())

    # "w" = write
    with open(fil, "w", encoding="utf-8") as f:
        # indent=2 ger snygg läsbar JSON, ensure_ascii=False behåller å, ä, ö
        json.dump(servrar, f, ensure_ascii=False, indent=2)


def hitta_server(servrar, namn):
    # Går igenom listan och returnerar servern om namnet matchar 
    for server in servrar:
        if server["namn"] == namn:
            return server # return avslutar funktionen direkt

    # Hit kommer vi bara om loopen aldrig hittade något
    return None

def skapa_rapportsokvag():
    # Returnerar sökvägen till rapportfilen

    katalog = Path("rapporter")
    katalog.mkdir(exist_ok=True)  # skapar mappen, och om den redan finns blir det inget fel

    tiden = datetime.now().strftime("%Y-%m-%d_%H%M") #Hämtar nuvarande tid från datorn och formaterar den som text, t.ex. "2026-11-10_1430"
    filnamn = f"inventering_{tiden}.csv" #Bygger namnet på filen med tiden i namnet.

    return katalog / filnamn # sätter ihop mappen och filnamnet till en sökväg.

def exportera_csv(servrar):
    # Exporterar alla servrar till en CSV-fil

    # Hämtar sökvägen och skapar rapporter om den saknas
    sokvag = skapa_rapportsokvag()

    # newline="" undviker extra radbrytningar och encoding utf-8 gör att å, ä, ö fungerar
    with open(sokvag, "w", newline="", encoding="utf-8") as fil:

        # DictWriter skriver dictionaries som rader. fieldnames anger kolumnernaoch bestämmer i vilken ordning de står i filen.
        skrivare = csv.DictWriter(
            fil,
            fieldnames=["namn", "adress", "miljo", "roll", "status", "senast_kontrollerad"],
        )

        #skriver rubrikraden samt en rad för varje server i listan
        skrivare.writeheader()
        skrivare.writerows(servrar)

    
    return sokvag