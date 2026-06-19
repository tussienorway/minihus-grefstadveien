import os
import sys
import shutil

class SecurityManager:
    TRIGGER_PATH = "/home/tussie/hermes-control/kill_switch.trigger"

    def check_kill_switch(self):
        """Checks if the kill switch is triggered."""
        if os.path.exists(self.TRIGGER_PATH):
            print("!!! PANIC BUTTON TRIGGERED !!!")
            print("Terminating process immediately to prevent damage.")
            # Remove trigger file so it doesn't loop infinitely on restart
            try:
                os.remove(self.TRIGGER_PATH)
            except Exception:
                pass
            sys.exit(911) # Force exit code 911 for emergency shutdown

    def trigger_kill_switch(self):
        """Triggers the kill switch manually."""
        os.makedirs(os.path.dirname(self.TRIGGER_PATH), exist_ok=True)
        with open(self.TRIGGER_PATH, "w") as f:
            f.write("PANIC")
        print("Panic button written to disk.")

    def load_secure_env(self, env_path="/home/tussie/.config/hermes-control/.env"):
        """Loads environment variables securely from .env."""
        if not os.path.exists(env_path):
            print("Secure env file not found.")
            return False
            
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()
        print("Secure environment variables loaded.")
        return True
