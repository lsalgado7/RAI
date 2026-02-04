from crewai import Crew, Process, LLM
from src.agents import ResearchAgents
from src.tasks import ResearchTasks
import os

class FinancialCrew:
    def __init__(self, topic):
        self.topic = topic
        
        # Using 2.5 Flash-Lite as it's the cheapest 
        self.llm = LLM(
            model="gemini/gemini-2.5-flash-lite",
            temperature=0.5,
            api_key=os.getenv("GOOGLE_API_KEY")
        )

    def run(self):
        # 1. Initialize Agents
        agents = ResearchAgents(self.llm)
        researcher = agents.researcher()
        data_engineer = agents.data_engineer()
        writer = agents.writer()

        # 2. Initialize Tasks
        tasks = ResearchTasks({'researcher': researcher, 'data_engineer': data_engineer, 'writer': writer})
        
        task1 = tasks.research_task(self.topic)
        task2 = tasks.csv_task(self.topic, [task1])
        task3 = tasks.report_task(self.topic, [task1])

        # 3. Create Crew
        crew = Crew(
            agents=[researcher, data_engineer, writer],
            tasks=[task1, task2, task3],
            process=Process.sequential,
            max_rpm=5
        )

        return crew.kickoff()