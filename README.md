# Research Agent with Gemini, LangChain, Tavily, and WeatherAPI

A lightweight AI research assistant built with Python, LangChain, and Google Gemini. The app can answer user questions by combining web search results with a custom weather tool, and it includes both a Streamlit chat interface and a simple one-off CLI example.

## Features

- Research agent powered by Google Gemini
- Web search via Tavily
- Custom weather lookup tool using WeatherAPI
- Interactive chat UI with Streamlit
- Simple command-line example for quick testing
- Example notebook in the research folder

## Project Structure

- `app.py` — Streamlit web application
- `main.py` — simple non-UI agent example
- `requirements.txt` — Python dependencies
- `research/agent_vinod.ipynb` — notebook with additional exploration
- `.env` — local environment variables (not committed)

## Tech Stack

- Python
- LangChain
- LangChain Google GenAI integration
- Tavily search API
- WeatherAPI
- Streamlit
- python-dotenv

## Prerequisites

- Python 3.10 or newer
- API keys for:
  - Google Gemini
  - Tavily
  - WeatherAPI

## Setup

1. Clone the repository and open the project folder.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your API keys:

   ```env
   GEMINI_API_KEY=your_gemini_api_key
   TAVILY_API_KEY=your_tavily_api_key
   WEATHERAPI_API_KEY=your_weatherapi_key
   ```

## Run the Streamlit App

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal to use the chat interface.

## Run the CLI Example

```bash
python main.py
```

This runs a predefined prompt and prints the agent’s response in the terminal.

## How the Agent Works

The agent uses a Gemini model with two tools:

1. `TavilySearchResults` for retrieving current web information
2. `get_weather_data(city)` for retrieving live weather data for a location

The system prompt instructs the model to use tools whenever external or current information is needed.

## Example Use Cases

- “What is the capital of Bangladesh?”
- “What is the current weather in Dhaka?”
- “Search for recent updates on AI news and summarize the top results.”

## Notes

- The app sets `SSL_CERT_FILE` using `certifi.where()` for certificate compatibility.
- API keys are loaded from `.env` using `python-dotenv`.
- The `research/agent_vinod.ipynb` notebook can be used for experimentation and further development.

## License

This project is provided for learning and experimentation purposes. Add a license file if you plan to distribute it publicly.
