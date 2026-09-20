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

st.set_page_config(page_title="Virasat.AI", page_icon="⚖️", layout="centered")

st.markdown("""
<style>
    .block-container { max-width: 820px !important; padding-top: 2.5rem !important; padding-bottom: 3rem !important; }
    .app-header { border-bottom: 1px solid rgba(128, 128, 128, 0.2); padding-bottom: 16px; margin-bottom: 24px; }
    .app-title { font-size: 28px; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
    .app-subtitle { font-size: 14px; opacity: 0.75; margin-top: 4px; }
    .checklist-item { padding: 12px 16px; border-left: 3px solid #3B82F6; background-color: rgba(59, 130, 246, 0.06); border-radius: 0 8px 8px 0; margin-bottom: 10px; font-size: 14px; line-height: 1.5; }
    .rbi-item { border-left-color: #10B981; background-color: rgba(16, 185, 129, 0.06); }
    .stButton>button, .stDownloadButton>button { border-radius: 8px !important; font-weight: 600 !important; height: 46px !important; }
</style>
""", unsafe_allow_html=True)

STATE_DATA = {
    "Uttar Pradesh": {"portal": "UP eDistrict Portal", "url": "https://edistrict.up.gov.in/", "cert": "Varisan Praman Patra (वारिसान प्रमाण पत्र)", "dept": "Revenue Department, Govt of Uttar Pradesh"},
    "Maharashtra": {"portal": "Aaple Sarkar Portal", "url": "https://aaplesarkar.mahaonline.gov.in/", "cert": "Legal Heir Certificate / Varis Dakhla", "dept": "Revenue & Forest Department, Maharashtra"},
    "Delhi NCT": {"portal": "e-District Delhi", "url": "https://edistrict.delhigovt.nic.in/", "cert": "Surviving Member Certificate (SMC)", "dept": "Revenue Department, Govt of NCT of Delhi"},
    "Karnataka": {"portal": "Seva Sindhu / Nadakacheri", "url": "https://sevasindhu.karnataka.gov.in/", "cert": "Family Tree & Survivorship Certificate", "dept": "Karnataka Revenue Administration"},
    "Bihar": {"portal": "RTPS Bihar (ServicePlus)", "url": "https://serviceonline.bihar.gov.in/", "cert": "Vanshavali (वंशावली) via Circle Officer", "dept": "Revenue and Land Reforms, Bihar"},
    "West Bengal": {"portal": "Banglarbhumi & e-District WB", "url": "https://edistrict.wb.gov.in/", "cert": "Legal Heir Certificate via SDO/BDO", "dept": "Judicial & Land Revenue, West Bengal"},
    "Other": {"portal": "National Government Services Portal", "url": "https://services.india.gov.in/", "cert": "Legal Heir Certificate via Local SDM", "dept": "Central & State Citizen Services"}
}

st.markdown("""
<div class="app-header">
    <div class="app-title">⚖️ Virasat.AI</div>
    <div class="app-subtitle">Inheritance & Legal Succession Document Generator for Indian Citizens</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    state = st.selectbox("State / Union Territory", list(STATE_DATA.keys()))
with col2:
    case_type = st.multiselect("Services Needed", ["Bank Account Transfer", "Life Insurance (LIC/Private)", "Legal Heir Certificate", "Property Mutation", "Pension Transfer"], default=["Bank Account Transfer", "Life Insurance (LIC/Private)"])

input_text = st.text_area("Describe Situation", height=110, placeholder=f"e.g., Father passed away in {state}. Need to transfer SBI savings account to mother (registered nominee) and claim LIC policy...")
generate_btn = st.button("Generate Documents & Roadmap", type="primary", use_container_width=True)

if generate_btn:
    if not input_text.strip() or not case_type:
        st.warning("Please provide situation details and select required services.")
    else:
        state_info = STATE_DATA[state]
        st.write("---")
        tab1, tab2, tab3 = st.tabs(["1. Action Roadmap", "2. Legal Application Letter", "3. Official State Links"])
        
        with tab1:
            st.markdown("#### Legal Procedure & Statutory Rights")
            if "Bank Account Transfer" in case_type:
                st.markdown("""
                <div class="checklist-item rbi-item">
                    <b>🏦 Bank Settlement (RBI Circular DBOD.No.Leg.BC.95):</b><br>
                    • If nominee exists, bank <b>cannot demand</b> court succession certificate.<br>
                    • Mandated turnaround time: <b>15 working days</b>.<br>
                    • Documents: Passbook, Chequebook, ATM card, Death Certificate, Nominee KYC.
                </div>
                """, unsafe_allow_html=True)
            if "Life Insurance (LIC/Private)" in case_type:
                st.markdown("""
                <div class="checklist-item">
                    <b>🛡️ Life Insurance Claim (LIC / Private):</b><br>
                    • Submit Form 3783 (Claimant Statement) + Original Policy Bond + Death Certificate.<br>
                    • Attach cancelled cheque with nominee's name for direct bank credit.
                </div>
                """, unsafe_allow_html=True)
            if "Legal Heir Certificate" in case_type or "Property Mutation" in case_type:
                st.markdown(f"""
                <div class="checklist-item">
                    <b>🏛️ {state} Succession Law:</b><br>
                    • Required Certificate: <b>{state_info['cert']}</b><br>
                    • Issuing Authority: {state_info['dept']}<br>
                    • Portal: {state_info['portal']}
                </div>
                """, unsafe_allow_html=True)

        with tab2:
            st.markdown("#### Pre-Drafted Formal Application")
            st.caption("You can edit the text directly in the box below before downloading your official PDF.")
            if "Property Mutation" in case_type:
                letter_subject = f"Application for Property Mutation (Virasat) in {state}"
                letter_text = f"""To,\nThe Tehsildar / Revenue Officer,\nDepartment of Revenue, {state}\n\nSubject: {letter_subject}\n\nRespected Sir/Madam,\nI am writing to formally report the demise of my father, Late [Father's Name], resident of [Address, {state}], who passed away on [Date of Death]. He was the registered owner of property bearing Khata/Plot No: [Plot/Khata Details].\n\nAs legal heirs, we request you to initiate property mutation in revenue records in our favor.\n\nEnclosed Documents:\n1. Certified Death Certificate\n2. Family Tree / {state_info['cert']}\n3. Property Tax Receipt / Title Deed\n4. Self-Declaration Affidavit\n\nYours faithfully,\n[Applicant Name]\nContact: [Mobile Number]"""
                file_name = f"Property_Mutation_{state}.pdf"
            elif "Life Insurance (LIC/Private)" in case_type and "Bank Account Transfer" not in case_type:
                letter_subject = f"Death Claim Intimation for Policy No [Policy Number] in {state}"
                letter_text = f"""To,\nThe Branch Manager,\nLife Insurance Corporation of India (LIC),\nBranch: [Branch Name, {state}]\n\nSubject: {letter_subject}\n\nRespected Sir/Madam,\nI regret to inform you of the demise of the policyholder, Late [Deceased Name], who held Policy No: [Policy Number] at your branch.\n\nAs the registered nominee, I request you to process the death claim.\n\nEnclosed Documents:\n1. Certified Death Certificate\n2. Original Policy Bond\n3. Claimant's Statement (Form 3783)\n4. Cancelled cheque & KYC documents\n\nYours faithfully,\n[Nominee Name]\nContact: [Mobile Number]"""
                file_name = f"Insurance_Claim_{state}.pdf"
            else:
                letter_subject = f"Claim for settlement of dues in A/c of Late [Deceased Name] under RBI Guidelines"
                letter_text = f"""To,\nThe Branch Manager,\n[Bank Name, e.g. State Bank of India],\nBranch: [Branch Name, {state}]\n\nSubject: {letter_subject}\n\nRespected Sir/Madam,\nI regret to inform you that my father, Late [Deceased Name], passed away on [Date of Death]. He held Account No: [Account Number] at your branch.\n\nI am the registered nominee. As per RBI Master Circular on 'Settlement of Claims in respect of Deceased Depositors', I request settlement of the balance without requiring a court succession certificate.\n\nEnclosed Documents:\n1. Certified Death Certificate\n2. Self-attested KYC (Aadhar & PAN) of Nominee\n3. Original Passbook & Chequebook\n4. Duly filled Deceased Claim Form (Annexure-A)\n\nYours faithfully,\n[Nominee Name]\nAddress: [City, {state}]"""
                file_name = f"Bank_Claim_{state}.pdf"

            edited_text = st.text_area("Edit Application Letter Below:", value=letter_text, height=260)
            pdf_data = generate_bulletproof_pdf(letter_subject, edited_text)
            st.download_button(label="📥 Download Application (PDF)", data=pdf_data, file_name=file_name, mime="application/pdf", type="primary", use_container_width=True)

        with tab3:
            st.markdown(f"#### Verified Government Links ({state})")
            st.markdown(f"- **State Portal:** [{state_info['portal']}]({state_info['url']})")
            st.markdown(f"- **Mandatory Certificate:** `{state_info['cert']}`")
            st.markdown(f"- **Issuing Office:** `{state_info['dept']}`")
            st.markdown("- **DigiLocker India:** [https://www.digilocker.gov.in/](https://www.digilocker.gov.in/)")
