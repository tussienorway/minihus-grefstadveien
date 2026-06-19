import asyncio
import os
import sys
from playwright.async_api import async_playwright

ENV_PATH = "/home/tussie/.config/hermes-control/.env"

def load_credentials():
    email = None
    password = None
    if not os.path.exists(ENV_PATH):
        print(f"Feil: Fant ikke .env filen på {ENV_PATH}")
        return None, None
        
    with open(ENV_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("GMAIL_EMAIL="):
                email = line.split("=", 1)[1].strip()
            elif line.startswith("GMAIL_PASSWORD="):
                password = line.split("=", 1)[1].strip()
    return email, password

async def run_gmail_login():
    email, password = load_credentials()
    if not email or not password:
        print("Kunne ikke laste GMAIL_EMAIL eller GMAIL_PASSWORD fra .env.")
        print("Vennligst legg dem inn i ~/.config/hermes-control/.env som:")
        print("GMAIL_EMAIL=din_epost@gmail.com")
        print("GMAIL_PASSWORD=ditt_passord")
        return
        
    print(f"Forsøker pålogging for: {email}...")
    
    async with async_playwright() as p:
        # Launch browser with standard user-agent to reduce bot detection
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # 1. Naviger til Google Sign-In
        print("Trinn 1: Navigerer til Google pålogging...")
        await page.goto("https://accounts.google.com/signin", wait_until="networkidle")
        await page.screenshot(path="/home/tussie/minihus-grefstadveien/gmail_step_1_landing.png")
        
        # 2. Skriv inn e-post
        print("Trinn 2: Skriver inn e-post...")
        await page.fill('input[type="email"]', email)
        await page.screenshot(path="/home/tussie/minihus-grefstadveien/gmail_step_2_email_typed.png")
        await page.press('input[type="email"]', "Enter")
        await asyncio.sleep(4.0) # Vent på animasjon og neste side
        
        await page.screenshot(path="/home/tussie/minihus-grefstadveien/gmail_step_3_after_email.png")
        
        # Sjekk om Google blokkerte oss med "secure browser" feil
        content = await page.content()
        if "Den nettleseren eller appen er kanskje ikke sikker" in content or "This browser or app may not be secure" in content:
            print("🚨 Google blokkerte påloggingen: 'Nettleseren er ikke sikker' (Bot Detection).")
            print("Vi må bruke en eksisterende brukerprofil eller et App-passord via IMAP i stedet.")
            await browser.close()
            return
            
        # 3. Skriv inn passord
        print("Trinn 3: Skriver inn passord...")
        try:
            await page.fill('input[type="password"]', password)
            await page.screenshot(path="/home/tussie/minihus-grefstadveien/gmail_step_4_password_typed.png")
            await page.press('input[type="password"]', "Enter")
            await asyncio.sleep(5.0)
        except Exception as e:
            print(f"Klarte ikke å finne passordfeltet: {e}")
            await browser.close()
            return
            
        await page.screenshot(path="/home/tussie/minihus-grefstadveien/gmail_step_5_after_password.png")
        
        # Sjekk for 2FA / To-trinns bekreftelse
        content = await page.content()
        if "to-trinns" in content.lower() or "verification" in content.lower() or "2-step" in content.lower():
            print("⏰ 2FA trigget! Sjekk mobilen din og trykk JA/Godkjenn nå. Venter i 30 sekunder...")
            await asyncio.sleep(30.0)
            await page.screenshot(path="/home/tussie/minihus-grefstadveien/gmail_step_6_after_2fa_wait.png")
            
        # Sjekk om vi lyktes
        await page.goto("https://mail.google.com/mail/u/0/", wait_until="networkidle")
        await page.screenshot(path="/home/tussie/minihus-grefstadveien/gmail_step_7_final_gmail.png")
        
        content = await page.content()
        if "inbox" in content.lower() or "innboks" in content.lower() or "skriv" in content.lower():
            print("🎉 SUKSESS! Vi har logget inn på din Gmail!")
        else:
            print("Pålogging fullført, men kunne ikke verifisere innboksen. Sjekk skjermbilder under /home/tussie/minihus-grefstadveien/")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_gmail_login())
