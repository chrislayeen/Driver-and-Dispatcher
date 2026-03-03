import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        screens = [
            "Dispatcher_Dashboard.html",
            "Inspection_Review.html",
            "Issue_Review.html"
        ]
        
        base_path = r"file:///c:/Users/GamingX/Desktop/5driver/"
        artifact_dir = r"C:\Users\GamingX\.gemini\antigravity\brain\d665ad33-9b9e-4955-92dc-bd716983e9fb"
        
        for screen in screens:
            file_url = f"{base_path}{screen}"
            print(f"Loading {file_url}...")
            await page.goto(file_url)
            
            # Hover over sidebar items to trigger animations
            await page.hover("text=Dashboard")
            await page.wait_for_timeout(500)
            await page.hover("text=Approvals")
            await page.wait_for_timeout(500)
            await page.hover("text=Incidents")
            await page.wait_for_timeout(500)
            
            screenshot_path = os.path.join(artifact_dir, f"playwright_verify_{screen.split('.')[0]}.png")
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"Captured screenshot: {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
