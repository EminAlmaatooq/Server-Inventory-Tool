import subprocess
from datetime import datetime
from lagring import spara_servrar

def svarar_pa_ping(adress):
    # Pingar adressen och returnerar True om den svarar, annars False.
    # -c 1 = ett paket, -W 2 = vänta högst 2 sekunder på svar.
    # capture_output=True fångar ping-texten så att den inte skrivs ut.
    resultat = subprocess.run(
        ["ping", "-c", "1", "-W", "2", adress],
        capture_output=True,
    )

    # Exitkod 0 betyder att servern svarade
    return resultat.returncode == 0


def hamta_tidsstampel():
    # Returnerar aktuell tid som text, t.ex. "2026-11-10 14:30"
    nu = datetime.now()
    return nu.strftime("%Y-%m-%d %H:%M")


def uppdatera_server(server):
    # Pingar en server och uppdaterar status och senast_kontrollerad.
    # Ändrar dictionaryn direkt, så ingen return behövs. Sparar inte till filen.
    adress = server["adress"]

    if svarar_pa_ping(adress):
        server["status"] = "up"
    else:
        server["status"] = "down"

    # Utanför if/else, så att tidsstämpeln sätts varje gång servern kontrolleras (G10)
    server["senast_kontrollerad"] = hamta_tidsstampel()


def kontrollera_alla(servrar):
    # Kontrollerar alla servrar, sparar en gång och returnerar antalet som är nere.

    antal_nere = 0
    
    for server in servrar:
        uppdatera_server(server)
       
        if server["status"] == "down":
            antal_nere += 1
    
    spara_servrar(servrar)
    return antal_nere