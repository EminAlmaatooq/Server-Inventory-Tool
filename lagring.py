import os
import json
from pathlib import Path

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