import os
import certifi
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
import requests

from langchain.agents import create_agent

# ==========================================
# LOAD ENV VARIABLES
# ==========================================

os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERAPI_API_KEY = os.getenv("WEATHERAPI_API_KEY")

# ==========================================
# SEARCH TOOL
# ==========================================

search_tool = TavilySearchResults(max_results=2)

# ==========================================
# CUSTOM TOOL
# ==========================================

@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a city.
    """

    url = (
        f"https://api.weatherapi.com/v1//current.json?"
        f"key={WEATHERAPI_API_KEY}&q={city}"
    )

    response = requests.get(url)

    data = response.json()

    if "current" not in data:
        return f"Could not fetch weather data for {city}"

    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temp_c']}°C\n"
        f"Weather: {data['current']['condition']['text']}\n"
        f"Humidity: {data['current']['humidity']}%"
    )

# ==========================================
# LLM
# ==========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=GEMINI_API_KEY
)

# ==========================================
# SYSTEM PROMPT
# ==========================================

prompt=(
        "You are a helpful research assistant. "
        "Use the available tools when you need current or external information. "
        "For questions requiring multiple pieces of information, "
        "complete the necessary tool calls before giving the final answer."
)

# ==========================================
# TOOLS
# ==========================================

tools = [search_tool, get_weather_data]

# ==========================================
# CREATE AGENT
# ==========================================

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=prompt
)

# ==========================================
# RUN
# ==========================================

response = agent.invoke({
        "messages": [{
                "role": "user",
                "content": "What is the capital of Bangladesh and what is the current weather there?"
            }]
})

print(response["messages"][-1].content[0]["text"])
