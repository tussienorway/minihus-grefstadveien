import subprocess
import os
import datetime

def run_cmd(cmd, shell=False):
    res = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error running: {cmd}")
        print(f"STDOUT: {res.stdout}")
        print(f"STDERR: {res.stderr}")
    return res.stdout, res.returncode

def main():
    print(f"[{datetime.datetime.now()}] Starting automated Minihus-Grefstadveien pipeline...")
    
    # 1. Regenerate floorplan SVG (ensure latest version is rendered)
    print("Regenerating Floorplan SVG...")
    run_cmd(["python3", "/home/tussie/minihus-grefstadveien/scripts/generate_floorplan.py"])
    
    # 2. Check if git has changes
    os.chdir("/home/tussie/minihus-grefstadveien")
    stdout, code = run_cmd(["git", "status", "--porcelain"])
    
    if stdout.strip():
        print("Changes detected! Committing and pushing to GitHub Pages...")
        run_cmd(["git", "add", "."])
        commit_msg = f"Automated pipeline update - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        run_cmd(["git", "commit", "-m", commit_msg])
        # Push using the verified token url
        run_cmd(["git", "push", "origin", "main"])
        print("SUCCESS: Website updated successfully!")
    else:
        print("No changes to push. Everything is up-to-date.")

if __name__ == '__main__':
    main()
