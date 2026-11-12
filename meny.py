from lagring import spara_servrar, hitta_server, ladda_servrar, exportera_csv
from kontroller import kontrollera_en, kontrollera_alla


MILJO_STATUS = ["dev", "test", "prod"] # Står utanför FunktionerNA så att alla kan använda den. Anledningen med stora bokstäver är att det är en konstant, dvs något som inte ska ändras.


def visa_servrar(servrar): 
    # Går igenom varje server i listan servrar.
    # Parametern "servrar" är listan som ska skrivas ut. Inget returneras.

    if not servrar:
        print("Inga servrar att visa.")
        return

    print(f"{'Namn':<15} {'Adress':<15} {'Miljö':<6} {'Roll':<18} {'Status':<9}")


    for server in servrar:
        print(f"{server['namn']:<15} {server['adress']:<15} {server['miljo']:<6} {server['roll']:<18} {server['status']:<9}") 
       # Varje kolumn får en fast bredd med :<bredd, så att kolumnerna ska hamna under varandra.



def filtrera_miljo(servrar, miljo):
    # Returnerar en ny lista med bara de servrar som finns i den valda miljön.
    # Tom lista där vi samlar de servrar som matchar

    matchande_servrar = []

    for server in servrar:  # Går igenom varje server i listan
        if server["miljo"] == miljo:
            matchande_servrar.append(server) # jämför om serverns miljö är lika med den vi söker sedan lägger vi till den i listan längst ner

    # Skickar tillbaka den nya listan.
    return matchande_servrar


def lagg_till_server(servrar, namn, adress, miljo, roll):
    # Lägger till en ny server i listan och sparar.

    server_finns = hitta_server(servrar, namn)  # Sparar svaret i variabeln

    # Om servern redan finns avbryter vi
    if server_finns:
        return False

    # Bygger en dictionary med serverdata. Nycklarna är de som vi använder i övriga funktioner.
    ny_server = {
        "namn": namn,
        "adress": adress,
        "miljo": miljo,
        "roll": roll,
        "status": "unknown",
        "senast_kontrollerad": "",
    }

    servrar.append(ny_server)  # Lägger till den nya servern i listan
    spara_servrar(servrar)  # Sparar listan med servrar till filen

    return True


def ta_bort_server(servrar, namn):
    # Tar bort servern med det namnet och sparar.
    # Returnerar True om den togs bort, False om den inte fanns.
    hitta = hitta_server(servrar, namn)  # Sparar svaret i variabeln

    if hitta is None:  # Om servern inte finns avbryter vi
        return False

    servrar.remove(hitta)  # Tar bort servern från listan
    spara_servrar(servrar)  # Sparar listan med servrar till filen

    return True


def fraga_miljo():
    # fråga efter en miljö tills användaren skriver det.
    
    while True:
        miljo = input("Ange miljö (dev, test, prod): ").strip().lower() # tar bort mellanslag och gör om till små bokstäver

        if miljo in MILJO_STATUS:
            return miljo

        print(f"Felaktig miljö. Giltiga miljöer är: {', '.join(MILJO_STATUS)}")


def fraga_lagg_till(servrar):
    
    namn = input("Server namn: ")
    adress = input("Server adress: ")
    roll = input("Server roll: ")

    miljo = fraga_miljo() # Frågar tills miljön är giltig

    hittade_servern = lagg_till_server(servrar, namn, adress, miljo, roll)


    if hittade_servern:
        print(f"Servern {namn} är nu tillagd.")
    else:
        print(f"Det finns redan en server med namnet {namn}.")

        
        
def fraga_ta_bort(servrar):
    # fråga vilken server som ska bort och anropa ta_bort_server().
    namn_pa_server = input("Vilken server vill du ta bort? ").strip()

    server = hitta_server(servrar, namn_pa_server)

    if server is None:
            print(f"Servern {namn_pa_server} finns inte. Avbryter.")
            return

    if server["miljo"] == "prod": # servrar i prod kräver en extra bekräftelse
        bekraftelse = input("Servern ligger i 'prod'. Är du säker på att du vill ta bort den? (ja/nej): ").strip().lower()
        if bekraftelse != "ja":
            print("Avbryter borttagning.")
            return

    # Hit kommer vi bara om servern finns och, för prod, är bekräftad                
    ta_bort_resultat = ta_bort_server(servrar, namn_pa_server)
    if ta_bort_resultat:
        print(f"Servern {namn_pa_server} har tagits bort.")
    else:
        print(f"Det gick inte att ta bort servern {namn_pa_server}.")


def visa_meny():
    # Skriver ut menyvalen

    print()
    print("=== Server Inventory Tool ===")
    print("1. Visa alla servrar")
    print("2. Visa servrar i en viss miljö")
    print("3. Lägg till server")
    print("4. Ta bort server")
    print("5. Kontrollera en server")
    print("6. Kontrollera alla servrar")
    print("7. Exportera rapport som CSV")
    print("8. Avsluta")
    print("=============================")


def kor_meny():# Huvudloopen: visar menyn, tar emot ett val och utför det tills användaren avslutar.

    # Läser in servrarna från filen innan loopen börjar
    servrar = ladda_servrar()

    # while True upprepar koden tills vi avslutar med return
    while True:

        # Skriver ut menyn varje varv
        visa_meny()
        
        val = input("Välj ett alternativ (1-8): ").strip()
        

        # Val 1: visa alla servrar i en tabell
        if val == "1":
            visa_servrar(servrar)

        # Val 2: fråga efter miljö, ta fram de servrar som ligger där och visa dem
        elif val == "2":
            miljo = fraga_miljo()
            filtrerade_servrar = filtrera_miljo(servrar, miljo)
            visa_servrar(filtrerade_servrar)

        # Val 3: fråga användaren efter uppgifterna och lägg till en ny server
        elif val == "3":
            fraga_lagg_till(servrar)

        # Val 4: fråga vilken server som ska bort och ta bort den
        elif val == "4":
            fraga_ta_bort(servrar)

        # Val 5: kontrollera en server med ping
        elif val == "5":
            namn = input("Ange servernamn att kontrollera: ").strip()

            # kontrollera_en ger tillbaka servern om den finns, annars None
            server = kontrollera_en(servrar, namn)

            if server is None:
                print(f"Servern {namn} finns inte.")
            else:
                # Visar om servern svarade (up) eller inte (down)
                print(f"Servern {namn} har kontrollerats. Status: {server['status']}")

        # Val 6: kontrollera alla servrar och räkna hur många som är nere
        elif val == "6":
            antal_nere = kontrollera_alla(servrar)
            print(f"Alla servrar har kontrollerats. Antal servrar som är nere: {antal_nere}")

        # Val 7: spara en CSV-rapport och skriv ut var den hamnade
        elif val == "7":
            sokvag = exportera_csv(servrar)
            print(f"Rapporten har exporterats till {sokvag}")

        # Val 8: avsluta. return stoppar funktionen och därmed loopen.
        elif val == "8":
            print("Avslutar programmet.")
            return

        # Allt annat är ett ogiltigt val, och då visas menyn igen
        else:
            print("Ogiltigt val, välj 1-8.")