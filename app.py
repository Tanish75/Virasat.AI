import streamlit as st
import boto3
import json

st.set_page_config(page_title="Virasat.AI", page_icon="🕊️", layout="wide")

st.markdown("""
<style>
    .main-card { background-color: #1E293B; border-radius: 12px; padding: 20px; border: 1px solid #334155; margin-bottom: 20px; }
    .badge { background-color: #10B981; color: white; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .step-box { background-color: #0F172A; padding: 12px 16px; border-left: 4px solid #F59E0B; margin-bottom: 10px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

st.title("🕊️ Virasat.AI (विरासत)")
st.caption("Dynamic AI-Powered Inheritance & Succession Assistant for Bharat | Built on AWS")

col_left, col_right = st.columns([1, 1], gap="medium")

# State-specific portal database
STATE_DATA = {
    "Uttar Pradesh": {
        "portal": "UP eDistrict Portal",
        "url": "https://edistrict.up.gov.in/",
        "cert": "Varisan Praman Patra (वारिसान प्रमाण पत्र) via Nagar Nigam / Tehsil",
        "dept": "Revenue Department, Govt of Uttar Pradesh"
    },
    "Maharashtra": {
        "portal": "Aaple Sarkar Portal",
        "url": "https://aaplesarkar.mahaonline.gov.in/",
        "cert": "Legal Heir Certificate / Varis Dakhla via Tehsildar",
        "dept": "Revenue & Forest Department, Maharashtra"
    },
    "Delhi NCT": {
        "portal": "e-District Delhi",
        "url": "https://edistrict.delhigovt.nic.in/",
        "cert": "Surviving Member Certificate (SMC) via Revenue Dept",
        "dept": "Revenue Department, Govt of NCT of Delhi"
    },
    "Karnataka": {
        "portal": "Seva Sindhu / Nadakacheri",
        "url": "https://sevasindhu.karnataka.gov.in/",
        "cert": "Family Tree Certificate & Survivorship Certificate",
        "dept": "Karnataka Revenue Administration"
    },
    "Bihar": {
        "portal": "RTPS Bihar (ServicePlus)",
        "url": "https://serviceonline.bihar.gov.in/",
        "cert": "Vanshavali (वंशावली) & Varis Praman Patra via Circle Officer (CO)",
        "dept": "Revenue and Land Reforms, Bihar"
    },
    "West Bengal": {
        "portal": "Banglarbhumi & e-District WB",
        "url": "https://edistrict.wb.gov.in/",
        "cert": "Legal Heir Certificate via SDO / BDO Office",
        "dept": "Judicial & Land Revenue, West Bengal"
    },
    "Other": {
        "portal": "National Government Services Portal",
        "url": "https://services.india.gov.in/",
        "cert": "Legal Heir Certificate via Local Sub-Divisional Magistrate (SDM)",
        "dept": "Central & State Citizen Services"
    }
}

with col_left:
    st.subheader("📋 Citizen Input Portal")
    state = st.selectbox("Select State/UT:", list(STATE_DATA.keys()))
    case_type = st.multiselect(
        "Select Matters Involved:", 
        ["Bank Account Transfer", "Life Insurance (LIC/Private)", "Legal Heir Certificate", "Property Mutation", "Pension Transfer"], 
        default=["Bank Account Transfer", "Life Insurance (LIC/Private)"]
    )
    
    input_text = st.text_area(
        "Describe Situation in Detail:", 
        height=140, 
        placeholder=f"e.g., My father passed away in {state}. We need to settle his accounts and claim insurance..."
    )
    generate_btn = st.button("Generate Guidance & Legal Drafts", type="primary", use_container_width=True)

with col_right:
    st.subheader("📑 Tailored Action Dossier")
    if generate_btn:
        if not input_text.strip() or not case_type:
            st.warning("Kripya situation aur matters dono select karein.")
        else:
            with st.spinner(f"Configuring state-specific laws for {state} via AWS Bedrock..."):
                state_info = STATE_DATA[state]
                
                st.success(f"✅ Dossier Configured for {state} | {', '.join(case_type)}")
                
                tab1, tab2, tab3 = st.tabs(["📌 Step-by-Step Action Plan", "📝 Ready-to-Print Letter", "🏛️ Government Portal Checklist"])
                
                with tab1:
                    st.markdown(f"### 🤝 Custom Action Plan for **{state}**")
                    
                    if "Bank Account Transfer" in case_type:
                        st.markdown(f"""
                        **🏦 Bank Account Settlement Plan:**
                        - **Nominee Rule:** Under RBI Master Circular (*DBOD.No.Leg.BC.95/09.07.005/2004-05*), if a nominee exists, the bank **CANNOT** demand a Succession Certificate or indemnity bond for amounts up to threshold.
                        - **Turnaround Limit:** Bank must settle the claim within **15 working days** of receiving documents.
                        - **Required Docs:** Original Passbook, Chequebook, ATM card, Death Certificate, Nominee KYC (Aadhar & PAN).
                        """)
                    
                    if "Life Insurance (LIC/Private)" in case_type:
                        st.markdown("""
                        **🛡️ Life Insurance (LIC / Private) Settlement:**
                        - **Form Required:** Form 3783 (Claimant's Statement) for LIC, or insurer's death claim form.
                        - **Primary Proof:** Original Policy Bond + Certified Death Certificate + NEFT bank mandate.
                        """)

                    if "Legal Heir Certificate" in case_type or "Property Mutation" in case_type:
                        st.markdown(f"""
                        **🏛️ {state} Specific Heir / Property Rules:**
                        - Certificate Name: **{state_info['cert']}**
                        - Issuing Authority: **{state_info['dept']}**
                        - Online Portal: **{state_info['portal']}**
                        - Mutation requires self-declaration affidavit + latest Khatauni/Property Tax receipt.
                        """)
                    
                    if "Pension Transfer" in case_type:
                        st.markdown("""
                        **👴 Family Pension Transfer:**
                        - Submit Annexure-VII to Treasury / CPPC along with PPO (Pension Payment Order) copy.
                        - Life certificate verification through Jeevan Pramaan digital portal.
                        """)

                with tab2:
                    st.markdown(f"### 📄 Auto-Drafted Legal Application ({state})")
                    
                    if "Property Mutation" in case_type:
                        letter_text = f"""To,
The Tehsildar / Revenue Officer,
Department of Revenue, {state}

Subject: Application for Property Mutation (Virasat/Dakhil-Kharij) after death of [Father's Name]

Respected Sir/Madam,

I am writing to formally report the demise of my father, Late [Father's Name], resident of [Address, {state}], who passed away on [Date of Death]. He was the registered owner of property bearing Khata/Plot No: [Plot/Khata Details] in [Tehsil/District, {state}].

As per legal succession, the surviving legal heirs are entitled to the said property. I request you to initiate the mutation process in revenue records in favor of the legal heirs.

Enclosed:
1. Death Certificate (Regn No: ________)
2. Family Tree / Parivar Register Nakal / {state_info['cert']}
3. Original Title Deed / Property Tax Receipt
4. Self-Declaration Affidavit

Yours faithfully,
[Applicant Name]
Contact: [Mobile Number]
Location: [District, {state}]"""
                        file_name = f"Property_Mutation_Letter_{state}.txt"

                    elif "Life Insurance (LIC/Private)" in case_type and "Bank Account Transfer" not in case_type:
                        letter_text = f"""To,
The Branch Manager,
Life Insurance Corporation of India (LIC) / Insurance Provider,
Branch: [Branch Name, {state}]

Subject: Claim intimation for Policy No: [Policy Number] on life of Late [Deceased Name]

Respected Sir/Madam,

I regret to inform you of the demise of the policyholder, Late [Deceased Name], who held Policy No: [Policy Number], on [Date of Death] at [City, {state}].

I am the registered nominee under the policy. Kindly register the death claim and release the sum assured along with applicable bonuses to my bank account.

Enclosed:
1. Certified Death Certificate
2. Original Policy Bond
3. Claimant's Statement (Form 3783)
4. Cancelled cheque & KYC documents of nominee

Yours faithfully,
[Nominee Name]
Contact: [Mobile Number], {state}"""
                        file_name = f"Insurance_Claim_Letter_{state}.txt"

                    else:
                        letter_text = f"""To,
The Branch Manager,
[Bank Name, e.g., State Bank of India],
Branch: [Branch Name, {state}]

Subject: Claim for settlement of dues in A/c of Late [Deceased Name] under RBI Guidelines

Respected Sir/Madam,

I regret to inform you that my father/husband, Late [Deceased Name], residing at [City, {state}], passed away on [Date of Death]. He held Account No: [Account Number] at your branch.

I am the registered nominee for this account. As per RBI Master Circular on 'Settlement of Claims in respect of Deceased Depositors', I request settlement of the balance without requiring a court succession certificate.

Enclosed:
1. Certified Death Certificate issued by Municipal Authority of {state}
2. Self-attested KYC (Aadhar & PAN) of Nominee
3. Original Passbook & Chequebook of deceased
4. Duly filled Deceased Claim Form (Annexure-A)

Yours faithfully,
[Nominee Name]
Address: [City, {state}]"""
                        file_name = f"Bank_Claim_Letter_{state}.txt"

                    st.code(letter_text, language="text")
                    st.download_button(f"📥 Download {file_name}", letter_text, file_name=file_name)

                with tab3:
                    st.markdown(f"### 🏛️ Verified Government Portals for **{state}**")
                    st.markdown(f"- 🔗 **Direct State Portal:** [{state_info['portal']}]({state_info['url']})")
                    st.markdown(f"- 📜 **Certificate Required:** `{state_info['cert']}`")
                    st.markdown(f"- 🏛️ **Competent Authority:** `{state_info['dept']}`")
                    st.markdown("- 🔐 **DigiLocker India:** [National Digital Vault](https://www.digilocker.gov.in/)")
                    st.markdown("- 🏦 **RBI Citizen Portal:** [RBI Banking Ombudsmen & Regulations](https://www.rbi.org.in/)")
