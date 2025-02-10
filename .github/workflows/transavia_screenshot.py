import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def main():
    async with async_playwright() as p:
        # Lance Chromium en mode headless
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Applique le stealth pour tenter de masquer les traces d'automatisation
        await stealth_async(page)

        # URL de la page Transavia
        url = "https://www.transavia.com/fr-FR/book-a-flight/flights/search/?r=True&ap=1&cp=0&ip=0&ds=ORY&as=AGA&od=14&om=2&oy=2025&id=25&im=2&iy=2025&fb=false"
        print(f"Navigation vers {url} ...")
        await page.goto(url, wait_until="networkidle")

        # Optionnel : attendre quelques secondes supplémentaires
        await asyncio.sleep(5)

        # Prendre une capture d'écran
        screenshot_path = "transavia_homepage.png"
        await page.screenshot(path=screenshot_path)
        print(f"Capture d'écran enregistrée sous {screenshot_path}")

        await browser.close()

asyncio.run(main())
