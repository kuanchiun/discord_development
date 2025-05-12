from abc import ABC, abstractmethod
from typing import List, Optional, Dict

class JobBranch(ABC):
    name: str
    main_attribute: List[str]
    dot_attribute: str
    
    