import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def random_sleep(min_seconds, max_seconds):
    """Pause aléatoire entre min_seconds et max_seconds."""
    time.sleep(random.uniform(min_seconds, max_seconds))

def simulate_mouse_movements(driver):
    """
    Simule des mouvements de souris aléatoires et quelques défilements.
    """
    actions = ActionChains(driver)
    
    # Déplacements aléatoires par petits offsets
    for _ in range(random.randint(3, 6)):
        x_offset = random.randint(-100, 100)
        y_offset = random.randint(-100, 100)
        actions.move_by_offset(x_offset, y_offset)
        actions.pause(random.uniform(0.5, 1.5))
    actions.perform()
    
    # Réinitialiser la position vers le centre de la page
    try:
        body = driver.find_element("tag name", "body")
        actions.move_to_element(body).perform()
    except Exception:
        pass
    
    # Simuler quelques défilements (scroll down)
    try:
        for _ in range(random.randint(1, 3)):
            body.send_keys(Keys.PAGE_DOWN)
            random_sleep(1, 2)
    except Exception:
        pass

def simulate_human_behavior(driver):
    """
    Combine des mouvements de souris et des pauses pour simuler un comportement humain.
    """
    simulate_mouse_movements(driver)
    random_sleep(1, 3)

def main():
    options = uc.ChromeOptions()
    # En environnement GitHub Actions, le mode headless est indispensable
    options.headless = True

    # Options pour limiter la détection d'automatisation
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Pour GitHub Actions, le binaire Chrome est généralement ici :
    options.binary_location = "/usr/bin/google-chrome"
    
    # Initialiser le driver en forçant l'utilisation d'une version compatible avec Chrome 132
    driver = uc.Chrome(version_main=132, options=options)
    
    try:
        # 1. Charger la première URL
        url1 = "https://www.transavia.com/fr-FR/book-a-flight/flights/search/?r=True&ap=4&cp=0&ip=0&ds=ORY&as=IST&od=13&om=4&oy=2025&id=22&im=4&iy=2025&fb=false"
        print("Ouverture de la première URL...")
        driver.get(url1)
        time.sleep(5)  # Attendre 5 secondes pour le chargement
        simulate_human_behavior(driver)
        
        # 2. Charger la deuxième URL
        url2 = "https://www.transavia.com/fr-FR/book-a-flight/flights/search/#month-view"
        print("Ouverture de la deuxième URL...")
        driver.get(url2)
        time.sleep(5)
        simulate_human_behavior(driver)
        
        # 3. Charger la troisième URL
        url3 = "https://www.transavia.com/fr-FR/reservez-un-vol/vols/calendar/"
        print("Ouverture de la troisième URL...")
        driver.get(url3)
        time.sleep(10)
        simulate_human_behavior(driver)
        
        # 4. Extraction du contenu textuel de la troisième page
        print("Extraction du contenu textuel de la troisième page...")
        body = driver.find_element("tag name", "body")
        page_text = body.text
        
        print("Contenu extrait de la troisième page :\n")
        print(page_text)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
