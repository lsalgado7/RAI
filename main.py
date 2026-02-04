# --- ENV SETUP ---
import os
from dotenv import load_dotenv
from typing import List, Optional
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

os.makedirs("data", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# Init LLM
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# --- ESTABLISH REPORT PARAMETERS ---
class MarketMetric(BaseModel):
    company_name: str = Field(..., description="Name of the company")
    stock_price: Optional[float] = Field(..., description="Current stock price")
    revenue_growth: str = Field(..., description="Revenue growth percentage")
    source_url: str = Field(..., description="URL where data was found")

class MarketReport(BaseModel):
    # Return a list of companies
    metrics: List[MarketMetric] = Field(..., description="List of market metrics for different companies")

# Agent Parameters

researcher = Agent(
    role='Senior Researcher',
    goal='Uncover latest financial data about {topic}',
    backstory="You are an expert at finding hidden financial gems.",
    tools=[SerperDevTool()],
    allow_delegation=False,
    memory=True,
    llm=gemini_llm
)

data_engineer = Agent(
    role='Data Engineer',
    goal='Extract exact metrics into structured JSON formats.',
    backstory="You hate fluff. You only care about rows and columns.",
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

writer = Agent(
    role='Tech Writer',
    goal='Write a compelling executive summary.',
    backstory="You write for C-level executives.",
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

# Task Outlines

research_task = Task(
    description='Research {topic} extensively. If the topic involves multiple companies, find data for all of them.',
    expected_output='A comprehensive dossier of findings.',
    agent=researcher
)

csv_task = Task(
    description='Extract financial metrics from the research.',
    expected_output='A valid JSON object matching the MarketReport schema.',
    agent=data_engineer,
    context=[research_task],
    output_pydantic=MarketReport,
    output_file='data/metrics.json'
)

report_task = Task(
    description='Write an executive summary of the research.',
    expected_output='A markdown formatted report.',
    agent=writer,
    context=[research_task],
    output_file='reports/summary.md'
)

# Crew Parameters

crew = Crew(
    agents=[researcher, data_engineer, writer],
    tasks=[research_task, csv_task, report_task],
    process=Process.sequential,
    # Low RPM to accomadate for gemini's free plan
    max_rpm=3
)

# --- EXECUTION ---
if __name__ == "__main__":
    print("## Welcome to the Agentic Research Squad")
    print("---------------------------------------")
    topic = input("Enter a stock or market topic (e.g., 'Nvidia vs AMD'): ")
    
    try:
        print("Testing API connection...")
        gemini_llm.invoke("Hello")
        print("Connection successful! Launching Crew...")
        result = crew.kickoff(inputs={'topic': topic})
        print(result)
    except Exception as e:
        print(f"API Failed immediately: {e}")
        print("DOUBLE CHECK: Did you use a key from aistudio.google.com?")