from pydantic import BaseModel, Field
from typing import List, Optional

class DatasetEntry(BaseModel):
    title: str = Field(..., description="The official name of the dataset")
    url: str = Field(..., description="Direct link to the dataset download page")
    file_format: Optional[str] = Field(None, description="The format of the data (e.g., CSV, JSON, DICOM, MRI)")
    source_platform: str = Field(..., description="Where it is hosted (e.g., Kaggle, HuggingFace, Zenodo)")
    description: str = Field(..., description="A brief 1-sentence summary of what the data contains")

class DatasetReport(BaseModel):
    datasets: List[DatasetEntry] = Field(..., description="List of discovered datasets")