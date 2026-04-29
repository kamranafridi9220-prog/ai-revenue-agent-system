import os
from datetime import datetime

import pandas as pd
import streamlit as st
from openai import OpenAI


st.set_page_config(
    page_title="AI Revenue Agent System",
    page_icon="🚀",
    layout="wide"
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def run_agent(role, prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content


st.title("🚀 AI Revenue Agent System")
st.write(
    "Upload lead data, select a company, and let 3 AI agents generate lead analysis, "
    "sales strategy, and outreach messaging."
)

st.divider()

with st.sidebar:
    st.header("How it works")
    st.write("1. Upload a CSV or Excel file")
    st.write("2. Select a company / lead")
    st.write("3. Run AI agents")
    st.write("4. Review analysis, strategy, and outreach")
    st.divider()
    st.caption("Built with Python, Streamlit, OpenAI API, and Pandas.")


uploaded_file = st.file_uploader(
    "Upload your leads file",
    type=["csv", "xlsx"]
)

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully.")

else:
    try:
        df = pd.read_excel("leads_sample.xlsx")
        st.info("No file uploaded. Using sample dataset from the repository.")
    except Exception:
        df = None
        st.warning("Upload a CSV or Excel file to begin.")


if df is not None:
    st.subheader("Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    required_columns = [
        "Company Name",
        "Industry",
        "Company Size",
        "Current Problem",
        "Possible Need"
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(
            "Your dataset is missing these required columns: "
            + ", ".join(missing_columns)
        )
        st.stop()

    company_options = df["Company Name"].astype(str).tolist()

    selected_company = st.selectbox(
        "Select a lead/company to analyse:",
        company_options
    )

    selected_row = df[df["Company Name"].astype(str) == selected_company].iloc[0]

    lead_input = f"""
Company Name: {selected_row.get("Company Name", "")}
Industry: {selected_row.get("Industry", "")}
Company Size: {selected_row.get("Company Size", "")}
Current Problem: {selected_row.get("Current Problem", "")}
Possible Need: {selected_row.get("Possible Need", "")}
"""

    st.subheader("Selected Lead")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Company", selected_row.get("Company Name", "N/A"))

    with col2:
        st.metric("Industry", selected_row.get("Industry", "N/A"))

    with col3:
        st.metric("Company Size", selected_row.get("Company Size", "N/A"))

    st.write("*Current Problem:*", selected_row.get("Current Problem", ""))
    st.write("*Possible Need:*", selected_row.get("Possible Need", ""))

    st.divider()

    if st.button("Run AI Agents", type="primary"):
        with st.spinner("Lead Analyst is working..."):
            lead_analysis = run_agent(
                "You are a B2B Lead Analyst. Analyse lead quality, pain points, buying signals, and objections.",
                f"""
Analyse this business lead:

{lead_input}

Provide a structured output with:
- Lead quality score out of 10
- Main pain points
- Buying signals
- Possible objections
- Short summary
"""
            )

        with st.spinner("Sales Strategist is working..."):
            sales_strategy = run_agent(
                "You are a Sales Strategist. Create practical B2B sales strategies from lead analysis.",
                f"""
Using this lead analysis:

{lead_analysis}

Create a practical sales strategy with:
- Best sales angle
- Value proposition
- Suggested first approach
- Next best action
- Priority level
- Confidence score
"""
            )

        with st.spinner("Outreach Writer is working..."):
            outreach_message = run_agent(
                "You are a B2B Outreach Writer. Write professional, human, concise outreach messages.",
                f"""
Using this lead analysis and sales strategy:

Lead Analysis:
{lead_analysis}

Sales Strategy:
{sales_strategy}

Write a short, professional outreach email or LinkedIn message.
"""
            )

        st.success("AI agents completed the analysis.")

        tab1, tab2, tab3 = st.tabs(
            ["Lead Analysis", "Sales Strategy", "Outreach Message"]
        )

        with tab1:
            st.markdown(lead_analysis)

        with tab2:
            st.markdown(sales_strategy)

        with tab3:
            st.markdown(outreach_message)

        full_report = f"""
AI Revenue Agent System Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

SELECTED LEAD
{lead_input}

LEAD ANALYSIS
{lead_analysis}

SALES STRATEGY
{sales_strategy}

OUTREACH MESSAGE
{outreach_message}
"""

        st.download_button(
            label="Download Full Report",
            data=full_report,
            file_name=f"{selected_company.replace(' ', '_')}_ai_revenue_report.txt",
            mime="text/plain"
        )
