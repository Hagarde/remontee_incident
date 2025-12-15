# streamlit_app.py
import streamlit as st
import utils

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
with col_interactif_1:
    acte_type = utils.SELECT_BOX_TYPE_ACTE()
with col_interactif_2:
    cat_cible = utils.SELECT_BOX_CAT_CIBLE()    
with col_interactif_3:
    cible_specifique = utils.SELECT_OBJET_SPECIFIQUE(cat_cible)
with col_interactif_4 :
    localisation_sur_site = utils.SELECT_BOX_LOCALISATION_SUR_SITE()


st.subheader("3. Détails techniques")

c1, c2 = st.columns(2)
with c1:
    reparation_provisioire = utils.SELECT_BOX_MESURE_PROVISOIRE()
with c2 : 
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