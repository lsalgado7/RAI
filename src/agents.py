from crewai import Agent
from crewai_tools import SerperDevTool

class ResearchAgents:
    def __init__(self, llm):
        self.llm = llm
        self.search_tool = SerperDevTool()

    def researcher(self):
        return Agent(
            role='Data Scout',
            goal='Find high-quality, open-source datasets related to {topic}',
            # We explicitly guide it to scientific repos
            backstory="You are a specialized academic librarian. You know how to dig through Kaggle, HuggingFace, UCI Repo, and government databases (CDC, NIH) to find raw data.",
            tools=[self.search_tool],
            allow_delegation=False,
            memory=True,
            llm=self.llm
        )

    def data_engineer(self):
        return Agent(
            role='Metadata Specialist',
            goal='Extract technical metadata (Format, Size, Link) from research results.',
            backstory="You are meticulous. You verify that links are actual datasets and not just articles talking about data.",
            allow_delegation=False,
            llm=self.llm
        )

    def writer(self):
        return Agent(
            role='Academic Advisor',
            goal='Summarize the available data landscape for a researcher.',
            backstory="You help researchers understand which datasets are best for their thesis. You highlight pros and cons of the discovered data.",
            allow_delegation=False,
            llm=self.llm
        )