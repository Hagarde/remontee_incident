from fpdf import FPDF
from datetime import datetime
import os

class RapportPDF(FPDF):
    def header(self):
        # Gestion du logo
        if os.path.exists("./data/logoRTE.jpg"):
            self.image('./data/logoRTE.jpg', 10, 8, 33)
        
        self.set_font('Arial', 'B', 15)
        self.cell(40)
        self.cell(0, 10, clean_text("RAPPORT D'INCIDENT DE SÉCURITÉ"), 0, 1, 'C')
        
        self.set_font('Arial', 'I', 10)
        self.set_text_color(100, 100, 100)
        self.cell(40)
        self.cell(0, 10, f'Généré le {datetime.now().strftime("%d/%m/%Y à %H:%M")}', 0, 1, 'C')
        
        self.ln(10)
        self.set_draw_color(0, 51, 102)
        self.line(10, 35, 200, 35)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'RTE - Document Confidentiel - Page {self.page_no()}/{{nb}}', 0, 0, 'C')

def clean_text(text):
    if text is None: return "Non renseigné"
    text = str(text).replace('€', 'Euros').replace('’', "'").replace('…', '...')
    try:
        return text.encode('latin-1', 'replace').decode('latin-1')
    except:
        return str(text)

def generer_pdf(data):
    pdf = RapportPDF('P', 'mm', 'A4')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    if data.get('urgent', False):
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(255, 0, 0)
        pdf.set_draw_color(255, 0, 0)
        pdf.cell(0, 10, "!!! INCIDENT SIGNALÉ URGENT !!!", 1, 1, 'C')
        pdf.set_text_color(0)
        pdf.set_draw_color(0)
        pdf.ln(5)

    # ==========================================================
    # LE CORRECTIF : FONCTION D'AFFICHAGE ROBUSTE
    # ==========================================================
    def print_line_robuste(label, value, color_val=(0, 0, 0)):
        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(0)
        
        valeur_propre = clean_text(value)
        if str(valeur_propre).strip() == "":
            valeur_propre = "Non renseigné"
            
        col_width = 65 # Élargi à 65 pour les grands mots
        start_y = pdf.get_y()
        start_x = pdf.get_x() # On mémorise où est le stylo
        
        # 1. Écriture du libellé
        pdf.cell(col_width, 6, clean_text(label), 0, 0)
        
        # 2. On change la marge et on remet le curseur au bon niveau
        pdf.set_left_margin(start_x + col_width)
        pdf.set_y(start_y) 
        
        # 3. Écriture de la valeur
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(*color_val)
        pdf.multi_cell(0, 6, valeur_propre)
        
        # 4. LA SOLUTION : On restaure la marge ET la position du stylo
        pdf.set_left_margin(start_x)
        pdf.set_x(start_x) 
        pdf.set_text_color(0)

    # ==========================================================
    # 1. CONTEXTE ET LOCALISATION
    # ==========================================================
    pdf.set_fill_color(245, 245, 245)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, clean_text("1. CONTEXTE ET LOCALISATION"), 0, 1, 'L', True)
    pdf.ln(2)
    
    date_str = data['date'].strftime('%d/%m/%Y') if isinstance(data.get('date'), datetime) else str(data.get('date', 'N/A'))
    print_line_robuste("Date du constat :", date_str)
    
    if data.get('urgent'):
        print_line_robuste("Niveau d'urgence :", "URGENT - Intervention requise", color_val=(255, 0, 0))
    else:
        print_line_robuste("Niveau d'urgence :", "Standard", color_val=(0, 100, 0))
    
    pdf.ln(2)

    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(255, 255, 255)
    pdf.set_fill_color(100, 100, 100)
    pdf.cell(0, 7, clean_text("  Détails Géographiques"), 0, 1, 'L', True)
    pdf.set_text_color(0)
    
    if data.get('type') == 'site':
        print_line_robuste("Code Ouvrage (ID) :", data.get('id_ref'))
        print_line_robuste("Nom du Site :", data.get('label_complet', data.get('id_ref')))
        print_line_robuste("Commune :", f"{data.get('commune')} ({data.get('cp')})")
        print_line_robuste("Région / Dép :", f"{data.get('region')} / {data.get('departement')}")
        print_line_robuste("GMR / GDP :", f"{data.get('gmr')} / {data.get('gdp')}")
    else:
        print_line_robuste("Commune :", f"{data.get('commune')} ({data.get('cp')})")
        print_line_robuste("Département :", data.get('departement'))
        print_line_robuste("Région :", data.get('region'))
    
    pdf.ln(5)

    # ==========================================================
    # 2. DÉTAIL DES FAITS
    # ==========================================================
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 51, 102)
    pdf.set_fill_color(245, 245, 245)
    pdf.cell(0, 10, clean_text("2. DÉTAIL DES FAITS CONSTATÉS"), 0, 1, 'L', True)
    pdf.ln(2)
    
    liste_faits = data.get('liste_faits', [])
    if not liste_faits and data.get('acte'):
        liste_faits = [{"acte": data.get('acte'), "categorie": data.get('cat_cible', ''), "objet": data.get('cible_spec', '')}]

    for i, fait in enumerate(liste_faits):
        acte = str(fait.get('acte', ''))
        cat = str(fait.get('categorie', ''))
        obj = str(fait.get('objet', ''))
        
        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(120, 130, 140) 
        pdf.cell(0, 7, clean_text(f"  Acte n°{i+1}"), 0, 1, 'L', True)
        
        pdf.set_text_color(0)
        print_line_robuste("Typologie :", acte)
        print_line_robuste("Mode Opératoire :", cat)
        print_line_robuste("Cible / Objet :", obj)
        pdf.ln(3)

    pdf.ln(2)

    # ==========================================================
    # 3. CONSTATATIONS TECHNIQUES
    # ==========================================================
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 51, 102)
    pdf.set_fill_color(245, 245, 245)
    pdf.cell(0, 10, clean_text("3. CONSTATATIONS TECHNIQUES"), 0, 1, 'L', True)
    pdf.ln(2)
    
    raw_obstacles = data.get('obstacles_list', [])
    if isinstance(raw_obstacles, list) and len(raw_obstacles) > 0:
        obstacle_str = ", ".join(raw_obstacles)
    else:
        obstacle_str = str(data.get('obstacle', 'Aucun'))
    
    print_line_robuste("Obstacles franchis :", obstacle_str)
    print_line_robuste("Système SIV déclenché :", str(data.get('siv', 'Non')))
    print_line_robuste("Mesures conservatoires :", data.get('mesure_provisoire', 'Aucune'))
    
    pdf.ln(3)
    pdf.set_font("Arial", 'B', 10)
    pdf.write(6, clean_text("Description détaillée des faits :\n"))
    pdf.set_font("Arial", '', 10)
    pdf.set_fill_color(255, 255, 240) 
    desc = data.get('desc') if data.get('desc') else "Aucune description complémentaire saisie."
    pdf.multi_cell(0, 6, clean_text(desc), 1, 'L', True)
    pdf.ln(5)

    # ==========================================================
    # 4. IMPACT ET SUIVI
    # ==========================================================
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 51, 102)
    pdf.set_fill_color(245, 245, 245)
    pdf.cell(0, 10, clean_text("4. IMPACT ET SUIVI"), 0, 1, 'L', True)
    pdf.ln(2)
    
    cout_val = str(data.get('cout', '0'))
    print_line_robuste("Préjudice estimé :", f"{cout_val} k Euros")
    
    plainte_val = clean_text(data.get('plainte', 'Non renseigné'))
    color_plainte = (0, 0, 200) if "Déposée" in plainte_val or "prévu" in plainte_val.lower() else (0, 0, 0)
    print_line_robuste("Statut de la plainte :", plainte_val, color_val=color_plainte)

    # ==========================================================
    # 5. BONUS : INTÉGRATION DE LA PIÈCE JOINTE
    # ==========================================================
    chemin = data.get('chemin_fichier')
    if chemin and os.path.exists(chemin):
        ext = chemin.split('.')[-1].lower()
        if ext in ['jpg', 'jpeg', 'png']:
            # On ajoute une nouvelle page pour l'image si elle existe
            pdf.add_page()
            pdf.set_font("Arial", 'B', 12)
            pdf.set_text_color(0, 51, 102)
            pdf.set_fill_color(245, 245, 245)
            pdf.cell(0, 10, clean_text("5. PIÈCE JOINTE (PHOTO)"), 0, 1, 'L', True)
            pdf.ln(5)
            try:
                # w=180 permet d'adapter l'image à la largeur de la feuille A4 (210 - marges)
                pdf.image(chemin, x=15, w=180)
            except Exception as e:
                pdf.set_font("Arial", 'I', 10)
                pdf.set_text_color(200, 0, 0)
                pdf.cell(0, 6, clean_text(f"Impossible d'afficher l'image : {e}"), 0, 1)
        else:
            # Si c'est un PDF ou autre, on affiche juste le nom
            pdf.ln(5)
            pdf.set_font("Arial", 'I', 9)
            pdf.set_text_color(100, 100, 100)
            nom_fichier = os.path.basename(chemin)
            pdf.cell(0, 6, clean_text(f"[Document PDF joint séparément : {nom_fichier}]"), 0, 1)

    return bytes(pdf.output(dest='S'))