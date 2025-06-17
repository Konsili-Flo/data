import streamlit as st
from PIL import Image, ImageOps
import base64
import io
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Relevé Visite Datacenter", layout="wide")
st.title("📂 Relevé technique & chiffrage - Démantèlement Datacenter")

# Initialisation de la session
if "salles" not in st.session_state:
    st.session_state.salles = []

# Ajout d'une nouvelle salle
st.sidebar.header("Ajouter une salle")
nouvelle_salle = st.sidebar.text_input("Nom de la salle")
if st.sidebar.button("Ajouter la salle") and nouvelle_salle:
    st.session_state.salles.append({"nom": nouvelle_salle, "donnees": {}})

# Pour chaque salle ajoutée
for index, salle in enumerate(st.session_state.salles):
    with st.expander(f"Salle {salle['nom']}", expanded=False):
        donnees = salle["donnees"]

        st.subheader("Informations générales")
        donnees["surface"] = st.number_input(f"Surface (m²) - {salle['nom']}", min_value=0.0, step=1.0, key=f"surf_{index}")
        donnees["observations"] = st.text_area(f"Observations - {salle['nom']}", key=f"obs_{index}")

        st.subheader("🗄️ Baies")
        donnees["baies_nombre"] = st.number_input(f"Nombre de baies - {salle['nom']}", min_value=0, key=f"baies_{index}")
        donnees["baies_type"] = st.text_input(f"Type de baies - {salle['nom']}", key=f"baies_type_{index}")
        donnees["baies_nom"] = st.text_area(f"Noms / Identifiants des baies - {salle['nom']}", key=f"baies_nom_{index}")
        donnees["baies_commentaire"] = st.text_area(f"Commentaire baies - {salle['nom']}", key=f"baies_com_{index}")

        st.subheader("🗄️ Câbles et fibres")
        donnees["cables_nombre"] = st.number_input(f"Nombre de câbles - {salle['nom']}", min_value=0, key=f"cables_{index}")
        donnees["cables_type"] = st.text_input(f"Types de câbles - {salle['nom']}", key=f"cables_type_{index}")
        donnees["fibres_nombre"] = st.number_input(f"Nombre de fibres - {salle['nom']}", min_value=0, key=f"fibres_{index}")
        donnees["repart_fibre"] = st.number_input(f"Nombre de répartiteurs fibre - {salle['nom']}", min_value=0, key=f"rfibre_{index}")
        donnees["repart_cuivre"] = st.number_input(f"Nombre de répartiteurs cuivre - {salle['nom']}", min_value=0, key=f"rcuivre_{index}")
        donnees["cables_commentaire"] = st.text_area(f"Commentaire câbles et fibres - {salle['nom']}", key=f"cables_com_{index}")

        st.subheader("🧯 Coupe-feux")
        donnees["coupe_feu_nombre"] = st.number_input(f"Nombre de coupe-feux - {salle['nom']}", min_value=0, key=f"cf_{index}")
        donnees["coupe_feu_type"] = st.text_input(f"Type de coupe-feux - {salle['nom']}", key=f"cf_type_{index}")
        donnees["cf_commentaire"] = st.text_area(f"Commentaire coupe-feux - {salle['nom']}", key=f"cf_com_{index}")

        st.subheader("⚡ Consignations électriques")
        donnees["consignation_nombre"] = st.number_input(f"Nombre de consignations électriques - {salle['nom']}", min_value=0, key=f"conso_{index}")
        donnees["consignation_commentaire"] = st.text_area(f"Commentaire consignations - {salle['nom']}", key=f"conso_com_{index}")

        st.subheader("🗄️ Passages de câbles")
        donnees["passages_hauteur"] = st.number_input(f"Passages en hauteur - {salle['nom']}", min_value=0, key=f"ph_{index}")
        donnees["passages_sol"] = st.number_input(f"Passages sous plancher - {salle['nom']}", min_value=0, key=f"ps_{index}")
        donnees["passages_commentaire"] = st.text_area(f"Commentaire passages de câbles - {salle['nom']}", key=f"pc_com_{index}")

        st.subheader("🔋 Disques durs & équipements")
        donnees["disques_nombre"] = st.number_input(f"Disques durs à détruire - {salle['nom']}", min_value=0, key=f"disques_{index}")
        donnees["repartiteurs"] = st.number_input(f"Nombre de répartiteurs - {salle['nom']}", min_value=0, key=f"rep_{index}")
        donnees["equip_extraction"] = st.text_area(f"Détail des extractions d'équipements - {salle['nom']}", key=f"extract_{index}")
        donnees["equip_retrait"] = st.number_input(f"Équipements à retirer des baies - {salle['nom']}", min_value=0, key=f"retire_{index}")
        donnees["equip_commentaire"] = st.text_area(f"Commentaire équipements - {salle['nom']}", key=f"equip_com_{index}")

        st.subheader("🚒 Alarmes incendie")
        donnees["alarmes_inhiber"] = st.text_area(f"Détail des alarmes à inhiber - {salle['nom']}", key=f"alarme_{index}")
        donnees["alarme_commentaire"] = st.text_area(f"Commentaire alarmes - {salle['nom']}", key=f"alarme_com_{index}")

        st.subheader("📷 Ajout de photos")
        photos = st.file_uploader("Uploader des photos (plusieurs possibles)", accept_multiple_files=True, type=["png", "jpg", "jpeg"], key=f"photos_{index}")
        donnees["photos"] = []
        for photo in photos:
            image = Image.open(photo)
            buffered = io.BytesIO()
            image = ImageOps.exif_transpose(image)
            image.save(buffered, format="JPEG")
            donnees["photos"].append(base64.b64encode(buffered.getvalue()).decode("utf-8"))
            st.image(image, caption=photo.name, width=200)

# Récapitulatif
st.markdown("---")
st.header("📊 Récapitulatif des données saisies")
if st.button("Afficher le récapitulatif"):
    for salle in st.session_state.salles:
        st.subheader(f"Salle {salle['nom']}")
        for k, v in salle["donnees"].items():
            if k != "photos":
                st.write(f"**{k}**: {v}")
            else:
                st.write("Photos: ")
                for p in v:
                    img = Image.open(io.BytesIO(base64.b64decode(p)))
                    st.image(img, width=100)

# Export PDF
st.markdown("---")
st.header("📤 Export PDF")
if st.button("Générer le PDF"):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", size=10)

    salles = st.session_state.salles if st.session_state.salles else [{"nom": "Sans nom", "donnees": {}}]

    for salle in salles:
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 16)
            titre_salle = salle['nom'].strip().encode('latin-1', 'ignore').decode('latin-1')
    pdf.cell(0, 10, f"Salle : {titre_salle}", ln=True)

            pdf.set_font("Helvetica", 'B', 14)
        sections = [
            ("Informations générales", ["surface", "observations"]),
            ("Baies", ["baies_nombre", "baies_type", "baies_nom", "baies_commentaire"]),
            ("Câbles et fibres", ["cables_nombre", "cables_type", "fibres_nombre", "repart_fibre", "repart_cuivre", "cables_commentaire"]),
            ("Coupe-feux", ["coupe_feu_nombre", "coupe_feu_type", "cf_commentaire"]),
            ("Consignations électriques", ["consignation_nombre", "consignation_commentaire"]),
            ("Passages de câbles", ["passages_hauteur", "passages_sol", "passages_commentaire"]),
            ("Disques durs & équipements", ["disques_nombre", "repartiteurs", "equip_extraction", "equip_retrait", "equip_commentaire"]),
            ("Alarmes incendie", ["alarmes_inhiber", "alarme_commentaire"])
        ]

        for section_title, fields in sections:
            pdf.set_font("Helvetica", 'B', 11)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(0, 8, section_title, ln=True, fill=True)
            pdf.set_font("Helvetica", '', 9)
            for field in fields:
                value = salle["donnees"].get(field, "")
                if value:
                    try:
                        texte = f"- {field.replace('_', ' ').capitalize()} : {str(value).strip()}"
                        texte = texte.encode('latin-1', 'ignore').decode('latin-1')
                        pdf.set_font("Helvetica", '', 9)
                        pdf.cell(0, 5, texte, ln=True)
                        pdf.set_font("Helvetica", '', 11)
                    except:
                        pdf.set_font("Helvetica", '', 9)
                        pdf.cell(0, 5, f"- {field.replace('_', ' ').capitalize()} : Erreur d'affichage", ln=True)
                        pdf.set_font("Helvetica", '', 11)

        photos = salle["donnees"].get("photos", [])
        if photos:
            pdf.set_font("Helvetica", 'B', 12)
            pdf.cell(0, 10, "Photos de la salle", ln=True)
            pdf.set_font("Helvetica", '', 11)
            for i, img_b64 in enumerate(photos):
                pdf.add_page()
                y_offset = 40
                try:
                    img_data = base64.b64decode(img_b64)
                    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                    tmp_file.write(img_data)
                    tmp_file.close()

                    image = Image.open(tmp_file.name)
                    image = ImageOps.exif_transpose(image)
                    rotated_path = tmp_file.name + "_rotated.jpg"
                    image.save(rotated_path, format="JPEG")

                    pdf.image(rotated_path, x=35, y=y_offset, w=pdf.w - 70)
                    pdf.set_y(y_offset + 60)
                    pdf.set_font("Helvetica", '', 9)
                    pdf.cell(0, 6, f"Photo {i + 1}", ln=True)
                    
                    # Retiré pour éviter double incrémentation
                    if y_offset > 240:
                        pdf.add_page()
                        y_offset = 20

                    os.remove(rotated_path)
                    os.remove(tmp_file.name)
                except Exception as e:
                    pdf.multi_cell(190, 6, f"Erreur chargement image : {str(e)}")

    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp_pdf.name)

    with open(tmp_pdf.name, "rb") as f:
        st.download_button("📥 Télécharger le PDF", f, file_name="releve_datacenter.pdf")
    # os.remove(tmp_pdf.name)  # Suppression différée pour éviter le verrouillage sous Windows
