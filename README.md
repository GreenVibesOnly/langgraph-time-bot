# LangGraph Stateless Chat Bot with Time Tool
This is a simple stateless bot built with LangGraph that responds to the question “What time is it?” by calling a custom tool `get_current_time`.

## Features
Powered by OpenAI GPT-4o.
Built using LangGraph and LangChain Agents.
Uses a custom get_current_time tool to return the current UTC time.
Stateless MessageGraph flow with tool integration.

## Installation
Clone the repository:
git clone https://github.com/your-username/langgraph-time-bot.git
cd langgraph-time-bot

Create a virtual environment and install dependencies:
python -m venv .venv && source .venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

Create a .env file with your OpenAI API key:
OPENAI_API_KEY=<your_key>

## Run the Bot
Start the dev server with the LangGraph CLI:
langgraph dev