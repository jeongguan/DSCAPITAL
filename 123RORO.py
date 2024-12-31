# Import necessary modules and tools
import openai
from phi.agent import Agent, RunResponse
from phi.model.openai import OpenAIChat
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.tools.calculator import Calculator
from phi.tools.baidusearch import BaiduSearch
from phi.tools.newspaper4k import Newspaper4k
from phi.tools.googlesearch import GoogleSearch
from phi.model.ollama import Ollama

from phi.playground import Playground, serve_playground_app

# Initialize OpenAI API Key (ensure to link this to a .env file for security)

openai.api_key = "####"
# -----------------------------------
# 1. Macro Data Agent
# -----------------------------------
# Initialize the Macro Data Agent to analyze global macroeconomic indicators and determine the market environment.
macro_data_agent = Agent(
    name="Macro Data Agent",
    model=Ollama(id="llama3.1"),
    tools=[
        DuckDuckGo(),
        BaiduSearch(),
        GoogleSearch(),
        Calculator(
            add=True,
            subtract=True,
            multiply=True,
            divide=True,
            exponentiate=True,
            factorial=True,
            is_prime=True,
            square_root=True,
        )
    ],
  instructions=[
        "Analyze global macroeconomic indicators to determine if the environment is Risk On or Risk Off.",
        "Consider the rate of change (acceleration or deceleration) of these indicators.",
        "Use DuckDuckGo, BaiduSearch, and Google Search to gather relevant data.",
        "Utilize the Calculator tool to compute necessary rate changes.",
        "Project the data 1 week and 2 weeks ahead to establish relevant timeframes.",
        "Sort the release of results of indicators within the next 1 week and 2 weeks.",
        "Weight the impact of each indicator, with Growth and Inflation data points having a heavier weight as they trigger heavier trading flows.",
        "Assess the strength of the US Dollar: (A) A stronger dollar tends to lead to a Risk Off environment as investors sell into the dollar, causing other currencies to weaken A weaker dollar tends to lead to a Risk On environment as investors sell dollars to buy assets.",
        "Use the rate of change in the dollar's strength and other indicators to follow Risk Off and Risk On environments.",
        "Backtest the Risk On and Risk Off probabilities against historical data to ensure accuracy and consistency.",
        "Output the probabilities for Risk On and Risk Off environments in percentages down to two decimal places.",
        "Assess the likelihood of acceleration within the next 1 week and 2 week timeframes.",
        "Aggregate sources from 100 websites to determine the percentage of Risk On and Risk Off sentiments.",
        "Provide a summary of daily headlines regarding macroeconomic data."
    ],
    show_tool_calls=True,
    markdown=True,
    description="Determines the current market environment as Risk On or Risk Off based on global macroeconomic indicators, their rate of change, and the strength of the US Dollar."
)

# -----------------------------------
# 2. Macro Data Agent Senior
# -----------------------------------
macro_data_agent_senior = Agent(
    name="Macro Data Agent Senior",
    model=Ollama(id="llama3.1"),
    tools=[
        DuckDuckGo(),
        BaiduSearch(),
        GoogleSearch(),
        Calculator(
            add=True,
            subtract=True,
            multiply=True,
            divide=True,
            exponentiate=True,
            factorial=True,
            is_prime=True,
            square_root=True,
        ),
  
    ],
    instructions=[
        "Perform advanced analysis on macroeconomic indicators to validate Risk On and Risk Off probabilities.",
        "Conduct backtesting against historical data to ensure accuracy and consistency of Risk On and Risk Off scores.",
        "Analyze the rate of change in indicators and the strength of the US Dollar to identify historical patterns of Risk On and Risk Off environments.",
        "Provide insights and adjustments to the Risk On and Risk Off models based on historical performance.",
        "Collaborate with Macro Data Agent to enhance data accuracy and reliability."
    ],
    show_tool_calls=True,
    markdown=True,    description="Performs advanced analysis and backtesting on macroeconomic indicators to validate and enhance Risk On and Risk Off probability models."

)

# -----------------------------------
# 3. Integrate Agents into a Team (Optional)
# -----------------------------------
macro_analyst_team = Agent(
    name="Macro Analyst Team",
    team=[macro_data_agent, macro_data_agent_senior],
    model=Ollama(id="llama3.1"),
    instructions=[
        "Lead and coordinate the Macro Data Agent and Macro Data Agent Senior to ensure comprehensive and accurate market environment analysis.",
        "Facilitate effective communication and collaboration between agents for thorough data analysis, validation, and backtesting.",
        "Integrate findings from both agents to compile a robust final assessment of Risk On and Risk Off probabilities.",
        "Ensure that the team judgment and rationale are clearly documented and justified based on data-driven insights.",
        "Oversee the aggregation of data from 100 websites to determine the overall sentiment towards Risk On and Risk Off environments.",
        "Present the final Risk On and Risk Off probabilities along with the likelihood of acceleration within the next 1 week and 2 week timeframes.",
        "Provide a summary of daily macroeconomic headlines to support the risk assessment."
    ],
    show_tool_calls=True,
    markdown=True,
    description="Leads the Macro Analyst Team to provide a comprehensive assessment of market environments as Risk On or Risk Off, utilizing coordinated efforts from specialized agents for accurate and validated insights."
)


# -----------------------------------
# PRINT TEST ZONE 
# -----------------------------------

macro_analyst_team.print_response("What is the Risk on and Risk off Probaility for This Week and Next Week")

