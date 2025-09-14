# Finkraft AI Sales Chatbot


The Finkraft AI Sales Chatbot is a multi-agent conversational assistant built with Streamlit and CrewAI. It simulates a sales workflow for Finkraft, engaging users, answering FAQs, sourcing information, capturing leads, and reviewing conversations. The chatbot leverages multiple specialized agents to provide accurate, engaging, and context-aware responses.

## Features
- Multi-agent architecture for robust sales conversations
- Real-time web scraping for up-to-date information
- Lead capture and follow-up suggestions
- Persistent session management
- User-friendly Streamlit interface

## Packages Used
- `streamlit`: For building the interactive web UI
- `crewai`: For agent/task/crew orchestration
- `crewai_tools`: For web scraping and search tools
- `uuid`: For unique session management
- `datetime`: For timestamping interactions
- `os`, `json`, `warnings`: For environment, data, and warning control

## How It Works

### 1. User Interaction
- The user enters their company name and inquiry in the Streamlit UI.
- The chatbot displays the conversation history for context.
- On submitting an inquiry, the chatbot processes the request using its multi-agent system.

### 2. Agent Workflow
The chatbot uses five specialized agents, each with a distinct role:

#### 1. Instant Clarity Agent
- Handles simple FAQs and objections instantly.
- Escalates complex queries to other agents.

#### 2. Trust & Source Agent
- Provides detailed, sourced answers with citations and examples.
- Uses web scraping and search tools for up-to-date information.

#### 3. Engagement & Nudge Agent
- Engages users with multi-turn conversations.
- Asks follow-up questions to maintain engagement.

#### 4. Lead Capture Agent
- Conversationally collects user details (name, email) when interest is shown.
- Integrates lead capture into the dialogue, avoiding forms.

#### 5. Message Simulation & Review Agent
- Simulates and refines the conversation for accuracy and engagement.
- Adds contact details and ensures a complete, professional closing.

### 3. Task Assignment
Each agent is assigned a specific task:
- **Initial Clarity Task:** Handles the first user inquiry.
- **Source Verification Task:** Provides detailed, sourced responses.
- **Engagement Task:** Engages with follow-up questions.
- **Lead Capture Task:** Captures user details and suggests next steps.
- **Simulation Review Task:** Reviews and refines the conversation.

### 4. Crew Orchestration
- All agents and tasks are managed by a `Crew` object.
- When the user submits an inquiry, the crew is triggered with the user's input.
- The crew coordinates agent responses, passing context and results between agents as needed.
- The final response is displayed to the user and saved in the session history.

### 5. Session Management
- Each user session is tracked using a unique session ID.
- Conversation history and context are saved in `chat_sessions.json`.
- Users can continue the conversation, with context preserved across interactions.

## Step-by-Step Workflow

1. **User submits an inquiry**
   → Inquiry is received by the chatbot UI.
2. **Instant Clarity Agent**
   → Handles simple FAQs and objections instantly.
   → If the query is complex, escalates to Trust & Source Agent.
3. **Trust & Source Agent**
   → Provides a detailed, sourced answer with citations and examples.
   → Passes context to Engagement & Nudge Agent.
4. **Engagement & Nudge Agent**
   → Engages the user with follow-up questions (e.g., "Which feature interests you?").
   → If user shows interest, passes context to Lead Capture Agent.
5. **Lead Capture Agent**
   → Conversationally requests user details (name, email) if interest is shown.
   → Passes conversation to Message Simulation & Review Agent.
6. **Message Simulation & Review Agent**
   → Refines and reviews the conversation for accuracy and engagement.
   → Adds contact details and ensures a complete closing.
7. **Final response**
   → Displayed to the user in the UI.
   → Saved in the session history for future reference.


