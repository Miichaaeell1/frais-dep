import streamlit as st

# Fonction pour calculer les frais de déplacement
def calculer_frais_deplacement(prix_carburant, distance_km, quote_part,
                                hebergement, restauration, nb_repas,
                                parking_par_jour, nb_jours):
    carburant_total = (distance_km * 2) * (prix_carburant / 100) * quote_part / 100
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
distance_km = st.number_input("Distance aller (km)", value=300)
quote_part = st.number_input("Quote-part voiture (%)", value=50)
hebergement = st.number_input("Coût de l'hébergement (€)", value=150)
restauration = st.number_input("Coût de la restauration par repas (€)", value=60)
nb_repas = st.number_input("Nombre de repas", value=2, step=1)
parking_par_jour = st.number_input("Coût du parking par jour (€)", value=25)
nb_jours = st.number_input("Nombre de jours de déplacement", value=2, step=1)

if st.button("Calculer"):
    resultats = calculer_frais_deplacement(
        prix_carburant, distance_km, quote_part,
        hebergement, restauration, nb_repas,
        parking_par_jour, nb_jours
    )
    st.write("### Résultats :")
    for cle, valeur in resultats.items():
        st.write(f"{cle} : {valeur:.2f} €")
