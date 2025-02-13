import streamlit as st
import requests

# Charger la clé API depuis les secrets Streamlit
ORS_API_KEY = st.secrets["ORS_API_KEY"]
ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

# Fonction pour calculer la distance entre deux adresses via l'API OpenRouteService
def calculer_distance(adresse_destination):
    origine = "14F rue Pierre de Coubertin, 21000 DIJON"
    
    # Géocodage des adresses
    def geocoder(adresse):
        geo_url = f"https://api.openrouteservice.org/geocode/search?api_key={ORS_API_KEY}&text={adresse}"
        response = requests.get(geo_url).json()
        if "features" not in response or len(response["features"]) == 0:
            raise ValueError(f"Erreur de géocodage pour l'adresse : {adresse}")
        coordinates = response["features"][0]["geometry"]["coordinates"]
        return coordinates
    
    try:
        coord_origine = geocoder(origine)
        coord_destination = geocoder(adresse_destination)
        
        # Calcul de l'itinéraire
        route_params = {
            "api_key": ORS_API_KEY,
            "start": f"{coord_origine[0]},{coord_origine[1]}",
            "end": f"{coord_destination[0]},{coord_destination[1]}"
        }
        route_response = requests.get(ORS_URL, params=route_params).json()
        if "routes" not in route_response or len(route_response["routes"]) == 0:
            raise ValueError("Erreur de calcul de l'itinéraire")
        
        distance_km = route_response["routes"][0]["summary"]["distance"] / 1000  # Conversion en km
        return distance_km * 2  # Aller-retour
    except Exception as e:
        st.error(f"Erreur : {e}")
        return None

# Fonction pour calculer les frais de déplacement
def calculer_frais_deplacement(prix_carburant, distance_km, quote_part,
                                hebergement, restauration, nb_repas,
                                parking_par_jour, nb_jours):
    carburant_total = (distance_km) * (prix_carburant / 100) * quote_part / 100
    sous_total_hebergement = hebergement
    sous_total_restauration = restauration * nb_repas
    sous_total_parking = parking_par_jour * nb_jours
    total_deplacement = (carburant_total + sous_total_hebergement +
                         sous_total_restauration + sous_total_parking)
    return {
        "Carburant aller-retour (€)": carburant_total,
        "Sous-total hébergement (€)": sous_total_hebergement,
        "Sous-total restauration (€)": sous_total_restauration,
        "Sous-total parking (€)": sous_total_parking,
        "Total déplacement (€)": total_deplacement
    }

# Interface Streamlit
st.title("Calcul des frais de déplacement")

prix_carburant = st.number_input("Prix du carburant (€)", value=1.85)
destination = st.text_input("Destination", "Paris")
quote_part = st.number_input("Quote-part voiture (%)", value=50)
hebergement = st.number_input("Coût de l'hébergement (€)", value=150)
restauration = st.number_input("Coût de la restauration par repas (€)", value=60)
nb_repas = st.number_input("Nombre de repas", value=2, step=1)
parking_par_jour = st.number_input("Coût du parking par jour (€)", value=25)
nb_jours = st.number_input("Nombre de jours de déplacement", value=2, step=1)

if st.button("Calculer"):
    distance_km = calculer_distance(destination)
    if distance_km is None:
        st.error("Impossible de calculer la distance. Vérifiez l'adresse entrée.")
    else:
        resultats = calculer_frais_deplacement(
            prix_carburant, distance_km, quote_part,
            hebergement, restauration, nb_repas,
            parking_par_jour, nb_jours
        )
        st.write(f"### Distance aller-retour : {distance_km:.2f} km")
        st.write("### Résultats :")
        for cle, valeur in resultats.items():
            st.write(f"{cle} : {valeur:.2f} €")
