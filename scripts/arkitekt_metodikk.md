# UTREDNING: Hvordan JARVIS skal tegne som en profesjonell arkitekt

Dette dokumentet beskriver den eksakte læringsmodellen, dataflyten og de beregningsmessige strategiene jeg vil bruke for å gå fra enkle 2D-skisser til produksjonsklare arkitekttegninger av høyeste kvalitet, fullt kompatible med norske byggestandarder (TEK17).

---

## 1. Regelbasert Constraint-Engine (TEK17 som harde rammer)
En ekte arkitekt tegner ikke vilkårlige linjer; de tegner innenfor et strengt geometrisk og lovpålagt rammeverk. Jeg vil programmere et sett med **harde parametriske grenser** direkte inn i tegnepipelinen:

*   **Snuareal (Universell utforming):** Selv om vi prioriterer robotstøvsugere, sikrer vi at bad, soverom og entré har en uavbrutt snusirkel på minimum **1,5 meter** i diameter. Dette gjør at søknaden glir rett gjennom hos kommunen uten dispensasjonssøknader.
*   **Dagslysforhold (Dagslysfaktor):** Vi programmerer en sjekk som sikrer at det totale glassarealet (vinduer) i oppholdsrom (stue/kjøkken) utgjør minimum **10 % av bruksarealet** (dvs. over 5 m² glass for stue/kjøkken), og at dagslyskravet i TEK17 § 13-7 er oppfylt.
*   **Rømningsveier og brannsikkerhet:** Soverom og stue skal ha direkte rømning via vinduer som oppfyller minstekravene (fri bredde x høyde overstiger 1,5 meter til sammen, og minimum 0,5 meter bredde).

---

## 2. Sirkulasjonsflyt og VVS-optimalisering (Det funksjonelle designet)
For å gjøre minihuset billig å bygge og ekstremt behagelig å bo i, bruker vi **geometrisk optimalisering**:

*   **VVS-vegg (Plumbing Wall):** Vi plasserer badet, det separate toalettet og kjøkkenet "rygg-mot-rygg" eller på linje. Dette samler alle vann- og avløpsrør i én enkelt kjerne. Dette sparer titusenvis av kroner i rørleggerarbeid og reduserer faren for frostskader.
*   **Siktlinjer (Sightlines):** Vi definerer siktlinje-vektorer. For eksempel: Når du åpner inngangsdøren, skal siktlinjen lede mot stuevinduet og hagen, aldri rett inn på toalettet eller badet.
*   **Møblerbarhet:** Vi tegner inn standardmøbler (1,8m dobbeltseng, 2,2m sofa, kjøkkenbenk på 60cm dybde) som faste geometriske blokker for å verifisere at det faktisk er plass til å gå rundt dem (minst 70 cm fri passasje).

---

## 3. "Juksing" via Vektor-parsing (Reverse-Engineering)
Jeg vil ikke finne opp hjulet på nytt. Vi bruker eksisterende, prisvinnende skandinaviske arkitekttegninger som råmateriale:

*   **DXF/PDF-Parsing:** Jeg bruker skript til å scanne offentlige databaser for godkjente minihus- og hytteprosjekter i Norge. 
*   **Nodepunktekstraksjon:** Vi pakker ut de rå vektorkoordinatene for vegger, dørkarmer og trappeløsninger fra disse filene, skalerer dem, og bruker dem som ferdige "moduler" i våre egne tegninger.
*   **Modulær arkitektur:** Vi lager et bibliotek av ferdige, TEK17-godkjente moduler (f.eks. "optimalt bad på 8m²", "kompakt kjøkken på 12m²") som vi kan flytte rundt på tomten.

---

## 4. Den Generative og Adversarielle loopen (Kritikeren)
Dette er hjernen i prosessen. Tegningen itereres gjennom en lukket feedback-sløyfe:

```
[Draftsman Agent] (Genererer SVG-planløsning basert på råmål)
       │
       ▼
[Render Agent] (Genererer høyoppløselig 2D/3D bilde)
       │
       ▼
[Critic Agent (Gemini 3.5 Pro)] (Analyserer bildet med datasyn)
       │
       ├─► Feil funnet? (F.eks: "Dør slår inn i kjøkkenbenk", "Soverom for mørkt")
       │         │
       │         ▼
       │   [Koordinat-korreksjon sendes tilbake til Draftsman]
       │
       └─► OK! ──► [Eksport til produksjonsformater: DXF, PDF, IFC]
```

---

## 5. Eksport til Ekte Byggeformater (Byggeklart)
Håndverkere bruker ikke SVG-filer fra nettsider. For at prosjektet skal kunne bygges, vil vår pipeline automatisk generere:

*   **DXF (Drawing Exchange Format):** To-dimensjonale CAD-tegninger som tømrere og CNC-maskiner kan lese direkte for å kappe stendere og bjelkelag med millimeterpresisjon.
*   **IFC (Industry Foundation Classes):** Hvis vi oppgraderer til 3D BIM, eksporterer vi standard IFC-modeller slik at tekniske installatører (elektriker/VVS) kan tegne sine anlegg direkte inn i vår modell.
*   **A3 Tegningssett i PDF:** Standardiserte byggetegninger med målestokk (1:50), nordpil, tegningshode og tegnforklaringer, klare til å printes ut på byggeplassen.
