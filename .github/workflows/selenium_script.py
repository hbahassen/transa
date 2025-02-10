import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configuration des options de Chrome en mode headless
chrome_options = Options()
chrome_options.add_argument("--headless")  # mode sans interface graphique
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

# Initialisation du driver avec webdriver_manager et l'objet Service
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 1. Ouvrir la première URL
    url1 = "https://www.transavia.com/fr-FR/book-a-flight/flights/search/?r=True&ap=4&cp=0&ip=0&ds=ORY&as=IST&od=13&om=4&oy=2025&id=22&im=4&iy=2025&fb=false"
    print("Ouverture de la première URL...")
    driver.get(url1)
    time.sleep(3)  # attendre 3 secondes

    # 2. Ouvrir la deuxième URL
    url2 = "https://www.transavia.com/fr-FR/book-a-flight/flights/search/#month-view"
    print("Ouverture de la deuxième URL...")
    driver.get(url2)
    time.sleep(2)  # attendre 2 secondes

    # 3. Ouvrir la troisième URL
    url3 = "https://www.transavia.com/fr-FR/reservez-un-vol/vols/calendar/"
    print("Ouverture de la troisième URL...")
    driver.get(url3)
    time.sleep(2)  # attendre 2 secondes pour s'assurer du chargement complet

    # 4. Extraction du texte de la troisième page
    print("Extraction du contenu textuel de la troisième page...")
    body = driver.find_element("tag name", "body")
    page_text = body.text

    # Affichage du contenu extrait
    print("Contenu extrait de la troisième page :\n")
    print(page_text)

finally:
    driver.quit()
