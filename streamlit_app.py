# streamlit_app.py
import streamlit as st
import utils
import generate_pdf

st.set_page_config(page_title="Portail Incidents", page_icon="🛡️", layout="wide")

st.title("🛡️ Detectout")

nature_incident = st.selectbox(
    "Quel secteur d'acitivité de RTE  ?",
    [
        "Industriel",
        "Autre (Chantier, Personnel RTE, Site Tertiaire)"
    ], index=None, placeholder="Choisissez une option"
)

st.markdown("---")

st.subheader("1. Date et localisation ")

loc_data = utils.afficher_selecteurs_localisation(referentiel="GMR")

st.subheader("2. Qualification de l'incident")

col_interactif_1, col_interactif_2 , col_interactif_3, col_interactif_4= st.columns(4)
acte_type_input = ""
cat_cible_input = ""
cible_specifique_input = ""
localisation_sur_site_input = ""
with col_interactif_1:
    acte_type = utils.SELECT_BOX_TYPE_ACTE()
    if acte_type == "Autre" : acte_type_input = st.text_input("Entrez la catégorie pertinente absente du menu déroulant", key="type_acte")
with col_interactif_2:
    cat_cible = utils.SELECT_BOX_CAT_CIBLE()    
    if cat_cible == "Autre" : cat_cible_input = st.text_input("Entrez la catégorie pertinente absente du menu déroulant", key="cat_cible")
with col_interactif_3:
    cible_specifique = utils.SELECT_OBJET_SPECIFIQUE(cat_cible)
    if cible_specifique == "Autre" : cible_specifique_input = st.text_input("Entrez la catégorie pertinente absente du menu déroulant", key="cible_specifique")
with col_interactif_4 :
    localisation_sur_site = utils.SELECT_BOX_LOCALISATION_SUR_SITE()
    if localisation_sur_site == "Autre" : localisation_sur_site_input = st.text_input("Entrez la catégorie pertinente absente du menu déroulant", key="localisation_sur_site")

st.subheader("3. Détails techniques")

c1, c2 = st.columns(2)
with c1:
    reparation_provisioire = utils.SELECT_BOX_MESURE_PROVISOIRE()
    cout_estime = utils.INPUT_COUT_ESTIME()
with c2 : 
    obstacle_franchies = utils.SELECT_BOX_OBSTACLE_FRANCHI()
    degat_obstacle = utils.SELECT_BOX_DEGAT_OBSTACLE()
    siv_present = utils.SELECT_BOX_SIV_DECLENCHE()
description = utils.INPUT_DESCRIPTION()

st.subheader("4. Aspects juridiques")

colo1, colo2 = st.columns(2)
with colo1 : 
    statut_plainte = utils.INPUT_PLAINTE ()
with colo2 : 
    plainte_file = utils.UPLOAD_PLAINTE()
with st.form("form_intrusion"):
    submit = st.form_submit_button("Envoyer Rapport 🚨")
pdf_bytes = generate_pdf.generer_pdf({
        "secteur": nature_incident,
        "loc_data": loc_data["ville"] if loc_data["mode"] == "Ville" else loc_data["gmr"],
        "acte": acte_type_input if acte_type == "Autre" else acte_type,
        "cat_cible": cat_cible if cat_cible != "Autre" else cat_cible_input,
        "cible_spec": cible_specifique if acte_type != "Autre" else cible_specifique_input,
        "loc_site": localisation_sur_site if acte_type != "Autre" else localisation_sur_site_input,
        "cout": cout_estime,
        "obstacle": obstacle_franchies,
        "desc": description,
        "plainte": statut_plainte
})
st.download_button(
        label="🚨 Générer et Télécharger le Rapport",
        data=pdf_bytes,
        file_name="rapport_incident.pdf",
        mime="application/pdf"
)