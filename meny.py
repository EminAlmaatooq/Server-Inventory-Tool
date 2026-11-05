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
    # Parametrarna: "servrar" är hela listan, "miljo" är t.ex. "prod".

    # Tom lista där vi samlar de servrar som matchar
    matchande_servrar = []

   
    for server in servrar:  # Går igenom varje server i listan
        
        if server["miljo"] == miljo:
            matchande_servrar.append(server) # jämför om serverns miljö är lika med den vi söker sedan lägger vi till den i listan matchande_servrar längst ner

    # Skickar tillbaka den nya listan till den som anropade funktionen
    return matchande_servrar


def hitta_server(servrar, namn):
    # Går igenom listan och returnerar servern om namnet matchar
    for server in servrar:
        if server["namn"] == namn:
            return server # return avslutar funktionen direkt

    # Hit kommer vi bara om loopen aldrig hittade något
    return None