from crewai import Task
from src.models import DatasetReport

class ResearchTasks:
    def __init__(self, agents):
        self.agents = agents

    def research_task(self, topic):
        return Task(
            description=f'''
                Search for open-source datasets regarding: {topic}.
                Prioritize sources like Kaggle, HuggingFace, Zenodo, PapersWithCode, and UCI Machine Learning Repository.
                Look for:
                1. Direct download links
                2. File formats (CSV, JSON, Images)
                3. Dataset size (if available)
            ''',
            expected_output='A list of potential datasets with their URLs and descriptions.',
            agent=self.agents['researcher']
        )

    def csv_task(self, topic, context):
        return Task(
            description='Extract the dataset details into a structured list.',
            expected_output='A valid JSON object matching the DatasetReport schema.',
            agent=self.agents['data_engineer'],
            context=context,
            output_pydantic=DatasetReport,
            output_file='data/metrics.json' 
        )

    def report_task(self, topic, context):
        return Task(
            description='Write a guide on "Where to find data for this topic". Recommend the top 3 datasets.',
            expected_output='A markdown formatted guide for a student.',
            agent=self.agents['writer'],
            context=context,
            output_file='reports/summary.md'
        )