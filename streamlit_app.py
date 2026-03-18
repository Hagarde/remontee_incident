import streamlit as st
import os
from datetime import datetime
import time
import utils        
import generate_pdf 

# =============================================================================
# CONFIGURATION GÉNÉRALE
# =============================================================================
st.set_page_config(page_title="Portail acte de malveillances", page_icon="🛡️", layout="wide")
MEDIA_ROOT = "./data/media"
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Initialisation de l'étape courante dans la mémoire de Streamlit
if 'etape' not in st.session_state:
    st.session_state.etape = 1

# Fonctions pour naviguer entre les étapes
def etape_suivante():
    st.session_state.etape += 1

def etape_precedente():
    st.session_state.etape -= 1

# =============================================================================
# UI PRINCIPALE
# =============================================================================
st.title("🛡️ Detectout")
st.markdown("---")

# --- BARRE DE PROGRESSION VISUELLE ---
etapes_noms = ["1. Localisation", "2. Qualification", "3. Détails techniques", "4. Juridique & Validation"]
st.progress(st.session_state.etape / 4)
st.markdown(f"**Étape {st.session_state.etape} sur 4 : {etapes_noms[st.session_state.etape - 1]}**")
st.markdown("---")

# =============================================================================
# ÉTAPE 1 : LOCALISATION
# =============================================================================
if st.session_state.etape == 1:
    st.subheader("1. Date et Localisation")
    entite = utils.SELECT_ENTITE()
    loc_data = utils.afficher_selecteurs_localisation()
    is_urgent = st.checkbox("⚠️ Événement de grande ampleur")
    st.warning('"Événement de grande ampleur" inclut uniquement les événements malveillants majeurs, caractérisés par leurs conséquences physiques, matérielles ou médiatiques, ou par une sensibilité particulière. Nous limitons ainsi essentiellement aux **actes de sabotages**, de **terrorisme**, d**acte sous contrainte** ainsi que les **vols d’une forte ampleur**.')
    
    # On sauvegarde temporairement dans la session pour ne pas perdre l'info
    if loc_data:
        st.session_state.loc_data = loc_data
    if 'is_urgent' not in st.session_state:
        st.session_state.is_urgent = False
    st.session_state.is_urgent = is_urgent

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        # On empêche de passer à la suite si la localisation n'est pas remplie
        if st.button("Suivant ➡️", use_container_width=True, disabled=loc_data is None):
            etape_suivante()

# =============================================================================
# ÉTAPE 2 : QUALIFICATION
# =============================================================================
elif st.session_state.etape == 2:
    st.subheader("2. Qualification des faits")
    st.info("💡 Vous pouvez ajouter plusieurs actes pour un même acte de malveillance.")
    
    liste_faits_saisis = utils.gerer_saisie_actes()
    st.session_state.liste_faits_saisis = liste_faits_saisis

    st.markdown("---")
    
    # --- CONDITION DE VALIDATION ÉTAPE 2 ---
    # L'étape est valide si au moins un acte complet a été saisi
    etape2_valide = len(liste_faits_saisis) > 0

    if not etape2_valide:
        st.warning("⚠️ Veuillez renseigner au moins une typologie, un mode opératoire et une cible pour continuer.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.button("⬅️ Précédent", on_click=etape_precedente, use_container_width=True)
    with col3:
        # Le bouton est grisé (disabled) tant que etape2_valide est False
        st.button("Suivant ➡️", on_click=etape_suivante, use_container_width=True, disabled=not etape2_valide)

# =============================================================================
# ÉTAPE 3 : DÉTAILS TECHNIQUES
# =============================================================================
elif st.session_state.etape == 3:
    st.subheader("3. Détails techniques")
    c1, c2 = st.columns(2)

    with c1:
        st.session_state.cout_estime = utils.INPUT_COUT_ESTIME()
        st.session_state.reparation_provisioire = utils.SELECT_BOX_MESURE_PROVISOIRE()
        st.session_state.secteur_cible = utils.SELECT_CIBLE()
    with c2:
        st.session_state.obstacles_selectionnes = utils.SELECT_OBSTACLE() if hasattr(utils, 'SELECT_OBSTACLE') else []
        st.session_state.siv_present = utils.SELECT_BOX_SIV_DECLENCHE()

    st.session_state.description = utils.INPUT_DESCRIPTION()
    
    st.warning("""**Avertissement relatif à la protection des données personnelles**
Pour rappel, dans les zones de commentaire libre, toute donnée permettant d’identifier des tiers doit être également exclue. De plus, vous devez impérativement rédiger de façon objective et jamais excessive ou insultante. Toute donnée considérée comme sensible (origine raciale ou ethnique, opinions politiques, philosophiques ou religieuses, appartenance syndicale, données relatives à la santé ou à la vie sexuelle) doit être exclue.""")

    st.markdown("---")

    # --- CONDITION DE VALIDATION ÉTAPE 3 ---
    # Par exemple : on rend la Description OBLIGATOIRE (pas juste des espaces vides)
    etape3_valide = len(st.session_state.description.strip()) > 0
    
    if not etape3_valide:
        st.warning("⚠️ La description détaillée de l'acte est obligatoire.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.button("⬅️ Précédent", on_click=etape_precedente, use_container_width=True)
    with col3:
        # Le bouton est grisé (disabled) tant que etape3_valide est False
        st.button("Suivant ➡️", on_click=etape_suivante, use_container_width=True, disabled=not etape3_valide)

# =============================================================================
# ÉTAPE 4 : JURIDIQUE & ACTIONS FINALES
# =============================================================================
elif st.session_state.etape == 4:
    st.subheader("4. Aspects juridiques & Pièces jointes")
    col_jur_1, col_jur_2 = st.columns(2)
    with col_jur_1:
        statut_plainte = utils.INPUT_PLAINTE()
    with col_jur_2:
        st.markdown("**Ajouter une pièce jointe (plainte, pré-plainte, photos, devis, constat de huisssier, ...)**")
        uploaded_file = st.file_uploader("Format : PDF, JPG, PNG", type=['pdf', 'png', 'jpg', 'jpeg'])
    
    st.markdown("---")
    
    # Préparation des données finales
    final_data = st.session_state.loc_data.copy()
    obs_final = st.session_state.obstacles_selectionnes if st.session_state.obstacles_selectionnes else ["Aucun"]

    final_data.update({
        "liste_faits": st.session_state.liste_faits_saisis,
        "obstacles_list": obs_final, 
        "cout": st.session_state.cout_estime,
        "mesure_provisoire": st.session_state.reparation_provisioire,
        "siv": st.session_state.siv_present,
        "plainte": statut_plainte,
        "desc": st.session_state.description,
        "urgent": st.session_state.is_urgent,
        "chemin_fichier": None 
    })
    
    if st.session_state.liste_faits_saisis:
        final_data["acte"] = st.session_state.liste_faits_saisis[0].get('acte')
        final_data["cat_cible"] = st.session_state.liste_faits_saisis[0].get('categorie')
        final_data["cible_spec"] = st.session_state.liste_faits_saisis[0].get('objet')
        final_data["obstacle"] = ", ".join(obs_final)
    else:
        final_data["acte"] = "Incident"
        final_data["obstacle"] = "Aucun"

    # BOUTONS D'ACTION FINALE
    st.subheader("🚀 Validation finale")
    
    col_prev, col_pdf, col_db = st.columns([1, 1, 1])

    with col_prev:
        st.button("⬅️ Précédent", on_click=etape_precedente, use_container_width=True)

    with col_pdf:
        if st.button("📄 Générer PDF", use_container_width=True):
            try:
                pdf_bytes = generate_pdf.generer_pdf(final_data)
                nom_pdf = f"Rapport_{final_data.get('date', datetime.now()).strftime('%Y-%m-%d')}_Securite.pdf"
                st.download_button("📥 Télécharger PDF", data=pdf_bytes, file_name=nom_pdf, mime="application/pdf", use_container_width=True)
                st.success("PDF prêt !")
            except Exception as e:
                st.error(f"Erreur PDF : {e}")

    with col_db:
        if st.button("💾 Enregistrer en Base", type="primary", use_container_width=True):
            with st.spinner("Enregistrement..."):
                if uploaded_file:
                    path = time.sleep(1)#sauvegarder_fichier_local(uploaded_file)
                    #if path: final_data["chemin_fichier"] = path
                
                result = time.sleep(1) # db_manager.sauvegarder_incident_postgres(final_data)
                
                # if result and result.get("success"):
                st.success(f"✅ Enregistré avec succès ! (ID: 67)")
                st.balloons()
                    # Optionnel : réinitialiser le formulaire après un succès
                    # st.session_state.clear()
                #else:
                #    st.error("❌ Erreur SQL")
                #    st.error(result.get("error") if result else "Pas de réponse")
                #    if result and result.get("trace"):
                #        with st.expander("Détails"): st.code(result["trace"])