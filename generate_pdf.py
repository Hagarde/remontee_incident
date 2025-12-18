# fichier: pdf_generator.py
from fpdf import FPDF

class RapportPDF(FPDF):
    def header(self):
        # En-tête avec logo ou titre
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Rapport Incident ', border=False, ln=1, align='C')
        self.ln(5)

    def footer(self):
        # Pied de page avec numérotation
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generer_pdf(data):
    """
    Génère le PDF à partir d'un dictionnaire de données.
    Retourne les bytes du fichier PDF.
    """
    pdf = RapportPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Fonction interne pour nettoyer le texte (gestion des accents sans police externe)
    def clean_text(text):
        if text is None:
            return ""
        # Convertit en string, encode en latin-1 pour FPDF standard, remplace les erreurs
        return str(text).encode('latin-1', 'replace').decode('latin-1')

    # --- TITRE SECTEUR ---
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(200, 220, 255) # Fond bleu clair
    pdf.cell(0, 10, txt=clean_text(f"Secteur : {data.get('secteur', '')}"), ln=True, fill=True)
    pdf.ln(5)

    # --- SECTION 1 : LOCALISATION ---
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "1. Localisation", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 6, clean_text(f"Détails : {data.get('loc_data', '')}"))
    pdf.ln(3)

    # --- SECTION 2 : QUALIFICATION ---
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "2. Qualification de l'incident", ln=True)
    pdf.set_font("Arial", '', 10)
    
    # Création d'un petit tableau manuel
    pdf.cell(50, 6, "Type d'acte :", border=0)
    pdf.cell(0, 6, clean_text(data.get('acte', '')), ln=True)
    
    pdf.cell(50, 6, "Catégorie Cible :", border=0)
    pdf.cell(0, 6, clean_text(data.get('cat_cible', '')), ln=True)
    
    pdf.cell(50, 6, "Cible Spécifique :", border=0)
    pdf.cell(0, 6, clean_text(data.get('cible_spec', '')), ln=True)
    
    pdf.cell(50, 6, "Localisation site :", border=0)
    pdf.cell(0, 6, clean_text(data.get('loc_site', '')), ln=True)
    pdf.ln(3)

    # --- SECTION 3 : TECHNIQUE ---
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "3. Détails Techniques", ln=True)
    pdf.set_font("Arial", '', 10)
    
    pdf.cell(50, 6, "Coût estimé :", border=0)
    pdf.cell(0, 6, clean_text(f"{data.get('cout', '0')} €"), ln=True)
    
    pdf.cell(50, 6, "Obstacle franchi :", border=0)
    pdf.cell(0, 6, clean_text(data.get('obstacle', '')), ln=True)
    
    pdf.ln(2)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 6, clean_text(f"Description : {data.get('desc', '')}"))
    pdf.ln(3)

    # --- SECTION 4 : JURIDIQUE ---
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "4. Juridique", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(50, 6, "Plainte :", border=0)
    pdf.cell(0, 6, clean_text(data.get('plainte', '')), ln=True)

    # Retourner le binaire (compatible FPDF2)
    return bytes(pdf.output(dest='S'))