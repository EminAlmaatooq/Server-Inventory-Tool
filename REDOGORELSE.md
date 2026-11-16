# Redogörelse

## 1. Tre konstruktioner i koden

**Villkor (if)**
**I meny.py, i funktionen lagg_till_server():**

**Det kontrollerar om servern redan finns. Om den gör det returneras False. Annars läggs den nya servern till.**

```python
if server_finns:
    return False

servrar.append(ny_server)
```

**if** Kontrollerar om server_finns är sant. Kolonet : visar att villkorets kod börjar, och indraget visar att return False hör till villkoret.

Om servern redan finns avbryts funktionen. Annars läggs den till i listan.

**Loop (while)**
**I meny.py, i funktionen fraga_miljo():**
**Loopen frågar efter en miljö tills man skriver ett giltigt värde.**

```python
while True:
    miljo = input("Ange miljö (dev, test, prod): ").strip().lower()

    if miljo in MILJO_STATUS:
        return miljo
```

**Funktion**
**lagring.py:**
**Funktionen söker efter en server med det angivna namnet. Den returnerar servern om den hittas, annars None.**

```python
def hitta_server(servrar, namn):
    for server in servrar:
        if server["namn"] == namn:
            return server
    return None
```

## 2. Lista med dictionaries

I meny.py, i funktionen lagg_till_server(), skapas en dictionary med information om en server:

```python
servrar = [
    {
        "namn": "web01",
        "adress": "192.168.1.10",
        "miljo": "prod",
        "roll": "webbserver",
        "status": "unknown",
        "senast_kontrollerad": ""
    }
]

Dictionaryn läggs till i listan med servrar.append(ny_server). 

Listan gör att programmet kan hålla reda på flera servrar. Varje dictionary samlar informationen om en server. Nycklarna är strängar och värdena är också strängar.
```

## 3. JSON och CSV

I lagring.py sparas serverlistan som JSON. Funktionen ladda_servrar() läser in listan från filen och spara_servrar() sparar ändringar. 

JSON gör att serverlistan finns kvar när programmet stängs och kan läsas in nästa gång det startas.

exportera_csv() sparar serverinformationen i en CSV-fil i mappen rapporter. CSV-filen visar informationen i rader och kolumner.

## 4. Moduler och funktioner

Programmet är uppdelat i flera filer med olika uppgifter. 

main.py startar programmet (funktionen main) och läser kommandoradsflaggorna.

meny.py sköter menyn och servrarna, t.ex. kor_meny, visa_servrar och lagg_till_server.

lagring.py läser och sparar data samt skapar rapporter, t.ex. ladda_servrar, spara_servrar och exportera_csv. 

kontroller.py testar servrarna och uppdaterar deras status, t.ex. svarar_pa_ping och kontrollera_alla.

Uppdelningen  av dessa gör det lättare att hitta, läsa och ändra koden.

## 5. Standardbiblioteket

- argparse läser kommandoradsflaggor.
- sys avslutar programmet med en exitkod.
- os hämtar namnet på datafilen från en miljövariabel.
- json läser och sparar serverlistan.
- pathlib hanterar sökvägar till filer och mappar.
- datetime hämtar och formaterar datum och tid.
- csv skapar rapporter.
- subprocess kör ping-kommandot för att kontrollera servrar.

## 6. God praxis
Jag har delat upp koden i funktioner, så varje funktion har en tydlig uppgift. Det gör koden lättare att läsa och ändra.

Jag kontrollerar att man väljer en giltig miljö. Det minskar risken för att felaktiga värden sparas.

Innan en server i prod tas bort frågar programmet om bekräftelse. Det minskar risken att servern tas bort av misstag.


## 7. Källor och hjälpmedel
Jag har använt Claude för att förstå begrepp, strukturera uppgiften och felsökning. Jag har också använt lärarens PowerPoint-presentationer och uppgifter samt YouTube-tutorials från Bro Code.