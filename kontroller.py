import subprocess


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