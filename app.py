import streamlit as st
import pandas as pd
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Revenue Agent System", layout="wide")

st.title("AI Revenue Agent System")
st.write("Upload lead data, select a company, and let 3 AI agents analyse it.")

uploaded_file = st.file_uploader("Upload your leads file", type=["csv", "xlsx"])

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
        with st.spinner("AI agents are working..."):

            lead_analyst = Agent(
                role="Lead Analyst",
                goal="Analyse the business lead and identify sales potential",
                backstory="You are an expert B2B lead analyst who understands pain points, buying signals, objections, and lead quality.",
                verbose=True,
            )

            sales_strategist = Agent(
                role="Sales Strategist",
                goal="Create a practical sales strategy based on the lead analysis",
                backstory="You are a senior sales strategist who creates clear commercial strategies for winning B2B clients.",
                verbose=True,
            )

            outreach_writer = Agent(
                role="Outreach Writer",
                goal="Write a personalised outreach message based on the sales strategy",
                backstory="You write professional, human, concise B2B outreach messages that do not sound robotic.",
                verbose=True,
            )

            task_1 = Task(
                description=f"""
                Analyse this business lead:

                {lead_input}

                Provide:
                - Lead quality score out of 10
                - Main pain points
                - Buying signals
                - Possible objections
                """,
                expected_output="A structured lead analysis with score, pain points, buying signals, and objections.",
                agent=lead_analyst,
            )

            task_2 = Task(
                description="""
                Using the lead analysis from Task 1, create a sales strategy.

                Provide:
                - Best sales angle
                - Value proposition
                - Suggested first approach
                - Next best action
                """,
                expected_output="A practical B2B sales strategy based on the lead analysis.",
                agent=sales_strategist,
            )

            task_3 = Task(
                description="""
                Using the lead analysis and sales strategy, write a personalised outreach message.

                Requirements:
                - Professional
                - Human
                - Short
                - Not pushy
                - Suitable for LinkedIn or email
                """,
                expected_output="A polished outreach message ready to send.",
                agent=outreach_writer,
            )

            crew = Crew(
                agents=[lead_analyst, sales_strategist, outreach_writer],
                tasks=[task_1, task_2, task_3],
                verbose=True,
            )

            result = crew.kickoff()

        st.subheader("Lead Analysis")
        st.write(result.tasks_output[0].raw)

        st.subheader("Sales Strategy")
        st.write(result.tasks_output[1].raw)

        st.subheader("Outreach Message")
        st.write(result.tasks_output[2].raw)

else:
    st.info("Upload a CSV or Excel file to begin.")