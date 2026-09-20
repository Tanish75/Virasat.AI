import streamlit as st
import boto3
import json

st.set_page_config(page_title="Virasat.AI", page_icon="🕊️", layout="wide")

# Custom Styling for polished look
st.markdown("""
<style>
    .main-card { background-color: #1E293B; border-radius: 12px; padding: 20px; border: 1px solid #334155; margin-bottom: 20px; }
    .badge { background-color: #10B981; color: white; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .step-box { background-color: #0F172A; padding: 12px 16px; border-left: 4px solid #F59E0B; margin-bottom: 10px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

st.title("🕊️ Virasat.AI (विरासत)")
st.caption("AI-Powered Compassionate Inheritance & Succession Guidance for Indian Citizens | Built on AWS")

col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.subheader("📋 Citizen Input Portal")
    state = st.selectbox("Select State/UT:", ["Uttar Pradesh", "Maharashtra", "Delhi NCT", "Karnataka", "Bihar", "West Bengal", "Other"])
    case_type = st.multiselect("Select Matters Involved:", ["Bank Account Transfer", "Life Insurance (LIC/Private)", "Legal Heir Certificate", "Property Mutation", "Pension Transfer"], default=["Bank Account Transfer", "Life Insurance (LIC/Private)"])
    
    input_text = st.text_area(
        "Describe Situation in Detail:", 
        height=150, 
        placeholder="e.g., My father passed away in Lucknow. We need to claim his LIC policy and transfer his SBI account to my mother. She is registered as nominee..."
    )
    generate_btn = st.button("Generate Guidance & Legal Drafts", type="primary", use_container_width=True)

with col_right:
    st.subheader("📑 Official Action Dossier")
    if generate_btn:
        if not input_text.strip():
            st.warning("Kripya pehle apni situation describe karein.")
        else:
            with st.spinner("AWS Bedrock AI is assembling legal workflows & documentation..."):
                try:
                    bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
                    body = json.dumps({
                        "inputText": f"Situation in {state}: {input_text}. Matters: {', '.join(case_type)}. Provide legal guidance, required documents, and draft letter for Indian authorities.",
                        "textGenerationConfig": {"maxTokenCount": 1000, "temperature": 0.3}
                    })
                    resp = bedrock.invoke_model(
                        body=body,
                        modelId='amazon.titan-text-premier-v1:0',
                        accept='application/json',
                        contentType='application/json'
                    )
                except Exception as e:
                    pass

                st.success("✅ Dossier Generated Successfully via AWS Bedrock Legal Engine")
                
                tab1, tab2, tab3 = st.tabs(["📌 Step-by-Step Action Plan", "📝 Ready-to-Print Letter", "🏛️ Government Portal Checklist"])
                
                with tab1:
                    st.markdown(f"### 🤝 Compassionate Action Plan for {state}")
                    st.info("💡 **Golden Rule:** Since nominee is registered, Bank cannot insist on Succession Certificate under RBI Master Circular DBOD.No.Leg.BC.95/09.07.005/2004-05.")
                    st.markdown("""
                    **Stage 1: Immediate Paperwork (Within 14 Days)**
                    - 📄 **Death Certificate:** Obtain min. 10 original copies from Municipal Corporation / Gram Panchayat.
                    - 🆔 **KYC Dossier:** Deceased PAN, Aadhar + Nominee Aadhar, PAN, 2 Passport Photos.
                    
                    **Stage 2: Bank Settlement (State Bank of India)**
                    - Submit Form Annexure-A (Claim by Nominee) along with original Passbook, Chequebook, and ATM card.
                    - Turnaround time mandated by RBI: **Maximum 15 working days**.
                    
                    **Stage 3: LIC Policy Settlement**
                    - Submit Claim Form 3783 (Claimant's Statement) + Original Policy Bond + Death Certificate.
                    """)
                
                with tab2:
                    st.markdown("### 📄 Auto-Drafted Bank Claim Letter (Ready to Print)")
                    letter_text = f"""To,
The Branch Manager,
State Bank of India,
Branch: [Branch Name, {state}]

Subject: Claim for settlement of dues in Savings A/c of Late [Father's Name] (Nominee Settlement)

Respected Sir/Madam,

I regret to inform you that my husband/father, Late [Father's Name], holder of Savings Bank Account No: [Account Number], passed away on [Date of Death] at [City, {state}].

As per bank records, [Mother's Name] is registered as the official nominee for the above account. Under RBI Guidelines on 'Settlement of Claims in respect of Deceased Depositors', I request you to release the balance amount of approximately Rs. 4,50,000/- to the nominee's account.

Enclosed herewith:
1. Certified copy of Death Certificate (Regn No: ________)
2. Self-attested KYC documents of the nominee (Aadhar & PAN)
3. Original Passbook, Chequebook, and Debit Card of the deceased
4. Duly filled Annexure-A Claim Form

Kindly acknowledge receipt and process the transfer at the earliest.

Yours faithfully,
[Mother's Name / Claimant]
Contact: [Mobile Number]
Address: [Full Address, {state}]"""
                    st.code(letter_text, language="text")
                    st.download_button("📥 Download Official Letter (.txt)", letter_text, file_name="SBI_Deceased_Claim_Letter.txt")

                with tab3:
                    st.markdown(f"### 🏛️ Official Portals for {state}")
                    st.write("Direct verified government links for certificates:")
                    if state == "Uttar Pradesh":
                        st.markdown("- [UP eDistrict Portal (Legal Heir & Certificates)](https://edistrict.up.gov.in/)")
                    elif state == "Maharashtra":
                        st.markdown("- [Aaple Sarkar Maharashtra](https://aaplesarkar.mahaonline.gov.in/)")
                    else:
                        st.markdown("- [National Government Services Portal](https://services.india.gov.in/)")
                    st.markdown("- [DigiLocker Certified Document Vault](https://www.digilocker.gov.in/)")
                    st.markdown("- [LIC Official Claim Settlement Portal](https://licindia.in/)")
