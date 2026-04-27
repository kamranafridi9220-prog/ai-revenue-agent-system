from crewai import Agent, Task, Crew
from dotenv import load_dotenv

load_dotenv()

lead_analyst = Agent(
    role="Lead Analyst",
    goal="Analyse the business lead and identify sales potential",
    backstory="You are an expert B2B lead analyst who understands buying signals, pain points, and lead quality.",
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

lead_description = """
Company Type: UK facilities management company
Company Size: Small to medium business
Current Problem: Uses spreadsheets to track leads, customer follow-ups, and revenue.
Possible Need: Better pipeline visibility, faster follow-ups, and improved client retention.
"""

task_1 = Task(
    description=f"""
    Analyse this business lead:

    {lead_description}

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

print("\n\nFINAL MULTI-AGENT OUTPUT:\n")
print(result)