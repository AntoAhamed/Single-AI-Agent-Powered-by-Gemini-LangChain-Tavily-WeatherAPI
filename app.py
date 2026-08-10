import os
import certifi
import requests
import streamlit as st

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
from langchain.agents import create_agent


# ==========================================
# CONFIGURATION
# ==========================================

os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERAPI_API_KEY = os.getenv("WEATHERAPI_API_KEY")


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Research Agent",
    page_icon="🤖",
    layout="centered"
)


# ==========================================
# PAGE TITLE
# ==========================================

st.title("🤖 Research Agent")
st.caption("Powered by Gemini + LangChain + Tavily + WeatherAPI")


# ==========================================
# SEARCH TOOL
# ==========================================

search_tool = TavilySearchResults(
    max_results=2
)


# ==========================================
# WEATHER TOOL
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

prompt = (
    "You are a helpful research assistant. "
    "Use the available tools when you need current or external information. "
    "For questions requiring multiple pieces of information, "
    "complete the necessary tool calls before giving the final answer."
)


# ==========================================
# TOOLS
# ==========================================

tools = [
    search_tool,
    get_weather_data
]


# ==========================================
# CREATE AGENT
# ==========================================

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=prompt
)


# ==========================================
# CHAT HISTORY
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================
# DISPLAY PREVIOUS MESSAGES
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==========================================
# CHAT INPUT
# ==========================================

user_input = st.chat_input(
    "Ask me anything..."
)


# ==========================================
# RUN AGENT
# ==========================================

if user_input:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })


    # Run agent
    with st.chat_message("assistant"):

        with st.spinner("Researching..."):

            response = agent.invoke({
                "messages": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            })


            # Get final message
            final_message = response["messages"][-1]

            content = final_message.content

            # Gemini may return content as a list
            if isinstance(content, list):

                text_parts = []

                for item in content:

                    if isinstance(item, dict) and "text" in item:
                        text_parts.append(item["text"])

                answer = "\n".join(text_parts)

            else:
                answer = str(content)


        # Display answer
        st.markdown(answer)


    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })