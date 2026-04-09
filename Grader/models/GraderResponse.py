from dataclasses import dataclass
from typing import List

@dataclass
class GraderResponse:
    score: int
    max_score: int
    feedback: str
    missing_points: List[str]
    confidence: float
