
# KI-Lehrling – Elektrotechnikrecht

Ein minimaler Unterrichtsprototyp für eine adaptive KI-Lernbegleitung.

## Was die App macht

- gemeinsamer KI-Lehrling für alle Schüler
- getrennte Chat-Sitzung pro Browser-Session
- fünf Diagnosefragen
- adaptive Hilfestufen 0–4
- 15 mögliche Praxisfälle
- Lehrlingskarte am Ende
- keine Schülerkonten notwendig, wenn die App öffentlich bereitgestellt wird

## Empfohlene schnelle Bereitstellung

### Variante A: Streamlit Community Cloud

Streamlit Community Cloud kann Apps kostenlos öffentlich bereitstellen.
Du brauchst selbst ein GitHub-Konto; die Schüler benötigen danach nur den App-Link.

1. Neues GitHub-Repository erstellen.
2. `app.py` und `requirements.txt` hochladen.
3. In Streamlit Community Cloud eine neue App aus diesem Repository erstellen.
4. Unter **App Settings → Secrets** folgende Werte hinterlegen:

```toml
API_KEY = "DEIN_API_KEY"
BASE_URL = "https://api.groq.com/openai/v1"
MODEL = "openai/gpt-oss-20b"
```

5. App-Link in Eduvidual einfügen.

Wichtig: API-Schlüssel niemals in `app.py` oder in ein öffentliches GitHub-Repository schreiben.

## KI-Anbieter

Die App benutzt eine OpenAI-kompatible Chat-Completions-Schnittstelle.
Standardmäßig ist sie für GroqCloud vorbereitet.

Damit kannst du später auch einen anderen kompatiblen Anbieter einsetzen, indem du
`BASE_URL`, `API_KEY` und `MODEL` in den Secrets änderst.

## Datenschutz

Für den Prototyp:
- keine Namen eingeben lassen
- keine Noten
- keine Gesundheitsdaten
- keine Förderdiagnosen
- keine sonstigen sensiblen personenbezogenen Daten

Die Chats werden in dieser App nur in der aktuellen Streamlit-Sitzung gehalten.
Welche Daten der KI-Anbieter verarbeitet, richtet sich zusätzlich nach dessen Bedingungen.

## Unterrichtsstart

Schüler öffnen nur den Link und klicken auf:

**Lernstrecke starten**

Am Ende schreiben sie:

**LEHRLINGSKARTE**
