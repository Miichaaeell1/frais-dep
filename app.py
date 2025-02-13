import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Titre de l'application
st.title("Calculateur de Distance et Coût du Péage avec Mappy.fr")

# Saisie des adresses
address1 = st.text_input("Entrez la première adresse (ex: Lyon 69001-69009)")
address2 = st.text_input("Entrez la deuxième adresse (ex: Dijon 21000)")

def get_toll_cost_mappy(address1, address2):
    """Scrape Mappy.fr pour obtenir le coût du péage avec Selenium et Browserless."""
    # Configurer Selenium pour utiliser Browserless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # URL de Browserless (vous devez créer un compte et obtenir une clé API)
    browserless_url = "wss://chrome.browserless.io?token=VOTRE_CLE_API"
    driver = webdriver.Remote(
        command_executor=browserless_url,
        options=chrome_options
    )

    try:
        # Construire l'URL de recherche Mappy
        url = f"https://fr.mappy.com/itineraire#/voiture/{address1}/{address2}/car/5"
        driver.get(url)
        
        # Attendre que le bloc contenant le coût du péage soit présent
        wait = WebDriverWait(driver, 20)  # Attendre jusqu'à 20 secondes
        toll_block = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div._FKR1"))
        )
        
        # Extraire tous les éléments <span> avec la classe MLSqu dans ce bloc
        toll_cost_elements = toll_block.find_elements(By.CSS_SELECTOR, "span.MLSqu")
        
        # Extraire le coût du péage (dernier élément)
        if toll_cost_elements:
            toll_cost = toll_cost_elements[-1].text.strip()  # Prendre le dernier élément
            return toll_cost
        else:
            st.error("Coût du péage non trouvé sur Mappy.fr.")
            return None
    except Exception as e:
        st.error(f"Erreur lors du scraping de Mappy.fr : {e}")
        return None
    finally:
        driver.quit()  # Fermer le navigateur

# Bouton pour lancer le calcul
if st.button("Calculer le coût du péage avec Mappy.fr"):
    if address1 and address2:
        # Remplacer les espaces par "%20" pour l'URL
        address1_formatted = address1.replace(" ", "%20")
        address2_formatted = address2.replace(" ", "%20")
        
        # Obtenir le coût du péage
        toll_cost = get_toll_cost_mappy(address1_formatted, address2_formatted)
        if toll_cost:
            st.success(f"Coût estimé du péage : {toll_cost}")
    else:
        st.warning("Veuillez entrer deux adresses valides.")
