import sqlite3
import json
import os
from datetime import datetime, timedelta

DB_PATH = "/home/tussie/.hermes/profiles/absolute/secretary_bot/notes.db"

def inspect_and_add_note():
    if not os.path.exists(DB_PATH):
        print(f"Secretary DB not found at: {DB_PATH}")
        return
        
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Tables in DB: {tables}")
        
        if "notes" in tables:
            # Check table structure
            cursor.execute("PRAGMA table_info(notes)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"Columns in 'notes' table: {columns}")
            
            # Formulate the note
            content = "Autonome framskritt: Byggingen av kontroll-VM-rammeverket (hermes-control) er i gang! Grunnleggende browser-driver (Playwright), CLI-wrapper og sikkerhetslag (med fysisk panic button/kill-switch-sjekk) er kodet og lagret på disk under /home/tussie/minihus-grefstadveien/. Testet med CLI-suksess for AWS!"
            tags = json.dumps(["viktig", "control-vm", "hermes-control"])
            now = datetime.now()
            timestamp = now.isoformat()
            
            # Set reminder to 12 hours in the future
            reminder_time = (now + timedelta(hours=12)).isoformat()
            status = "in_progress"
            
            # Prepare insert command
            insert_query = """
            INSERT INTO notes (content, tags, timestamp, reminder_time, status)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (content, tags, timestamp, reminder_time, status))
            conn.commit()
            print("Suksess! Ny oppdatering og påminnelse om 12 timer er registrert i sekretær-databasen din!")
        else:
            print("Tabellen 'notes' eksisterer ikke i databasen.")
            
        conn.close()
    except Exception as e:
        print(f"Feil under interaksjon med sekretær-databasen: {e}")

if __name__ == "__main__":
    inspect_and_add_note()
