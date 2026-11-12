from meny import kor_meny
import argparse
from lagring import ladda_servrar, visa_servrar
from meny import kor_meny, visa_servrar

def main():
    parser = argparse.ArgumentParser(description="Serverinventory tool")
    
    parser.add_argument("--lista", action="store_true", help="Visa alla servrar")
    
    args = parser.parse_args()

    if args.lista:
        # Användaren skrev --lista, så vi visar alla servrar
        servrar = ladda_servrar()
        visa_servrar(servrar)
    else:
        # Ingen flagga, så vi startar menyn
        kor_meny()