import argparse
import sys
from lagring import ladda_servrar
from meny import kor_meny, visa_servrar, filtrera_miljo
from kontroller import kontrollera_en


def main():

    # Skapar parsern som läser vad användaren skriver efter python3 main.py
    parser = argparse.ArgumentParser(description="Serverinventory tool")

    # --lista är av eller på: skriver man den visas servrarna
    parser.add_argument("--lista", action="store_true", help="Visa alla servrar")

    # --miljo tar ett värde och är valfritt
    parser.add_argument("--miljo", help="Visa bara servrar i en miljö (dev, test eller prod)")

    # --kontrollera tar ett värde (ett servernamn), samma som --miljo
    parser.add_argument("--kontrollera", help="Kontrollera en server med ping, t.ex. web01")

    args = parser.parse_args()

    if args.lista:
        # om man kör programmet med --lista så visas servrarna direkt och menyn körs inte
        servrar = ladda_servrar()

        # args.miljo är None om användaren inte skrev --miljo. Då hoppar vi över filtreringen.
        if args.miljo:
            servrar = filtrera_miljo(servrar, args.miljo)

        visa_servrar(servrar)

    elif args.miljo:
        # om man kör programmet med --miljo så visas servrarna i den miljön direkt och menyn körs inte
        servrar = ladda_servrar()
        filtrerade_servrar = filtrera_miljo(servrar, args.miljo)
        visa_servrar(filtrerade_servrar)

    elif args.kontrollera:
        # om man kör programmet med --kontrollera så kontrolleras den angivna servern
        servrar = ladda_servrar()

        # kontrollera_en pingar servern, sparar och ger tillbaka servern (eller None om den inte finns)
        server = kontrollera_en(servrar, args.kontrollera)

        if server is None:
            print(f"Servern {args.kontrollera} finns inte.")
            sys.exit(1)  # exitkod 1: servern finns inte

        print(f"{server['namn']}: {server['status']}")

        if server["status"] == "down":
            sys.exit(1)  # exitkod 1: servern är nere
        # Kommer vi hit utan sys.exit() blir exitkoden 0

    else:
        # Användaren skrev inget så menyn körs
        kor_meny()


# Körs bara när filen startas direkt (python3 main.py)
if __name__ == "__main__":
    main()