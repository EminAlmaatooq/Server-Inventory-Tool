# main.py
# Programmets startpunkt.

import argparse
from lagring import ladda_servrar
from meny import kor_meny, visa_servrar


def main():
    parser = argparse.ArgumentParser(description="Serverinventory tool")

    parser.add_argument("--lista", action="store_true", help="Visa alla servrar")

    args = parser.parse_args()

    if args.lista:
        # om man kör programmet med --lista så visas alla servrar direkt och menyn körs inte
        servrar = ladda_servrar()
        visa_servrar(servrar)
    else:
        # Användaren skrev inget så menyn körs
        kor_meny()


# Körs bara när filen startas direkt (python3 main.py)
if __name__ == "__main__":
    main()