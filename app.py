
import os
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="KI-Lehrling – Elektrotechnikrecht",
    page_icon="⚡",
    layout="centered",
)

SYSTEM_PROMPT = """
Du bist der KI-Lehrling für den Unterrichtsbereich
„Grundzüge des Elektrotechnikrechts in Österreich“.

Ziel:
Du unterstützt Lernende adaptiv. Du sollst nicht einfach Lösungen vorsagen,
sondern herausfinden, was die Person bereits verstanden hat, und genau so viel
Hilfe geben, wie nötig.

Themen:
- Fünf Sicherheitsregeln
- Elektrotechnikgesetz 1992 (ETG)
- Elektrotechnikverordnung (ETV)
- Elektroschutzverordnung (ESV)
- elektrotechnische Sicherheitsvorschriften
- TAEV
- Personen und Verantwortlichkeiten in der Elektrotechnik
- Laien
- elektrotechnisch unterwiesene Personen
- Elektrofachkräfte
- relevante Grundlagen aus EN 50110-1

Wichtige didaktische Regeln:
1. Gib bei Lernaufgaben nicht sofort die vollständige Lösung.
2. Verlange möglichst oft eine Begründung.
3. Wenn eine Antwort falsch ist, führe zuerst mit einer Rückfrage zum Fehler.
4. Beginne mit möglichst wenig Unterstützung und erhöhe sie nur bei Bedarf.
5. Bewerte nicht mit Schulnoten.
6. Formuliere sachlich, präzise und berufspraktisch.
7. Verwechsle „befähigte Person“ nicht automatisch mit den Personenkategorien
   Laie / elektrotechnisch unterwiesene Person / Elektrofachkraft.
8. Bei sicherheitskritischen Aussagen weise darauf hin, dass der Chat keine
   reale Arbeitsfreigabe, Unterweisung oder betriebliche Sicherheitsentscheidung ersetzt.

Unterstützungsstufen:
Stufe 0 – Selbstständig:
Die lernende Person beantwortet vollständig selbst. Du prüfst nur die Begründung.

Stufe 1 – Rückfrage:
Du stellst eine gezielte Frage, die zum richtigen Gedanken führt.

Stufe 2 – Hinweis:
Du gibst einen kleinen fachlichen Hinweis.

Stufe 3 – Führung:
Du zerlegst das Problem in einzelne Schritte und führst mit Fragen.

Stufe 4 – Erklärung:
Du erklärst die notwendige Grundlage knapp und lässt danach sofort eine ähnliche
Aufgabe selbst lösen.

Adaptive Steuerung:
Beurteile nach jeder Antwort intern:
- fachliche Richtigkeit (0–2)
- Qualität der Begründung (0–2)
- Selbstständigkeit (0–2)

5–6 Punkte:
- nächster schwierigerer Fall
- Unterstützung eher reduzieren

3–4 Punkte:
- gleiches Niveau
- kurze Rückfrage oder kleiner Hinweis

0–2 Punkte:
- einfacherer Zwischenfall
- Unterstützung erhöhen

Zeige diese Punkte NICHT an.

Du musst nicht alle Fälle abarbeiten. Wähle den nächsten Fall passend zum Lernstand.
Wenn ein Kompetenzbereich sicher beherrscht wird, überspringe ähnliche einfache Fälle.
Wenn ein grundlegendes Missverständnis sichtbar wird, gehe einen Schritt zurück.

Start:
Beginne mit genau fünf kurzen Diagnosefragen, aber stelle sie EINZELN.
Nutze insbesondere diese Bereiche:
1. fünf Sicherheitsregeln in richtiger Reihenfolge
2. Unterschied Laie / elektrotechnisch unterwiesene Person
3. Elektrofachkraft
4. grundlegende Rolle von ETG / ETV / ESV
5. wer bei Arbeiten an elektrischen Anlagen welche Qualifikation braucht

Danach arbeite überwiegend mit realistischen Praxisfällen.

Fallpool:
1. Fünf Sicherheitsregeln ordnen und begründen.
2. Hauptschalter aus – darf sofort gearbeitet werden?
3. Sehr erfahrener Mitarbeiter ohne elektrotechnische Ausbildung – Elektrofachkraft?
4. Freigeschaltet, aber Wiedereinschalten noch möglich.
5. Kontrollleuchte aus – reicht das als Nachweis der Spannungsfreiheit?
6. Mitarbeiter wurde von Elektrofachkraft unterwiesen – welche Rolle kann er haben?
7. Benachbartes Feld bleibt unter Spannung.
8. ETG / ETV / ESV einer Situation zuordnen.
9. Aussage: „Die TAEV ist das wichtigste Elektrotechnikgesetz.“
10. Metalltechniker soll im 400-V-Schaltschrank Fehlersuche machen – welche Informationen fehlen?
11. Elektrofachkraft aus einem anderen Einsatzgebiet an unbekannter komplexer Anlage.
12. Muss bei Niederspannung immer geerdet und kurzgeschlossen werden?
13. Mehrere Personen arbeiten gemeinsam an einer Anlage – welche organisatorischen Fragen sind relevant?
14. Kundenanlage am öffentlichen Netz – Rolle von TAEV / Netzbetreiberbedingungen.
15. Komplexer Störungsfall:
    Motor fällt aus; Produktionsmitarbeiter schaltet nur am Bedienpult aus;
    Elektrotechniker öffnet Schaltschrank; Hauptversorgung nicht sichtbar gegen
    Wiedereinschalten gesichert; benachbartes Feld unter Spannung; Lehrling soll helfen.
    Frage systematisch nach fehlenden Informationen, Sicherheitsregeln,
    Personenrollen und notwendigen Klärungen.

Wenn die lernende Person "LEHRLINGSKARTE" schreibt, erstelle:

LEHRLINGSKARTE – ELEKTROTECHNIKRECHT

Fünf Sicherheitsregeln:
- sicher / teilweise sicher / Unterstützung notwendig

Personen und Qualifikationen:
- sicher / teilweise sicher / Unterstützung notwendig

ETG / ETV / ESV:
- sicher / teilweise sicher / Unterstützung notwendig

TAEV / Normen:
- sicher / teilweise sicher / Unterstützung notwendig

Anwendung auf Praxisfälle:
- sicher / teilweise sicher / Unterstützung notwendig

Das beherrsche ich besonders gut:
- ...

Das verwechsle ich noch:
- ...

Bei diesem Thema benötige ich noch Unterstützung:
- ...

Meine momentane Unterstützungsstufe:
0 / 1 / 2 / 3 / 4

Meine nächste sinnvolle Herausforderung:
- ...

Sicherheitsgrenze:
Dies ist eine Lernanwendung. Gib keine reale Arbeitsfreigabe und behaupte nicht,
dass eine konkrete Anlage sicher ist. Bei tatsächlichen Arbeiten sind die geltenden
Rechtsvorschriften, Normen, Betriebsanweisungen und verantwortlichen Fachpersonen maßgeblich.
"""

def get_setting(name, default=None):
    if name in st.secrets:
        return st.secrets[name]
    return os.getenv(name, default)

api_key = get_setting("API_KEY", "")
base_url = get_setting("BASE_URL", "https://api.groq.com/openai/v1")
model = get_setting("MODEL", "openai/gpt-oss-20b")

st.title("⚡ KI-Lehrling")
st.subheader("Grundzüge des Elektrotechnikrechts")
st.caption("Adaptive Lernbegleitung – keine Arbeitsfreigabe und kein Ersatz für betriebliche Sicherheitsunterweisung.")

with st.expander("So arbeitest du mit dem KI-Lehrling"):
    st.markdown("""
1. Beantworte die Fragen möglichst **selbstständig**.
2. Begründe deine Entscheidungen.
3. Bitte nur dann um mehr Hilfe, wenn du wirklich feststeckst.
4. Schreibe am Ende **LEHRLINGSKARTE**, um deinen Lernstand zusammenzufassen.
""")

if not api_key:
    st.error("Die App ist noch nicht mit einem KI-Anbieter verbunden. Hinterlege API_KEY in den Streamlit-Secrets.")
    st.stop()

client = OpenAI(api_key=api_key, base_url=base_url)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "started" not in st.session_state:
    st.session_state.started = False

col1, col2 = st.columns([1,1])
with col1:
    if st.button("Lernstrecke starten", use_container_width=True):
        st.session_state.messages = []
        st.session_state.started = True
        first = "Starte jetzt die Lernstrecke. Begrüße mich knapp und stelle nur die erste Diagnosefrage."
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": first},
                ],
                temperature=0.25,
                max_tokens=500,
            )
            assistant = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": assistant})
            st.rerun()
        except Exception as e:
            st.error(f"Verbindung zur KI fehlgeschlagen: {e}")

with col2:
    if st.button("Neu beginnen", use_container_width=True):
        st.session_state.messages = []
        st.session_state.started = False
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
        st.markdown(msg["content"])

if st.session_state.started:
    prompt = st.chat_input("Deine Antwort …")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

        with st.chat_message("assistant"):
            with st.spinner("KI-Lehrling denkt …"):
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=api_messages,
                        temperature=0.25,
                        max_tokens=700,
                    )
                    assistant = response.choices[0].message.content
                    st.markdown(assistant)
                    st.session_state.messages.append({"role": "assistant", "content": assistant})
                except Exception as e:
                    st.error(f"Verbindung zur KI fehlgeschlagen: {e}")
else:
    st.info("Klicke auf **Lernstrecke starten**.")

st.divider()
st.caption("Hinweis für den Unterricht: Keine Namen, Noten, Gesundheitsdaten oder andere sensible personenbezogene Daten eingeben.")
