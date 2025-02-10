import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def random_sleep(min_seconds, max_seconds):
    """Attend un temps aléatoire entre min_seconds et max_seconds."""
    duration = random.uniform(min_seconds, max_seconds)
    time.sleep(duration)

def simulate_mouse_movements(driver):
    """
    Simule des mouvements de souris aléatoires et des défilements,
    imitant ainsi des actions humaines.
    """
    actions = ActionChains(driver)
    
    # Déplacer la souris par petits offsets aléatoires
    for _ in range(random.randint(3, 6)):
        x_offset = random.randint(-100, 100)
        y_offset = random.randint(-100, 100)
        actions.move_by_offset(x_offset, y_offset)
        actions.pause(random.uniform(0.5, 1.5))
    actions.perform()
    
    # Réinitialiser la position de la souris en la déplaçant vers le centre de la page
    actions.move_to_element(driver.find_element("tag name", "body")).perform()
    
    # Simuler quelques défilements (scroll down)
    body = driver.find_element("tag name", "body")
    for _ in range(random.randint(1, 3)):
        body.send_keys(Keys.PAGE_DOWN)
        random_sleep(1, 2)

def simulate_human_behavior(driver):
    """
    Simule des comportements humains en combinant mouvements de souris et pauses.
    """
    simulate_mouse_movements(driver)
    random_sleep(1, 3)

def main():
    # Configuration des options pour undetected_chromedriver
    options = uc.ChromeOptions()
    # Pour simuler un comportement humain, il est préférable de ne pas utiliser le mode headless.
    # Si vous devez exécuter en headless (par exemple dans un environnement CI), sachez que cela peut être détecté.
    # options.headless = True  # Désactivé ici pour simuler un usage réel
    
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    # Si nécessaire, indiquez le chemin du binaire Chrome (sur Ubuntu, généralement "/usr/bin/google-chrome")
    # options.binary_location = "/usr/bin/google-chrome"
    
    # Forcer l'utilisation d'une version compatible avec votre Chrome installé (ici, version 132 par exemple)
    driver = uc.Chrome(version_main=132, options=options)

    try:
        # 1. Ouvrir la première URL dans la même fenêtre
        url1 = "https://www.transavia.com/fr-FR/book-a-flight/flights/search/?r=True&ap=4&cp=0&ip=0&ds=ORY&as=IST&od=13&om=4&oy=2025&id=22&im=4&iy=2025&fb=false"
        print("Ouverture de la première URL...")
        driver.get(url1)
        random_sleep(3, 5)
        simulate_human_behavior(driver)
        
        # 2. Ouvrir la deuxième URL dans le même onglet
        url2 = "https://www.transavia.com/fr-FR/book-a-flight/flights/search/#month-view"
        print("Ouverture de la deuxième URL...")
        driver.get(url2)
        random_sleep(3, 5)
        simulate_human_behavior(driver)
        
        # 3. Ouvrir la troisième URL dans le même onglet
        url3 = "https://www.transavia.com/fr-FR/reservez-un-vol/vols/calendar/"
        print("Ouverture de la troisième URL...")
        driver.get(url3)
        random_sleep(5, 10)
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
