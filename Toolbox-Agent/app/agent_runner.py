from dotenv import load_dotenv
import os
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import web_search, calc, file_fetch
from langchain.tools import tool

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL"),
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

tools = [web_search.web_search, calc.calculator, file_fetch.file_fetch]

system_prompt = """You have the following tools: {tools}
Use the format Thought / Action / Action Input / Observation / Final Answer.
Question: {input}
Thought:{agent_scratchpad}"""

agent = create_agent(model=llm, tools=tools)

def run_agent(query: str) -> str:
    result = agent.invoke(({
    "messages": [{"role": "user", "content": query}]
}))
    return result['messages'][-1].content

result = run_agent("sin(90)*20 + 25 *cos(45)")
print(type(result))
# print(result.content)

