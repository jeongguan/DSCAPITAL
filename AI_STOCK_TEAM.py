import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import inspect  # Ensure the inspect module is imported

# Runtime patch for inspect.getargspec
if not hasattr(inspect, "getargspec"):
    def getargspec_patch(func):
        """Patch to replace inspect.getargspec with inspect.getfullargspec."""
        from collections import namedtuple
        ArgSpec = namedtuple('ArgSpec', ['args', 'varargs', 'keywords', 'defaults'])
        spec = inspect.getfullargspec(func)
        return ArgSpec(
            args=spec.args,
            varargs=spec.varargs,
            keywords=spec.varkw,
            defaults=spec.defaults
        )
    inspect.getargspec = getargspec_patch

# Importing phi tools after applying the patch
from phi.agent import Agent, RunResponse
from phi.model.ollama import Ollama
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.baidusearch import BaiduSearch
from phi.tools.googlesearch import GoogleSearch
from phi.tools.calculator import Calculator
from fredapi import Fred

fred = Fred(api_key='c00e7183c90f3fe002826e4a980b51f9')


# List of top 500 stock tickers (ensure these are valid tickers on Yahoo Finance)
top_500_tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "BRK-B", "NVDA", "META", "V", "JNJ",
    "WMT", "PG", "XOM", "JPM", "UNH", "MA", "HD", "BAC", "PFE", "KO",
    "PEP", "ABBV", "MRK", "COST", "T", "CVX", "DIS", "CSCO", "AVGO", "MCD",
    "TMUS", "DHR", "LLY", "INTC", "CMCSA", "NFLX", "VZ", "NEE", "ADBE", "CRM",
    "TSM", "BABA", "RHHBY", "SHEL", "ASML", "LVMUY", "NVO", "TM", "SAP", "NSRGY",
    "ORCL", "NKE", "HSBC", "UL", "SNY", "RIO", "BP", "TOT", "AMGN", "TXN",
    "SPY", "IVV", "VOO", "QQQ", "IWM", "VTI", "EFA", "IEMG", "VWO", "VEA",
    "BTC", "ETH", "ADA", "USDT", "BNB", "XRP", "DOGE", "SOL", "DOT", "MATIC",
    "GLD", "SLV", "PPLT", "PALL", "IAU", "BAR", "HG", "JJCTF", "CPER",
    "LB", "KC", "OJ", "ZW", "ZS", "CORN", "WEAT", "SOYB", "CL=F", "NG=F",
    "BZ=F", "XLE", "VDE", "OIH", "XOP", "IEO", "PYPL", "SQ", "ZM", "SHOP",
    "ROKU", "DOCU", "CRWD", "SNOW", "UBER", "LYFT", "AMD", "F", "GM", "BA",
    "CAT", "DE", "HON", "GE", "MMM", "IBM", "QCOM", "INTU", "MU", "NOW",
    "ABT", "BMY", "GILD", "VRTX", "REGN", "PLD", "AMT", "CCI", "DLR", "EQIX",
    "O", "SPG", "AVB", "EQR", "MAA", "IBKR", "TROW", "SCHW", "FITB", "KEY",
    "RF", "ZION", "HBAN", "CMA", "STT", "INFY", "TCS", "ITUB", "VALE", "PBR",
    "MELI", "BIDU", "JD", "NTES", "SEA", "EL", "CL", "KMB", "CHD", "HRL",
    "KHC", "GIS", "CPB", "SJM", "TSCO", "NVTA", "ARKK", "ARKG", "ARKW", "TDOC",
    "SQNS", "PLTR", "SPLK", "DDOG", "ZS", "GS", "MS", "BLK", "C", "WFC",
    "USB", "PNC", "TFC", "MTB", "XAGUSD", "XAUUSD", "CME:NG", "CME:CL", "COFFEE",
    "LUMBER", "OAT", "LIVE", "CATTLE", "HOGS",
]

# Set up the AI agent with Ollama3.1
one_agent = Agent(
    name="Agent",
    model=Ollama(id="llama3.1"),
    tools=[
        DuckDuckGo(),
        BaiduSearch(),
        GoogleSearch(),   
    ],
    instructions=[
        "Analyze analyst recommendations and RSI to determine if the stock should be bought, sold, or held, and provide a target price.",
        "Provide a simple and easy-to-digest analysis from a stock and ETF perspective, including target price, timeframe, and probability."
    ],
    show_tool_calls=True,
    markdown=True,
    description="Determines the current market environment as Risk On or Risk Off based on global macroeconomic indicators, their rate of change, and the strength of the US Dollar. Also analyzes analyst recommendations and RSI for stock advice."
)

st.set_page_config(layout="wide")
st.title("Trading2You")
# Add icon links to X and Telegram
st.sidebar.markdown(
    """
    [![X](https://img.icons8.com/ios-filled/25/000000/twitter.png)](https://twitter.com) 
    [![Telegram](https://img.icons8.com/ios-filled/25/000000/telegram-app.png)](https://telegram.org)
    """
)
st.subheader("Dashboard")
# Add a ticker showing live data information from the FRED
# Initialize FRED API (replace 'your_api_key' with your actual FRED API key)

st.sidebar.header("Configuration")
# Function to fetch live data from FRED
def fetch_fred_data(series_id):
    try:
        data = fred.get_series(series_id)
        return data.iloc[-1]  # Get the latest value
    except Exception as e:
        st.error(f"Failed to fetch FRED data: {e}")
        return None

# Example FRED series IDs (e.g., GDP, Unemployment Rate)
fred_series_ids = {
    "GDP": "GDP",
    "Unemployment Rate": "UNRATE",
    "Consumer Price Index": "CPIAUCSL"
}

# Fetch live data for each series
fred_data = {name: fetch_fred_data(series_id) for name, series_id in fred_series_ids.items()}

# Theme selection toggle at the top left of the page
theme = st.sidebar.radio("Select Theme:", ("Light", "Dark"))

# Ticker inputs
ticker = st.sidebar.selectbox("Select Stock Ticker (e.g., AAPL):", top_500_tickers)
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-12-31"))

# Fetch the company name for the selected ticker
def get_company_name(ticker):
    try:
        stock_info = yf.Ticker(ticker).info
        return stock_info.get("longName", ticker)
    except Exception as e:
        st.error(f"Failed to fetch company name: {e}")
        return ticker

company_name = get_company_name(ticker)
st.sidebar.write(f"Selected Ticker: {company_name} ({ticker})")

# Fetch corporate news for the selected ticker
def fetch_corporate_news(ticker):
    try:
        stock_info = yf.Ticker(ticker)
        news = stock_info.news
        return news
    except Exception as e:
        st.error(f"Failed to fetch corporate news: {e}")
        return []

corporate_news = fetch_corporate_news(ticker)

# Display the ticker and corporate news at the top of the page
st.markdown("### Live Economic Indicators and Corporate News")
ticker_text = " | ".join([f"{name}: {value}" for name, value in fred_data.items() if value is not None])
news_text = " | ".join([f"{item['title']}" for item in corporate_news])
st.markdown(f"<marquee>{ticker_text} | {news_text}</marquee>", unsafe_allow_html=True)

# Fetch stock data
if st.sidebar.button("Fetch Data"):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        st.session_state["stock_data"] = stock_data
        st.success(f"Stock data for {company_name} loaded successfully!")
    except Exception as e:
        st.error(f"Failed to fetch stock data for {company_name}: {e}")

# Display stock data and analysis
if "stock_data" in st.session_state:
    data = st.session_state["stock_data"]

    # Calculate Market Capitalization
    data['Market Cap'] = data['Close'] * 1_000_000  # Assuming a fixed number of outstanding shares

    # Define colors based on the selected theme
    if theme == "Light":
        line_color = 'black'
        grid_color = 'lightgray'
        bg_color = 'white'
        font_color = 'black'
    else:
        line_color = 'white'
        grid_color = 'gray'
        bg_color = 'black'
        font_color = 'white'

    # Plot Market Capitalization chart with enhanced visualization
    fig = go.Figure(
        data=[go.Scatter(
            x=data.index,
            y=data['Market Cap'],
            mode='lines',
            name=f"{company_name} Market Capitalization",
            line=dict(color=line_color, width=2)  # Adjust line color and thickness
        )]
    )
    fig.update_layout(
        title=f"{company_name} Market Capitalization Chart",
        xaxis_title="Date",
        yaxis_title="Market Capitalization (USD)",
        xaxis_rangeslider_visible=False,
        template="plotly_white" if theme == "Light" else "plotly_dark",  # Use appropriate template
        yaxis=dict(
            tickprefix="$",  # Add dollar prefix to Y-axis values
            gridcolor=grid_color,  # Gridlines color
        ),
        xaxis=dict(
            gridcolor=grid_color,  # Gridlines for X-axis
        ),
        margin=dict(l=40, r=40, t=40, b=40),  # Adjust margins for better spacing
        plot_bgcolor=bg_color,  # Set background color to match webpage
        paper_bgcolor=bg_color,  # Set paper background color to match webpage
        font=dict(color=font_color)  # Set font color
    )

    # Add a title font style
    fig.update_layout(title_font=dict(size=20, family='Arial', color=font_color))

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

    # AI Analysis Section
    if st.button("Run AI Analysis"):
        with st.spinner("Analyzing with Ollama3.1..."):
            try:
                # Prepare prompt for Ollama
                messages = [
                    {
                        "role": "user",
                        "content": f"""You are a Stock Analyst using Ollama3.1. Analyze the stock performance of {company_name} ({ticker}) 
                        based on historical data and provide insights. Include recommendations for Buy/Hold/Sell."""
                    }
                ]
                response = one_agent.run(messages=messages)
                if isinstance(response, RunResponse):
                    st.write("### AI Analysis Results:")
                    st.write(response.content)
                else:
                    st.error("AI response could not be retrieved.")
            except Exception as e:
                st.error(f"An error occurred during AI analysis: {e}")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

### Write Message History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar="🧑‍💻").write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar="🤖").write(msg["content"])

## Generator for Streaming Tokens
def generate_response():
    response = one_agent.run(messages=st.session_state.messages)
    if isinstance(response, RunResponse):
        for partial_resp in response:
            st.write(f"Debug: partial_resp type: {type(partial_resp)}, content: {partial_resp}")
            token, _ = partial_resp  # Unpack the tuple correctly
            st.session_state["full_message"] += token
            yield token
    else:
        st.error("AI response could not be retrieved.")

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧑‍💻").write(prompt)
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar="🤖").write_stream(generate_response)
    st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})
    # Chatbot interaction for stock queries
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you with stock information?"}]

    # Display message history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message(msg["role"], avatar="🧑‍💻").write(msg["content"])
        else:
            st.chat_message(msg["role"], avatar="🤖").write(msg["content"])

    # Function to generate response from Ollama3.1
    def generate_response():
        response = one_agent.run(messages=st.session_state.messages)
        if isinstance(response, RunResponse):
            for partial_resp in response:
                token = partial_resp.content
                st.session_state["full_message"] += token
                yield token
        else:
            st.error("AI response could not be retrieved.")

    # Handle user input
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user", avatar="🧑‍💻").write(prompt)
        st.session_state["full_message"] = ""
        st.chat_message("assistant", avatar="🤖").write_stream(generate_response)
        st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})