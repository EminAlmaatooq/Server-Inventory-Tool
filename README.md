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

## Starta programmet

Kör alla kommandon i projektmappen.

### Textmeny

Starta utan argument:

```
python3 main.py
```

Då visas en meny med åtta val. Skriv siffran för valet och tryck Enter. Menyn visas igen
efter varje val, tills du väljer 8 för att avsluta.

| Val | Vad som händer |
|---|---|
| 1 | Visa alla servrar |
| 2 | Visa servrar i en viss miljö |
| 3 | Lägg till en server |
| 4 | Ta bort en server. Servrar i prod kräver en extra bekräftelse. |
| 5 | Kontrollera en server med ping |
| 6 | Kontrollera alla servrar med ping |
| 7 | Exportera en rapport som CSV |
| 8 | Avsluta |

### Kommandoraden

Programmet kan också styras med flaggor, utan någon meny:

| Kommando | Vad som händer |
|---|---|
| `python3 main.py` | Textmenyn startar. |
| `python3 main.py --lista` | Alla servrar skrivs ut och programmet avslutas. |
| `python3 main.py --lista --miljo prod` | Bara servrar i miljön prod skrivs ut. |
| `python3 main.py --kontrollera web01` | Servern web01 kontrolleras med ping. |
| `python3 main.py --kontrollera-alla` | Alla servrar kontrolleras med ping. |
| `python3 main.py --export` | En CSV-rapport skapas i katalogen rapporter. |
| `python3 main.py --help` | Visar en hjälptext med alla flaggor. |

`--miljo` fungerar tillsammans med `--lista`. Giltiga miljöer är dev, test och prod.
