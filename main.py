import argparse
from lagring import ladda_servrar
from meny import kor_meny, visa_servrar, filtrera_miljo


def main():
    parser = argparse.ArgumentParser(description="Serverinventory tool")

    parser.add_argument("--lista", action="store_true", help="Visa alla servrar")

    # --miljo tar ett värde och är valfritt. Om det inte anges är args.miljo None.
    parser.add_argument("--miljo", help="Visa bara servrar i en miljö (dev, test eller prod)")

    args = parser.parse_args()

    if args.lista:
        # om man kör programmet med --lista så visas servrarna direkt och menyn körs inte
        servrar = ladda_servrar()

        # args.miljo är None om användaren inte skrev --miljo. Då hoppar vi över filtreringen.
        if args.miljo:
            servrar = filtrera_miljo(servrar, args.miljo)

        visa_servrar(servrar)
    else:
        # Användaren skrev inget så menyn körs
        kor_meny()


# Körs bara när filen startas direkt (python3 main.py)
if __name__ == "__main__":
    main()