
# Import required modules
import streamlit as st
import os
import json
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import uuid
from datetime import datetime

# Warning control
import warnings
warnings.filterwarnings('ignore')

# Set OpenAI API key (ensure you set this in your environment or replace with your key)
# For VS Code, set the environment variable in your terminal or .env file
# Example: export OPENAI_API_KEY='your-api-key'
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or "Your_openai_api_key_here"
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

# Custom tool for scraping Finkraft website
finkraft_scrape_tool = ScrapeWebsiteTool(
    website_url="https://finkraft.ai/en"
)

# Load or initialize session data
SESSION_FILE = "chat_sessions.json"
def load_session(session_id):
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            sessions = json.load(f)
            return sessions.get(session_id, {"history": [], "context": {}})
    return {"history": [], "context": {}}

def save_session(session_id, session_data):
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            sessions = json.load(f)
    else:
        sessions = {}
    sessions[session_id] = session_data
    with open(SESSION_FILE, 'w') as f:
        json.dump(sessions, f, indent=4)

# Define the 5 Agents for the Sales Chatbot Multi-Agent System

# 1. Instant Clarity Agent
instant_clarity_agent = Agent(
    role="Instant Clarity Agent",
    goal="Provide lightning-fast, accurate answers to straightforward FAQs and common objections to build trust",
    backstory=(
        "You work at Finkraft (https://finkraft.ai/en) and handle simple queries instantly. "
        "You escalate complex queries to other agents and keep responses friendly and engaging."
    ),
    tools=[finkraft_scrape_tool],
    allow_delegation=True,
    verbose=True
)

# 2. Trust & Source Agent
trust_source_agent = Agent(
    role="Trust & Source Agent",
    goal="Provide detailed, sourced answers with examples and citations from credible documents",
    backstory=(
        "You work at Finkraft (https://finkraft.ai/en) and retrieve data from official sources or CRM. "
        "You provide citations and practical examples, refusing to guess on uncertain queries."
    ),
    tools=[finkraft_scrape_tool, SerperDevTool()],
    allow_delegation=False,
    verbose=True
)

# 3. Engagement & Nudge Agent
engagement_nudge_agent = Agent(
    role="Engagement & Nudge Agent",
    goal="Engage users with multi-turn conversations and ask relevant follow-up questions",
    backstory=(
        "You work at Finkraft (https://finkraft.ai/en) and detect user interest or hesitation. "
        "You ask follow-ups like 'Which feature interests you?' to keep the conversation flowing."
    ),
    allow_delegation=True,
    verbose=True
)

# 4. Lead Capture Agent
lead_capture_agent = Agent(
    role="Lead Capture Agent",
    goal="Collect user details conversationally when interest is shown",
    backstory=(
        "You work at Finkraft (https://finkraft.ai/en) and capture leads naturally (e.g., 'What’s your email?'). "
        "You avoid forms and integrate details into the conversation."
    ),
    allow_delegation=False,
    verbose=True
)

# 5. Message Simulation & Review Agent
message_simulation_review_agent = Agent(
    role="Message Simulation & Review Agent",
    goal="Simulate and refine multi-turn conversations, ensuring accuracy and engagement",
    backstory=(
        "You work at Finkraft (https://finkraft.ai/en) and simulate responses for scenarios like feature inquiries. "
        "You refine tone, add contact details, and ensure a complete dialogue."
    ),
    allow_delegation=True,
    verbose=True
)

# Define Tasks for the Agents

# Task 1: Handle initial FAQ or objection
initial_clarity_task = Task(
    description=(
        "The user from {company} has asked: {inquiry}. "
        "Provide a quick, friendly answer or escalate to Trust & Source Agent for detailed responses."
    ),
    expected_output=(
        "A brief response or escalation note based on the inquiry's complexity."
    ),
    tools=[finkraft_scrape_tool],
    agent=instant_clarity_agent
)

# Task 2: Verify and source the information
source_verification_task = Task(
    description=(
        "Provide a detailed response to {company}'s inquiry. Include specific features, examples, or discount info "
        "with citations from https://finkraft.ai/en or other sources."
    ),
    expected_output=(
        "A detailed, sourced response with examples addressing all inquiry parts."
    ),
    tools=[finkraft_scrape_tool, SerperDevTool()],
    agent=trust_source_agent
)

# Task 3: Engage with follow-ups
engagement_task = Task(
    description=(
        "Engage {company} with a multi-turn conversation based on their inquiry and history. "
        "Ask follow-up questions (e.g., 'Which feature interests you?') and build on previous responses."
    ),
    expected_output=(
        "An engaging response with follow-up questions, continuing the dialogue."
    ),
    agent=engagement_nudge_agent
)

# Task 4: Capture lead details
lead_capture_task = Task(
    description=(
        "If {company} shows interest, ask for their name and email conversationally and suggest next steps."
    ),
    expected_output=(
        "Lead details (if provided) and a next-step suggestion, integrated into the response."
    ),
    agent=lead_capture_agent
)

# Task 5: Simulate and review the conversation
simulation_review_task = Task(
    description=(
        "Simulate and review the full conversation for {company}. Ensure it’s engaging, accurate, and multi-turn. "
        "Add contact details (email: contact@finkraft.ai, phone: +91-9876543210) at the end."
    ),
    expected_output=(
        "A refined, multi-turn conversation with contact details at the end."
    ),
    agent=message_simulation_review_agent
)

# Create the Crew with all agents and tasks
sales_crew = Crew(
    agents=[
        instant_clarity_agent,
        trust_source_agent,
        engagement_nudge_agent,
        lead_capture_agent,
        message_simulation_review_agent
    ],
    tasks=[
        initial_clarity_task,
        source_verification_task,
        engagement_task,
        lead_capture_task,
        simulation_review_task
    ],
    verbose=True,
    memory=True
)

# Streamlit UI
def main():
    st.set_page_config(page_title="Finkraft AI Sales Chatbot", layout="wide")
    st.title("Finkraft AI Sales Chatbot")
    st.write("Ask about Finkraft's AI solutions, and our multi-agent system will assist you with an engaging conversation!")

    # Session management
    session_id = st.session_state.get('session_id', str(uuid.uuid4()))
    st.session_state['session_id'] = session_id
    session = load_session(session_id)

    # Input fields
    company = st.text_input("Your Company Name", value=session.get("context", {}).get("company", "Potential Customer Inc."))
    inquiry = st.text_area("Your Inquiry", value=session.get("context", {}).get("inquiry", ""))

    # Display conversation history
    st.subheader("Conversation History")
    for entry in session["history"]:
        st.markdown(entry)

    # Button to trigger the crew
    if st.button("Submit Inquiry"):
        if company and inquiry:
            with st.spinner("Processing your inquiry..."):
                inputs = {
                    "company": company,
                    "inquiry": inquiry
                }
                try:
                    # Run the crew and get the result
                    result = sales_crew.kickoff(inputs=inputs)
                    
                    # Append to session history
                    timestamp = datetime.now().strftime("%I:%M %p IST, %B %d, %Y")
                    session["history"].append(f"**{company} ({timestamp}):** {inquiry}")
                    session["history"].append(f"**Finkraft Bot ({timestamp}):** {result}")
                    session["context"]["company"] = company
                    session["context"]["inquiry"] = inquiry
                    save_session(session_id, session)

                    # Update UI with new response
                    st.subheader("Response")
                    st.markdown(result)
                    
                    # Suggest follow-up
                    st.write("Would you like to continue the conversation? Submit another inquiry or let us know how we can assist further!")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please provide both company name and inquiry.")

if __name__ == "__main__":
    main()
