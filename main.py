import argparse
import sys
from lagring import ladda_servrar, exportera_csv
from meny import kor_meny, visa_servrar, filtrera_miljo
from kontroller import kontrollera_en, kontrollera_alla

# skapar funktionen main(), som innehåller programmets huvuddel och styr vilket kommando som ska köras.
def main(): 

    parser = argparse.ArgumentParser(description="Serverinventory tool")  # Skapar parsern som läser vad användaren skriver efter python3 main.py

    parser.add_argument("--lista", action="store_true", help="Visa alla servrar") # ett argument som gör att man kan skriva --lista och då visas alla servrar.

    parser.add_argument("--miljo", help="Visa bara servrar i en miljö (dev, test eller prod)") # skapar ett argument där man kan skriva --miljo och då visas bara servrar i den miljön.

    parser.add_argument("--kontrollera", help="Kontrollera en server med ping, t.ex. web01") # skapar ett argument där man kan skriva --kontrollera och då kontrolleras den vilken server man vill kontrollera.

    parser.add_argument("--kontrollera-alla", action="store_true", help="Kontrollera alla servrar med ping") # skapar ett argument där man kan skriva --kontrollera-alla och då kontrolleras alla servrar.

    parser.add_argument("--export", action="store_true", help="Exportera alla servrar till en CSV-rapport")  # skapar ett argument där man kan skriva --export och då exporteras alla servrar till en CSV-rapport.


    args = parser.parse_args() # läser in argumenten som man skriver efter python3 main.py och sparar dem i args.


    # Om användaren skriver --lista, visas alla servrar och om man skriver --miljo, visas bara servrar i den miljön.
    if args.lista: 
        servrar = ladda_servrar() # Hämtas servrarna från filen

        if args.miljo:
            servrar = filtrera_miljo(servrar, args.miljo)

        visa_servrar(servrar)


    # Om användaren skriver --miljo utan --lista, visas bara servrar i den miljön
    elif args.miljo:
        servrar = ladda_servrar()

        filtrerade_servrar = filtrera_miljo(servrar, args.miljo) # Filtrerar servrarna i den miljön beroende på vad man skriver in

        visa_servrar(filtrerade_servrar)


    # Om användaren skriver --kontrollera med ett servernamn, kontrolleras den servern
    elif args.kontrollera:
        servrar = ladda_servrar()

        server = kontrollera_en(servrar, args.kontrollera) # Kontrollerar servern med ping

        # Om servern inte finns, skrivs ett felmeddelande ut och programmet avslutas med exitkod 1
        if server is None:
            print(f"Servern {args.kontrollera} finns inte.") 
            sys.exit(1) #exitkod 1

        print(f"{server['namn']}: {server['status']}")

        if server["status"] == "down": # Om servern är nere, avslutas programmet med exitkod 1
            sys.exit(1)

        
    # Om man skriver --kontrollera_alla, kontrolleras alla servrar och antalet som är nere skrivs ut. Om någon server är nere avslutas programmet med exitkod 1    
    elif args.kontrollera_alla:
        servrar = ladda_servrar()

        antal_nere = kontrollera_alla(servrar)

        visa_servrar(servrar)
        print(f"Antal servrar som är nere: {antal_nere}")

        if antal_nere > 0:
            sys.exit(1) 


    # Om man skriver --export, exporteras alla servrar till en CSV-rapport och sökvägen till filen skrivs ut.
    elif args.export:

        servrar = ladda_servrar()

        sokvag = exportera_csv(servrar)
        print(f"Rapporten har exporterats till {sokvag}")
    

    # Om användaren inte skriver något argument, körs menyn som vanligt.
    else:
        # Användaren skrev inget så menyn körs
        kor_meny()

# programmet startar här.
if __name__ == "__main__":
    main()