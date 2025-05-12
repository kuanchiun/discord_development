import yaml

from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict

FILE_PATH = "job.yml"

@dataclass
class Job:
    name: str
    description: str
    
    skills: List[str]
    
    next_job: Optional[List[str]] = field(default_factory = list)
    required_level: Optional[int] = None


def get_job_list() -> Dict[str, Job]:
    with open(FILE_PATH, "r", encoding = "utf-8") as f:
        jobs = yaml.safe_load(f)
        
    return {job["name"]: Job(**job) for job in jobs}
