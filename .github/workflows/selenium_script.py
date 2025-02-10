import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests

def random_sleep(min_seconds, max_seconds):
    """Pause aléatoire entre min_seconds et max_seconds."""
    time.sleep(random.uniform(min_seconds, max_seconds))

def simulate_human_behavior(driver):
    """Simule quelques actions humaines simples (mouvements de souris et délais)."""
    actions = ActionChains(driver)
    # Déplacement aléatoire
    for _ in range(random.randint(2, 4)):
        x_offset = random.randint(-50, 50)
        y_offset = random.randint(-50, 50)
        actions.move_by_offset(x_offset, y_offset)
        actions.pause(random.uniform(0.5, 1))
    actions.perform()
    random_sleep(1, 3)

def get_cookies_string(driver):
    """Extrait les cookies de la session Selenium et les convertit en chaîne pour requests."""
    cookies = driver.get_cookies()
    return "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

def main():
    # Configuration de Selenium avec undetected_chromedriver
    options = uc.ChromeOptions()
    # Pour simuler un comportement plus humain, nous ouvrons le navigateur en mode visible.
    # En environnement CI (GitHub Actions) vous devrez peut-être utiliser le mode headless.
    options.headless = False  
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    # Si nécessaire, précisez le chemin du binaire de Chrome (ex. sur Ubuntu : /usr/bin/google-chrome)
    # options.binary_location = "/usr/bin/google-chrome"
    
    # Forcer l'utilisation d'une version compatible (ex. version 132 si c'est votre version installée)
    driver = uc.Chrome(version_main=132, options=options)
    
    try:
        # 1. Ouvrir la première URL dans la même fenêtre
        url1 = ("https://www.transavia.com/fr-FR/book-a-flight/flights/search/"
                "?r=True&ap=4&cp=0&ip=0&ds=ORY&as=IST&od=13&om=4&oy=2025&id=22&im=4&iy=2025&fb=false")
        print("Ouverture de la première URL...")
        driver.get(url1)
        time.sleep(5)
        simulate_human_behavior(driver)
        
        # 2. Ouvrir la deuxième URL dans la même fenêtre
        url2 = "https://www.transavia.com/fr-FR/book-a-flight/flights/search/#month-view"
        print("Ouverture de la deuxième URL...")
        driver.get(url2)
        time.sleep(5)
        simulate_human_behavior(driver)
        
        # À ce stade, la page 2 a effectué en arrière-plan des requêtes XHR
        # qui contiennent l'URL de la troisième page.
        # Au lieu d'ouvrir la troisième page dans le navigateur, nous allons la récupérer via requests.
        
        # Extraire la chaîne de cookies depuis la session Selenium
        cookies_str = get_cookies_string(driver)
        
        # Préparer les en-têtes tels que reproduits depuis votre commande cURL
        headers = {
            "authority": "www.transavia.com",
            "accept": "*/*",
            "accept-language": "fr-FR,fr;q=0.9",
            "cookie": cookies_str,
            "referer": "https://www.transavia.com/fr-FR/book-a-flight/flights/search/",
            "request-context": "appId=cid-v1:942f733a-0e08-45b5-a6e2-53089f65a4b2",
            "request-id": "|c37de72e6ee3482ca4352554c4d037a0.827e5395e242446f",
            "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "traceparent": "00-c37de72e6ee3482ca4352554c4d037a0-827e5395e242446f-01",
            "user-agent": ("Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36"),
            "x-requested-with": "XMLHttpRequest"
        }
        
        # L'URL de la requête XHR (d'après votre copie cURL)
        third_url = "https://www.transavia.com/fr-FR/reservez-un-vol/vols/calendar/"
        print("Exécution d'une requête GET sur l'URL XHR (troisième URL) via requests...")
        response = requests.get(third_url, headers=headers)
        if response.status_code == 200:
            print("Contenu récupéré avec succès :\n")
            print(response.text)
        else:
            print(f"Échec de la récupération, code de statut: {response.status_code}")
            print(response.text)
            
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
