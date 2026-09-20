import streamlit as st
import boto3
import json
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

st.set_page_config(page_title="Virasat.AI", page_icon="🕊️", layout="wide")

st.title("🕊️ Virasat.AI (विरासत)")
st.caption("Dynamic AI-Powered Inheritance & Succession Assistant for Bharat | Built on AWS")

col_left, col_right = st.columns([1, 1], gap="medium")

STATE_DATA = {
    "Uttar Pradesh": {"portal": "UP eDistrict Portal", "url": "https://edistrict.up.gov.in/", "cert": "Varisan Praman Patra", "dept": "Revenue Dept, UP"},
    "Maharashtra": {"portal": "Aaple Sarkar Portal", "url": "https://aaplesarkar.mahaonline.gov.in/", "cert": "Legal Heir Certificate", "dept": "Revenue Dept, Maharashtra"},
    "Delhi NCT": {"portal": "e-District Delhi", "url": "https://edistrict.delhigovt.nic.in/", "cert": "Surviving Member Certificate", "dept": "Revenue Dept, Delhi"},
    "Karnataka": {"portal": "Seva Sindhu", "url": "https://sevasindhu.karnataka.gov.in/", "cert": "Family Tree Certificate", "dept": "Revenue Admin, Karnataka"},
    "Bihar": {"portal": "RTPS Bihar", "url": "https://serviceonline.bihar.gov.in/", "cert": "Vanshavali", "dept": "Revenue, Bihar"},
    "West Bengal": {"portal": "e-District WB", "url": "https://edistrict.wb.gov.in/", "cert": "Legal Heir Certificate", "dept": "Land Revenue, WB"},
    "Other": {"portal": "National Services Portal", "url": "https://services.india.gov.in/", "cert": "Legal Heir Certificate", "dept": "Citizen Services"}
}

with col_left:
    st.subheader("📋 Citizen Input Portal")
    state = st.selectbox("Select State/UT:", list(STATE_DATA.keys()))
    case_type = st.multiselect("Select Matters Involved:", ["Bank Account Transfer", "Life Insurance (LIC/Private)", "Legal Heir Certificate", "Property Mutation", "Pension Transfer"], default=["Bank Account Transfer", "Life Insurance (LIC/Private)"])
    input_text = st.text_area("Describe Situation in Detail:", height=140, placeholder=f"e.g., Father passed away in {state}...")
    generate_btn = st.button("Generate Guidance & Legal Drafts", type="primary", use_container_width=True)

with col_right:
    st.subheader("📑 Tailored Action Dossier")
    if generate_btn:
        if not input_text.strip() or not case_type:
            st.warning("Kripya details bharein.")
        else:
            state_info = STATE_DATA[state]
            st.success(f"✅ Dossier Configured for {state}")
            tab1, tab2, tab3 = st.tabs(["📌 Action Plan", "📝 Download Letter (PDF)", "🏛️ Government Portals"])
            
            with tab1:
                st.info("Under RBI Circular DBOD.No.Leg.BC.95, bank must settle nominee claims within 15 days without succession certificate.")
            
            with tab2:
                letter_subject = f"Claim for settlement of dues in A/c of Late [Deceased Name]"
                letter_text = f"To,\nThe Branch Manager,\nState Bank of India, {state}\n\nSubject: {letter_subject}\n\nRespected Sir/Madam,\nMy father Late [Deceased Name] passed away. I am the nominee for A/c [Account Number]. Kindly settle the dues under RBI guidelines.\n\nYours faithfully,\n[Nominee Name]"
                
                edited = st.text_area("Edit Application Letter:", value=letter_text, height=220)
                pdf_bytes = generate_bulletproof_pdf(letter_subject, edited)
                st.download_button("📥 Download Application (PDF)", data=pdf_bytes, file_name=f"Claim_{state}.pdf", mime="application/pdf", type="primary")

            with tab3:
                st.write(f"Portal: {state_info['portal']}")
