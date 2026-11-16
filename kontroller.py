import subprocess
from datetime import datetime
from lagring import spara_servrar, hitta_server


# Skapar funktionen svarar_pa_ping som kontrollerar om en adress svarar
# Vi kör ping mot adressen
# Sparar ping-kommandots utkrift
# Till sist retunerar True om ping lyckades, annars False
def svarar_pa_ping(adress):
    resultat = subprocess.run(
        ["ping", "-c", "1", "-W", "2", adress],
        capture_output=True,
    )

    return resultat.returncode == 0

# Skapar funktionen hamta_tidsstampel som hämtar aktuell tid och datum från datorn
# Sist så gör vi om tiden till text i formatet år=Y månad=m dag=d timme=H:minut=M
def hamta_tidsstampel():
    nu = datetime.now()

    return nu.strftime("%Y-%m-%d %H:%M")


# Skapar funktionen uppdatera_server som tar emot en server och uppdaterar status och tid för senaste kontroll.
# Först så hämtar vi servern adress
# Vi kontrollerar om servern svara på ping 
# svara den så sparar statusen som up annars som down.
# Sist så hämtar vi aktuell tid genom hamta_tidsstampel,
# och sedan sparar den tiden i serverns så programmet kan visa när servern var senaste kontrollerad.
def uppdatera_server(server):
    adress = server["adress"]

    if svarar_pa_ping(adress):
        server["status"] = "up"
    else:
        server["status"] = "down"

    server["senast_kontrollerad"] = hamta_tidsstampel()


# Skapar funktionen kontrollera_alla som tar emot listan med servrar som ska kontrolleras.
# Vi börjar räkningen med 0
# Vi går igenom varje servern och kontrollerar servern och uppdaterar statusen på de
# Om servern inte svarar ökar vi antalet srvrar som är nere med ett
# sedan sparar vi de nya uppdaterade server uppgifterna och skickar tillbaka antal servern som är nere
def kontrollera_alla(servrar):
    antal_nere = 0
    
    for server in servrar:
        uppdatera_server(server)
       
        if server["status"] == "down":
            antal_nere += 1
    
    spara_servrar(servrar)
    return antal_nere


# skapar funktionen kontrollera_en som tar emot serverlistan och namnet på servern som ska kontrolleras.
# Först så söker vi efter servern i listan
# gör en if sats om servern inte hittas så avslutas funktionen och visar då att servern saknas
# sedan kontrollerar vi servern och uppdaterar statusen och sparar den uppdaterade serverlistan Listan sparas i JSON-filen som anges av INVENTORY_DATAFIL
# Till sist så skickar vi tillbaka servern med den nya statusen
def kontrollera_en(servrar, namn):
    server = hitta_server(servrar, namn) # Sökning
   
    if not server:
        return None
    
    uppdatera_server(server)
    
    spara_servrar(servrar)

    return server