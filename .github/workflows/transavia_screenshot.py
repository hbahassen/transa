import asyncio
import random
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def simulate_human_interaction(page):
    """Simule des mouvements de souris aléatoires et un défilement naturel."""
    # Simuler plusieurs déplacements de la souris
    for _ in range(random.randint(3, 5)):
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        steps = random.randint(10, 30)
        await page.mouse.move(x, y, steps=steps)
        await asyncio.sleep(random.uniform(0.5, 1.5))
    
    # Récupérer la hauteur totale de la page
    total_height = await page.evaluate("document.body.scrollHeight")
    
    # Défilement progressif (vers le bas)
    for pos in range(0, total_height // 2, 200):
        await page.evaluate(f"window.scrollTo(0, {pos})")
        await asyncio.sleep(random.uniform(0.5, 1))
    
    # Pause, puis retour vers le haut
    await asyncio.sleep(random.uniform(1, 2))
    await page.evaluate("window.scrollTo(0, 0)")
    await asyncio.sleep(random.uniform(1, 2))

async def main():
    async with async_playwright() as p:
        # Lance Chromium en mode non-headless (affichage visible)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Appliquer le plugin stealth pour masquer certains indices d'automatisation
        await stealth_async(page)

        # URL cible
        url = ("https://www.transavia.com/fr-FR/book-a-flight/flights/search/"
               "?r=True&ap=1&cp=0&ip=0&ds=ORY&as=AGA&od=14&om=2&oy=2025&id=25&im=2&iy=2025&fb=false")
        print(f"Navigation vers {url} ...")
        await page.goto(url, wait_until="networkidle")
        
        # Attendre quelques secondes pour être certain que la page est chargée
        await asyncio.sleep(5)
        
        # Simuler des interactions humaines (mouvements de souris et défilement)
        await simulate_human_interaction(page)
        
        # Attendre qu'un élément clé (par exemple, le calendrier) soit présent
        try:
            await page.wait_for_selector(".c-calendar", timeout=15000)
            print("Elément du calendrier détecté.")
        except Exception as e:
            print("Elément du calendrier non détecté:", e)
        
        # Attendre un peu de temps supplémentaire pour le rendu complet
        await asyncio.sleep(5)
        
        # Prendre une capture d'écran complète de la page
        screenshot_path = "transavia_homepage.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"Capture d'écran enregistrée sous {screenshot_path}")

        await browser.close()

asyncio.run(main())
