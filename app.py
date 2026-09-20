import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

def generate_bulletproof_pdf(title, text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading2'], fontSize=12, leading=16, fontName='Helvetica-Bold', textColor='#000000', spaceAfter=14)
    body_style = ParagraphStyle('DocBody', parent=styles['Normal'], fontSize=11, leading=16, fontName='Helvetica', textColor='#111827', spaceAfter=8)
    
    elements = []
    elements.append(Paragraph(f"<b>SUBJECT: {title.upper()}</b>", title_style))
    elements.append(Spacer(1, 10))
    for line in text.split("\n"):
        clean = line.strip()
        if clean:
            clean = clean.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            elements.append(Paragraph(clean, body_style))
        else:
            elements.append(Spacer(1, 8))
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

st.set_page_config(page_title="Virasat.AI", page_icon="⚖️", layout="wide")

st.title("🕊️ Virasat.AI")
st.caption("Succession & Statutory Rights Guidance Assistant")
st.divider()

col_left, col_right = st.columns([1, 1], gap="large")

STATE_DATA = {
    "Uttar Pradesh": {"portal": "UP eDistrict Portal", "url": "https://edistrict.up.gov.in/", "cert": "Varisan Praman Patra"},
    "Maharashtra": {"portal": "Aaple Sarkar Portal", "url": "https://aaplesarkar.mahaonline.gov.in/", "cert": "Legal Heir Certificate"},
    "Delhi NCT": {"portal": "e-District Delhi", "url": "https://edistrict.delhigovt.nic.in/", "cert": "Surviving Member Certificate"}
}

with col_left:
    state = st.selectbox("State / Territory", list(STATE_DATA.keys()))
    case_type = st.multiselect("Services Needed", ["Bank Account Transfer", "Life Insurance (LIC/Private)", "Legal Heir Certificate"], default=["Bank Account Transfer"])
    input_text = st.text_area("Case Details", height=130)
    generate_btn = st.button("Generate Documents", type="primary", use_container_width=True)

with col_right:
    if generate_btn and input_text:
        tab1, tab2 = st.tabs(["Action Checklist", "Edit & Download PDF"])
        with tab1:
            st.info("Under RBI Circular DBOD.No.Leg.BC.95, bank must settle nominee claims within 15 days.")
        with tab2:
            letter = f"To,\nThe Branch Manager,\nBank Branch, {state}\n\nSubject: Claim Settlement\n\nRespected Sir,\nKindly settle account dues for Late [Name] under RBI guidelines.\n\nYours faithfully,\n[Nominee Name]"
            edited = st.text_area("Review Application", value=letter, height=200)
            pdf = generate_bulletproof_pdf("Claim Settlement", edited)
            st.download_button("📥 Download Official PDF", data=pdf, file_name=f"Claim_{state}.pdf", mime="application/pdf", type="primary")
