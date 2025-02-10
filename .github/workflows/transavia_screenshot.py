import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def main():
    async with async_playwright() as p:
        # Lance Chromium en mode non-headless
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Appliquer le plugin stealth (vous pouvez le commenter temporairement pour tester)
        await stealth_async(page)

        # URL cible
        url = "https://www.transavia.com/fr-FR/book-a-flight/flights/search/?r=True&ap=1&cp=0&ip=0&ds=ORY&as=AGA&od=14&om=2&oy=2025&id=25&im=2&iy=2025&fb=false"
        print(f"Navigation vers {url} ...")
        await page.goto(url, wait_until="networkidle")
        
        # Attendre explicitement que le calendrier soit présent (ajustez le sélecteur si nécessaire)
        try:
            await page.wait_for_selector('.c-calendar', timeout=15000)
            print("Calendrier détecté.")
        except Exception as e:
            print("Calendrier non détecté:", e)
        
        # Faire défiler la page pour forcer le rendu du contenu
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(2)
        
        # Prendre une capture d'écran
        screenshot_path = "transavia_homepage.png"
        await page.screenshot(path=screenshot_path)
        print(f"Capture d'écran enregistrée sous {screenshot_path}")

        await browser.close()

asyncio.run(main())
