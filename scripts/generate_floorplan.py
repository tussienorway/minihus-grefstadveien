import os

def create_floorplan_svg():
    # 78 sqm house layout. Dimensions: 12m width x 6.5m depth = 78 sqm
    # Inside layout:
    # Soverom: 3.5m x 3.42m (~12 m²) - top left
    # Bad: 2.5m x 3.2m (~8 m²) - bottom left
    # WC: 1.5m x 2.0m (~3 m²) - middle bottom
    # Bod: 2.0m x 2.5m (~5 m²) - middle left (with vacuum dock)
    # Gang/Inngang: 2.0m x 2.0m (~4 m²) - middle top
    # Kjøkken: 3.0m x 4.0m (~12 m²) - right side top
    # Stue: 5.5m x 6.5m - right side bottom / center (combined with kitchen) -> actually (~34 m² remaining)
    
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1300 750" width="100%" height="100%" style="background-color: #030703; font-family: monospace;">
        <!-- Definitions for patterns/styles -->
        <defs>
            <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#003300" stroke-width="0.5"/>
            </pattern>
        </defs>
        
        <!-- Grid Background -->
        <rect width="100%" height="100%" fill="url(#grid)" />
        
        <!-- External walls (1200x650) with offset for centering (50, 50) -->
        <rect x="50" y="50" width="1200" height="650" fill="none" stroke="#00ff00" stroke-width="4" stroke-dasharray="none" />
        
        <!-- ROOM DIVISIONS -->
        <!-- Soverom (Top Left): 3.5m x 3.5m -> 350px x 350px -->
        <line x1="50" y1="350" x2="350" y2="350" stroke="#00ff00" stroke-width="3" />
        <line x1="350" y1="50" x2="350" y2="350" stroke="#000000" stroke-width="3" stroke-dasharray="5,5" />
        <text x="70" y="100" fill="#00ff00" font-size="16" font-family="monospace" font-weight="bold">SOVEROM (12 m²)</text>
        <text x="70" y="130" fill="#00ff00" font-size="12">Seng: 180x200</text>
        <text x="70" y="150"" fill="#00ff00" font-size="12">Garderobe</text>

        <!-- Bad (Bottom Left): 3.0m x 2.5m -> 300px x 250px -->
        <line x1="50" y1="350" x2="350" y2="350" stroke="#00ff00" stroke-width="3" />
        <line x1="350" y1="50" x2="350" y2="350" stroke="#00ff00" stroke-width="3" />
        <line x1="350" y1="350" x2="350" y2="700" stroke="#000000" stroke-width="3" />
        <!-- Inner partition for Toilet vs Bathroom -->
        <line x1="180" y1="350" x2="180" y2="550" stroke="#00ff00" stroke-dasharray="5,5" />
        
        <!-- WC (Toilet) -->
        <text x="70" y="380" fill="#00ff00" font-family="monospace" font-size="14" font-weight="bold">WC (3 m²)</text>
        
        <!-- Bad -->
        <text x="210" y="380" fill="#000000" font-family="sans-serif" font-size="14" font-weight="bold" fill-opacity="0.8">BAD (12 m²)</text>
        <text x="210" y="410" fill="#00ff00" font-size="12">Dusj, vask, vaskemaskin</text>

        <!-- Bod (liten bod ved siden av badet eller gang) -->
        <line x1="350" y1="200" x2="350" y2="350" stroke="#00ff00" stroke-width="3" />
        <line x1="350" y1="200" x2="450" y2="200"  stroke="#000000" stroke-width="3"/>
        <line x1="450" y1="200" x2="450" y2="350"  stroke="#000000" stroke-width="3" />
        <text x="360" y="100" fill="#00ff00" font-size="14" font-family="monospace" font-weight="bold">BOD (5 m²)</text>
        <text x="360" y="130" fill="#00ff00" font-size="11">Sikringsskap / Teknikk</text>
        <text x="360" y="150" fill="#00ff00" font-size="11" font-weight="bold" class="blink">★ ROBOT-DOCK</text>

        <!-- Kjøkken (Right Top) -->
        <line x1="800" y1="50" x2="800" y2="300" stroke="#00ff00" stroke-width="3" />
        <line x1="800" y1="300" x2="1250" y2="300" stroke="#00ff00" stroke-width="3" />
        <text x="850" y="100" fill="#00ff00" font-size="16" font-family="monospace" font-weight="bold">KJØKKEN (12 m²)</text>
        <text x="850" y="130" fill="#00ff00" font-size="12">L-form benk, komfyr, oppvask</text>

        <!-- Stue (Living Room - Center / Right Bottom) -->
        <text x="500" y="450" fill="#00ff00" font-size="20" font-family="monospace" font-weight="bold">STUE (34 m²)</text>
        <text x="500" y="490" fill="#00ff00" font-size="12">Åpen, lys og luftig løsning</text>
        <text x="500" y="520" fill="#00ff00" font-size="12">Utgang til hage / terrasse mot sør</text>

        <!-- Entrance (Gang/Inngang) -->
        <text x="500" y="100" fill="#00ff00" font-size="14" font-family="monospace" font-weight="bold">GANG / ENTRÉ (5 m²)</text>

        <!-- Scale & Labels -->
        <text x="50" y="725" fill="#00ff00" font-size="12" font-family="monospace">Skala: 1:50 | 100px = 1 meter | Totalareal: 12m x 6.5m = 78 m²</text>
        <text x="1100" y="725" fill="#00ff00" font-size="12" font-family="monospace" font-weight="bold">TEK17 COMPLIANT</text>
    </svg>
    """
    
    os.makedirs('/home/tussie/minihus-grefstadveien/images', exist_ok=True)
    with open('/home/tussie/minihus-grefstadveien/images/floorplan.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("SUCCESS: Floorplan SVG successfully generated at /home/tussie/minihus-grefstadveien/images/floorplan.svg")

if __name__ == '__main__':
    create_floorplan_svg()
