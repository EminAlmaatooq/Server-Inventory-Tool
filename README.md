# Server Inventory Tool

Ett Python-program som håller reda på servrar: vad de heter, vilken adress de har,
vilken miljö de körs i (dev, test eller prod) och vilken roll de har. Programmet kan
också kontrollera om servrarna svarar på ping och exportera en rapport som CSV.

Programmet kan användas på två sätt: via en textmeny, eller direkt från kommandoraden.

## Vad programmet kan göra

- Visa alla servrar, eller bara servrar i en viss miljö
- Lägga till och ta bort servrar
- Kontrollera om en eller alla servrar svarar på ping
- Spara servrarna i en JSON-fil, så att de finns kvar mellan körningarna
- Exportera alla servrar till en CSV-fil

## Vad som krävs

- Python 3
- Linux eller macOS, eftersom programmet använder `ping -c`. På Windows kan du köra det i WSL.
- Inga extra bibliotek behöver installeras, bara Pythons standardbibliotek
