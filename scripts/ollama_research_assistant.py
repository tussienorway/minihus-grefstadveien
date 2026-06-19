import json
import urllib.request
import os
import subprocess
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"
OUTPUT_PATH = "/home/tussie/minihus-grefstadveien/ollama_rapport.html"

# Define the architectural design to compare
DESIGN_SPECS = """
Eiendomsadresse: Grefstadveien 81, Grimstad
Totalt bruksareal (BRA): 78 m² på 1 plan.
Planløsning:
- Stue: 38 m² (Åpen mot kjøkken, store vinduer sør/vest)
- Kjøkken: 12 m² (L-formet, integrerte hvitevarer)
- Soverom: 12 m² (Plass til dobbeltseng og skyvedørsgarderobe)
- Bad: 8 m² (Flislagt, dusjhjørne, opplegg for vaskemaskin/tørketrommel, varmekabler)
- WC: 3 m² (Separat toalett med vask, nær stuen)
- Bod: 5 m² (Teknisk bod med sikringsskap, varmtvannsbereder og integrert dockingstasjon for robotstøvsuger)

Særegne hensyn:
- Robotstøvsugervennlig: Dørterskler under 15 mm, brede passasjer over 40 cm.
- Ikke rullestoltilgjengelig (bruker har lave krav til rullestol, ønsker maksimal plassutnyttelse for robotstøvsugere).
- Sikring mot kreditorer (SI) via 100-års tomtefeste med privat beslagsforbud etter dekningsloven § 3-1.
"""

PROMPT = f"""
Du er en høyt kvalifisert norsk sivilarkitekt (MNAL) og forskningsassistent for et automatisert tegnekontor.
Gjør en grundig, proaktiv arkitektonisk analyse av dette minihus-konseptet på 78 m² på Grefstadveien 81:

{DESIGN_SPECS}

Sammenlign dette utkastet med profesjonell arkitekturpraksis i Norge og TEK17-standarder:
1. Soneinndeling (privat vs. offentlig sone): Er soverommet og separat WC optimalt plassert i forhold til stuen?
2. VVS og rørøkonomi: Er bad, WC og kjøkken plassert slik at rørføringen samles effektivt, og hvordan kan det optimaliseres?
3. Dagslys og solforhold: Hvordan utnytter vinduene mot sør/vest tomten på Grefstadveien 81 best?
4. Robotstøvsuger-optimaliseringen: Hva er de arkitektoniske fordelene ved å integrere dockingstasjonen i den tekniske boden?
5. Kom med 3 konkrete, proaktive designforbedringer som en profesjonell arkitekt ville foreslått for å maksimere romfølelsen (f.eks. siktlinjer, takhøyde/pulttak, skyvedører).

Svar på NORSK, i en profesjonell, direkte og analytisk tone. Svaret skal formateres med ren HTML-kode (uten ```html innpakning), klar til å settes inn på en nettside, med mørke-grønne terminalstiler som passer til resten av siden.
"""

def generate_report():
    print(f"Søker råd hos lokal Ollama-forskningsserver ({MODEL_NAME})...")
    payload = {
        "model": MODEL_NAME,
        "prompt": PROMPT,
        "stream": False
    }
    
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(OLLAMA_URL, data=json.dumps(payload).encode('utf-8'), headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            ollama_response = res_data.get("response", "")
            
            # Wrap in a beautiful retro-green terminal HTML template
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            html_content = f"""<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ollama Arkitekt-Rapport</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
        body {{
            background-color: #050a05;
            color: #00ff00;
            font-family: 'Share Tech Mono', monospace;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
            text-shadow: 0 0 5px rgba(0, 255, 0, 0.5);
        }}
        body::after {{
            content: " ";
            display: block;
            position: fixed;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            aspect-ratio: 1;
            background-size: 100% 4px, 6px 100%;
            z-index: 9999;
            pointer-events: none;
        }}
        .terminal {{
            max-width: 1000px;
            margin: 0 auto;
            border: 2px solid #00ff00;
            background-color: #030703;
            padding: 30px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
        }}
        header {{
            border-bottom: 2px solid #00ff00;
            padding-bottom: 15px;
            margin-bottom: 25px;
        }}
        .box {{
            border: 1px solid #00ff00;
            padding: 20px;
            margin-bottom: 25px;
            background-color: #040904;
            line-height: 1.6;
        }}
        h1, h2, h3 {{
            color: #00ff00;
            margin-top: 0;
        }}
        h2 {{
            border-bottom: 1px dashed #00ff00;
            padding-bottom: 5px;
            margin-top: 30px;
        }}
        a {{
            color: #00ff00;
            text-decoration: underline;
        }}
        a:hover {{
            background-color: #00ff00;
            color: #000000;
        }}
    </style>
</head>
<body>
    <div class="terminal">
        <header>
            <div style="display: flex; justify-content: space-between;">
                <span>STASJON ID: OLLAMA-RESEARCH-SERVER</span>
                <span>DATO: {current_time}</span>
            </div>
            <h1 style="margin: 10px 0 0 0;">OLLAMA ANALYSE: Arkitektonisk Sammenligning</h1>
            <div style="font-weight: bold; margin-top: 5px;">KILDE: {MODEL_NAME}</div>
        </header>

        <div class="box">
            {ollama_response}
        </div>

        <p><a href="index.html">&lt;&lt; Tilbake til hovedterminalen</a></p>
    </div>
</body>
</html>
"""
            with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"Suksess! Rapport skrevet til {OUTPUT_PATH}")
            
    except Exception as e:
        print(f"Feil ved kommunikasjon med Ollama: {e}")

if __name__ == "__main__":
    generate_report()
