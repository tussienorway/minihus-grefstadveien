import asyncio
import time
import os
import random
from playwright.async_api import async_playwright

class PlaywrightBrowserDriver:
    def __init__(self, headless=True, user_data_dir="/home/tussie/hermes-control/browser_session"):
        self.headless = headless
        self.user_data_dir = user_data_dir
        self.playwright = None
        self.context = None
        self.page = None
        
    async def start(self):
        print("Starting Chromium Playwright browser...")
        self.playwright = await async_playwright().start()
        # Use persistent context to preserve cookies and sessions
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=self.headless,
            viewport={"width": 1280, "height": 800},
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        print("Browser started successfully.")

    async def stop(self):
        if self.context:
            await self.context.close()
        if self.playwright:
            await self.playwright.stop()
        print("Browser stopped.")

    async def open_url(self, url):
        print(f"Opening URL: {url}")
        await self.page.goto(url, wait_until="networkidle")
        await asyncio.sleep(random.uniform(1.0, 2.5)) # Human-like pause

    async def screenshot(self, step_name):
        os.makedirs("/home/tussie/control_screenshots", exist_ok=True)
        path = f"/home/tussie/control_screenshots/{step_name}_{int(time.time())}.png"
        await self.page.screenshot(path=path)
        print(f"Screenshot saved to: {path}")
        return path

    async def click(self, selector):
        print(f"Clicking on selector: {selector}")
        # Human-like delay and mouse movements
        element = await self.page.wait_for_selector(selector, state="visible")
        box = await element.bounding_box()
        if box:
            # Simulate moving to coordinate
            x = box["x"] + box["width"] / 2
            y = box.get("y", 0) + box.get("height", 0) / 2
            await self.page.mouse.move(x, y, steps=10) # 10 steps for smooth movement
            await self.page.mouse.click(x, y)
        else:
            await self.page.click(selector)
        await self.screenshot(f"click_{selector.replace('/', '_')}")
        await asyncio.sleep(0.5)

    async def type(self, selector, text, mask_log=False):
        logged_text = "***" if mask_log else text
        print(f"Typing into {selector}: {logged_text}")
        await self.page.focus(selector)
        for char in text:
            await self.page.keyboard.type(char)
            # Human-like typing speed variation
            import random
            await asyncio.sleep(random.uniform(0.05, 0.15))
        await self.page.press(selector, "Enter") # Standard submit action

    def press_key(self, key):
        print(f"Pressing key: {key}")
        self.page.keyboard.press(key)

    def wait_for_text(self, text, timeout_sec=30):
        print(f"Waiting for text: '{text}'...")
        try:
            self.page.wait_for_selector(f"text={text}", timeout=timeout_sec*1000)
            return True
        except Exception as e:
            print(f"Timed out waiting for text: {text}")
            return False
