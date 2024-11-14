from dataclasses import dataclass
from conditions import Condition
from typing import List

@dataclass
class Strategy:
    conditions: List[Condition]
    value: float

    def __str__(self):
        raise NotImplementedError(f"{self.__class__.__name__}.__str__ not implemented")

    def __eq__(self):
        raise NotImplementedError(f"{self.__class__.__name__}.__eq__ not implemented")
    
    def prune(self):
        raise NotImplementedError(f"{self.__class__.__name__}.prune not implemented")