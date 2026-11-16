import os
import json
from pathlib import Path
from datetime import datetime
import csv


# Skapar funktionen hamta_filnamn som hämtar namnet på datafilen
# Där vi använder miljövariabeln om den finns, annars servrar.json
def hamta_filnamn():
    return os.environ.get("INVENTORY_DATAFIL", "servrar.json")


# Skapar funktionen ladda_servrar som läser in serverlistan
# Först så hämtar vi sökvägen till datafilen
# Sedan kollar vi om filen saknas och returnerar en tom lista om filen inte finns
# Efter det öppnar vi filen för läsning och använder UTF-8 för att hantera å, ä och ö
# Sist så läser JSON-innehållet och gör om det till Python-data
def ladda_servrar():
    fil = Path(hamta_filnamn())

    if not fil.exists():
        return []

    with open(fil, "r", encoding="utf-8") as f:
        return json.load(f)

# Skapar funktionen spara_servrar som sparar serverlistan
# Först så hämtar vi sökvägen till datafilen
# Sedan öppnar vi filen för skrivning och sparar listan som JSON
def spara_servrar(servrar):
    fil = Path(hamta_filnamn()) # hämtar sökvägen till datafilen

    # "w" = write
    with open(fil, "w", encoding="utf-8") as f:
        # indent=2 gör JSON lättare att läsa och ensure_ascii=False behåller å, ä, ö
        json.dump(servrar, f, ensure_ascii=False, indent=2)

# Skapar funktionen hitta_server som söker efter en server med det angivna namnet
# Först går vi igenom servarna en i taget
# Sedan jämför vi servernas namn med namnet vi söker efter
# Vi skickar tillbaka servern om namnet matchar, om servern inte hittades skickar vi tillbaka None.
def hitta_server(servrar, namn):

    for server in servrar:
        if server["namn"] == namn:
            return server

    return None


# Skapar funktionen skapa_rapportsokvag som skapar sökvägen till rapportfilen
# Först så väljer vi mappen där rapporterna ska sparas. katalog = Path("rapporter") anger vilken mapp som ska användas
# Sedan skapar vi mappen om den inte redan finns.
# Därefter hämtar vi nuvarande tid från datorn och formaterar den som text, t.ex. "2026-11-10_1430"
# Skapar ett filnamn med datum och tid
# När det är klart, Sätter vi ihop mappen och filnamnet till en sökväg
def skapa_rapportsokvag():
    
    katalog = Path("rapporter") 
    katalog.mkdir(exist_ok=True)
    tiden = datetime.now().strftime("%Y-%m-%d_%H%M") 
    filnamn = f"inventering_{tiden}.csv" #Bygger namnet på filen med tiden i namnet.

    return katalog / filnamn


# skapar funktionen exportera_csv() där den tar emot listan servrar som ska skrivas till en CSV-fil.
# Först så hämtar vi sölvägen där rapporten ska sparas
# Öppnar en ny fil för skrivning och använder UTF-8 och newline="" som undviker extra radbrytningar
# Senare skapar vi en skrivare och anger vilka kolumer rapporten ska ha
# Sist så skriver vi kolumnrubrikerna och skriver en rad för varje server där vi skickar tillbaka sökvägen till rapporten
def exportera_csv(servrar):
    sokvag = skapa_rapportsokvag()

    with open(sokvag, "w", newline="", encoding="utf-8") as fil:

        skrivare = csv.DictWriter(
            fil,
            fieldnames=["namn", "adress", "miljo", "roll", "status", "senast_kontrollerad"], # Här anger vi vilka
        )

        skrivare.writeheader()
        skrivare.writerows(servrar)

    return sokvag