import os
import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="AI Revenue Agent System", layout="wide")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("AI Revenue Agent System")
st.write("Upload lead data, select a company, and let 3 AI-style agents analyse it.")

uploaded_file = st.file_uploader("Upload your leads file", type=["csv", "xlsx"])

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

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    selected_index = st.selectbox(
        "Select a lead/company row to analyse:",
        df.index
    )

    selected_row = df.loc[selected_index]

    lead_input = f"""
Company Name: {selected_row.get("Company Name", "")}
Industry: {selected_row.get("Industry", "")}
Company Size: {selected_row.get("Company Size", "")}
Current Problem: {selected_row.get("Current Problem", "")}
Possible Need: {selected_row.get("Possible Need", "")}
"""

    st.subheader("Selected Lead")
    st.text(lead_input)

    if st.button("Run AI Agents"):
        with st.spinner("Lead Analyst is working..."):
            lead_analysis = run_agent(
                "You are a B2B Lead Analyst. Analyse lead quality, pain points, buying signals, and objections.",
                f"""
Analyse this business lead:

{lead_input}

Provide:
- Lead quality score out of 10
- Main pain points
- Buying signals
- Possible objections
"""
            )

        with st.spinner("Sales Strategist is working..."):
            sales_strategy = run_agent(
                "You are a Sales Strategist. Create practical B2B sales strategies from lead analysis.",
                f"""
Using this lead analysis:

{lead_analysis}

Create:
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

        st.subheader("Lead Analysis")
        st.write(lead_analysis)

        st.subheader("Sales Strategy")
        st.write(sales_strategy)

        st.subheader("Outreach Message")
        st.write(outreach_message)

else:
    st.info("Upload a CSV or Excel file to begin.")
