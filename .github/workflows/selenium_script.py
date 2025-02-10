import time
import undetected_chromedriver as uc

# Configuration des options pour undetected_chromedriver
options = uc.ChromeOptions()
# En environnement GitHub Actions, il faut exécuter en mode headless
options.headless = True
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--remote-debugging-port=9222")

# Spécifier le chemin du binaire de Google Chrome (sur ubuntu-latest, il se trouve généralement ici)
options.binary_location = "/usr/bin/google-chrome"

# Forcer l'utilisation d'une version compatible avec Chrome 132
driver = uc.Chrome(version_main=132, options=options)

try:
    # 1. Ouvrir la première URL
    url1 = "https://www.transavia.com/fr-FR/book-a-flight/flights/search/?r=True&ap=4&cp=0&ip=0&ds=ORY&as=IST&od=13&om=4&oy=2025&id=22&im=4&iy=2025&fb=false"
    print("Ouverture de la première URL...")
    driver.get(url1)
    time.sleep(5)  # Attendre 5 secondes pour être sûr du chargement

    # 2. Ouvrir la deuxième URL
    url2 = "https://www.transavia.com/fr-FR/book-a-flight/flights/search/#month-view"
    print("Ouverture de la deuxième URL...")
    driver.get(url2)
    time.sleep(5)  # Attendre 5 secondes

    # 3. Ouvrir la troisième URL
    url3 = "https://www.transavia.com/fr-FR/reservez-un-vol/vols/calendar/"
    print("Ouverture de la troisième URL...")
    driver.get(url3)
    time.sleep(10)  # Attendre 10 secondes pour s'assurer du chargement complet

    # 4. Extraction du contenu textuel de la troisième page
    print("Extraction du contenu textuel de la troisième page...")
    body = driver.find_element("tag name", "body")
    page_text = body.text

    print("Contenu extrait de la troisième page :\n")
    print(page_text)

finally:
    driver.quit()
