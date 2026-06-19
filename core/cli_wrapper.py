import subprocess
import os

class CLIWrapper:
    @staticmethod
    def run_command(cmd, workdir=None):
        print(f"Executing CLI command: {' '.join(cmd)}")
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=workdir)
        
        # Mask credentials if they appear in logs
        stdout = res.stdout
        stderr = res.stderr
        
        if res.returncode != 0:
            print(f"CLI execution failed with returncode: {res.returncode}")
            print(f"Error output: {stderr}")
            return {"success": False, "stdout": stdout, "stderr": stderr, "exit_code": res.returncode}
        
        return {"success": True, "stdout": stdout, "stderr": stderr, "exit_code": res.returncode}

    def run_aws_cmd(self, args):
        cmd = ["aws"] + args
        return self.run_command(cmd)

    def run_gcloud_cmd(self, args):
        cmd = ["gcloud"] + args
        return self.run_command(cmd)
