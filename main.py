import sys
import os
import argparse
import asyncio

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.browser_driver import PlaywrightBrowserDriver
from core.cli_wrapper import CLIWrapper
from core.security import SecurityManager

async def run_gui_test():
    sec = SecurityManager()
    sec.check_kill_switch()
    
    driver = PlaywrightBrowserDriver(headless=True)
    try:
        await driver.start()
        sec.check_kill_switch()
        
        # Test navigating to AWS console landing
        await driver.open_url("https://aws.amazon.com/console/")
        await driver.screenshot("aws_landing_test")
        
        sec.check_kill_switch()
    except Exception as e:
        print(f"Exception during GUI test: {e}")
    finally:
        await driver.stop()

def run_cli_test():
    cli = CLIWrapper()
    # Check AWS version
    res = cli.run_aws_cmd(["--version"])
    print(f"AWS CLI check success: {res['success']}")
    print(f"AWS CLI version: {res['stdout']}")

def main():
    parser = argparse.ArgumentParser(description="Hermes VM & Browser Control Engine")
    parser.add_argument("mode", choices=["gui-test", "cli-test", "panic"], help="Execution mode")
    args = parser.parse_args()
    
    if args.mode == "gui-test":
        asyncio.run(run_gui_test())
    elif args.mode == "cli-test":
        run_cli_test()
    elif args.mode == "panic":
        sec = SecurityManager()
        sec.trigger_kill_switch()

if __name__ == "__main__":
    main()
