from lagring import spara_servrar, hitta_server, ladda_servrar, exportera_csv
from kontroller import kontrollera_en, kontrollera_alla


MILJO_STATUS = ["dev", "test", "prod"] # Står utanför Funktionerna så att alla kan använda den. Stora bokstäver är att det är en konstant, då något som inte ska ändras.¨


# Går igenom varje server i listan servrar. Parametern "servrar" är listan som ska skrivas ut. Inget returneras.
def visa_servrar(servrar):

    if not servrar:
        print("Inga servrar att visa.")
        return

    print(f"{'Namn':<15} {'Adress':<15} {'Miljö':<6} {'Roll':<18} {'Status':<9}")

    for server in servrar: # går igenom varje server och skriver ut den
        print(f"{server['namn']:<15} {server['adress']:<15} {server['miljo']:<6} {server['roll']:<18} {server['status']:<9}") # skriver ut serverns namn, adress, miljö, roll och status där < och en siffra bestämmer bredden på kolumnen.


# En funktion som filtrerar servrar efter miljö (servrar, miljo) och skapar en tom lista som vi ska lägga till matchande servrar i [].
# Först så går igenom varje server i listan och Kollar om server tillhör den miljö som vi söker efter.
# Därefter jämför vi om serverns miljö är lika med den vi söker, sedan lägger vi till den i listan längst ner genom append().

def filtrera_miljo(servrar, miljo):
    matchande_servrar = []
    for server in servrar:  

        if server["miljo"] == miljo: 
            matchande_servrar.append(server) 

    return matchande_servrar 

# Skapar funktionen lagg_till_server(), som får serverlistan och den nya serverns namn, adress, miljö och roll.
# Först så sparar vi svaret i variabeln server_finns, som kollar om servern redan finns i listan genom att anropa hitta_server() med (servrar och namn).
# Om servern redan finns avbryter vi och returnerar False.
# Om servern inte finns, skapar vi en ny dictionary med serverdata och lägger till den i listan med append() och sparar listan med spara_servrar(). Returnerar True om servern lades till.
def lagg_till_server(servrar, namn, adress, miljo, roll):

    server_finns = hitta_server(servrar, namn) 

    if server_finns:
        return False

    ny_server = { # Dictionary med serverdata
        "namn": namn,
        "adress": adress,
        "miljo": miljo,
        "roll": roll,
        "status": "unknown",
        "senast_kontrollerad": "",
    }

    servrar.append(ny_server)
    spara_servrar(servrar)
    
    return True

# Skapar funktionen ta_bort_server() som tar bort servern med det angivna namnet från listan
# Det vi börjar med är att spara svaret i variabeln hitta och om servern inte finns avbryter vi
# Sedan  viTar bort servern från listan och sparar den uppdaterade listan i filen.
def ta_bort_server(servrar, namn):
    
    hitta = hitta_server(servrar, namn) 

    if hitta is None:
        return False

    servrar.remove(hitta)  
    spara_servrar(servrar)

    return True

# Skapar funktionen fraga_miljo som Frågar efter en giltig miljö
# Vi börjar med att skapa en while loop som är true, och anledningen är för att vi till att den fortsätter fråga tills miljön är giltig
# if satsen kollar om miljön är giltig, ifall den är det så returenrar den miljön och visar giltiga miljoer.
def fraga_miljo():
    
    while True:
        miljo = input("Ange miljö (dev, test, prod): ").strip().lower() # tar bort mellanslag och gör om till små bokstäver (strip och lower)

        if miljo in MILJO_STATUS:
            return miljo

        print(f"Felaktig miljö. Giltiga miljöer är: {', '.join(MILJO_STATUS)}")


# Skapar Funktion Fraga_lagg_till där vi frågar efter uppgifter och lägger till en server
# Vi gör en så kallad "inmatning" genom input() frågar vi först server namn, adress och roll.
# Nästa steg är att vi frågar efter en giltig miljö och därefter försöker lägga till servern
# Om server blev inlagd, så skriver vi ut success!, annars ett felmeddelande att servern redan finns.

def fraga_lagg_till(servrar):
    
    namn = input("Server namn: ")
    adress = input("Server adress: ")
    roll = input("Server roll: ")

    miljo = fraga_miljo() # är miljön giltig?

    hittade_servern = lagg_till_server(servrar, namn, adress, miljo, roll)


    if hittade_servern:
        print(f"Servern {namn} är nu tillagd.")
    else:
        print(f"Det finns redan en server med namnet {namn}.")


# Skapar funktionen fraga_ta_bort som frågar vilken server som ska tas bort
# Genom input vill vi läsa in servern namnet som ska tas bort där strip tar bort whitespace
# Sedan letar vi efter server i listan och om servern INTE finns så avbryter vi
# Om den finns i miljön, då i prod, ställer vi en kontroll/säkerthetsfråga där om man inte trycker ja så avbryter vi funktionen.
def fraga_ta_bort(servrar):
    namn_pa_server = input("Vilken server vill du ta bort? ").strip()

    server = hitta_server(servrar, namn_pa_server) # Vart är servern?

    if server is None: 
            print(f"Servern {namn_pa_server} finns inte. Avbryter.")
            return

    if server["miljo"] == "prod": # Finns server i prod?
        bekraftelse = input("Servern ligger i 'prod'. Är du säker på att du vill ta bort den? (ja/nej): ").strip().lower() #kontroll/säkerhetsfråga

        if bekraftelse != "ja":
            print("Avbryter borttagning.")

            return

    # Hit kommer vi bara om servern finns      
    # Finns den så försöker vi ta bort den och printar ut reslutat
    # Antigen att den lyckades eller ej.          
    ta_bort_resultat = ta_bort_server(servrar, namn_pa_server)
    if ta_bort_resultat:
        print(f"Servern {namn_pa_server} har tagits bort.")
    else:
        print(f"Det gick inte att ta bort servern {namn_pa_server}.")


# Skapar en funktion som skriver ut menyvalen
def visa_meny():

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


# Skapar en funktion där vi kör programmet meny
# Först vi läser vi in servarna från filen
# därefter gör vi en till while-loop där vi till visa menyn om igen tills vi avslutar
# Sedan genom input vill vi att man ska skriva ut vilken menyval.
def kor_meny():
    servrar = ladda_servrar()

    while True:

        visa_meny()
        
        val = input("Välj ett alternativ (1-8): ").strip()
        
       # Val 1: visar alla servrar
        if val == "1":
            visa_servrar(servrar)

       # Val 2: filtrerar och visar servrar i en vald miljö
        elif val == "2":
            miljo = fraga_miljo()
            filtrerade_servrar = filtrera_miljo(servrar, miljo)
            visa_servrar(filtrerade_servrar)

        # Val 3: frågar efter uppgifter och lägger till en server
        elif val == "3":
            fraga_lagg_till(servrar)

        # Val 4: frågar vilken server som ska tas bort
        elif val == "4":
            fraga_ta_bort(servrar)

        # Val 5: frågar efter en server och kontrollerar den med ping
        elif val == "5":
            namn = input("Ange servernamn att kontrollera: ").strip()

            server = kontrollera_en(servrar, namn)

            if server is None:
                print(f"Servern {namn} finns inte.")
            else:
                
                print(f"Servern {namn} har kontrollerats. Status: {server['status']}")

        # Val 6: kontrollerar alla servrar
        elif val == "6":
            antal_nere = kontrollera_alla(servrar)
            print(f"Alla servrar har kontrollerats. Antal servrar som är nere: {antal_nere}")

        # Val 7: skapar en CSV-rapport
        elif val == "7":
            sokvag = exportera_csv(servrar)
            print(f"Rapporten har exporterats till {sokvag}")

        # Val 8: avslutar programmet
        elif val == "8":
            print("Avslutar programmet.")
            return

        # Meddelar om man skriver ett annat val än 1–8
        else:
            print("Ogiltigt val, välj 1-8.")