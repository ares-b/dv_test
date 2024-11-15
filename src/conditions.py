from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Self

@dataclass
class Condition(ABC):
    variable: str
    value: int | str

    @property
    @abstractmethod
    def operator(self) -> str:
        raise NotImplementedError(f"{self.__class__.__name__}.operator not implemented")
    
    @abstractmethod
    def negate(self) -> Self:
        raise NotImplementedError(f"{self.__class__.__name__}.negate not implemented")

    @abstractmethod
    def contradicts(self, other: "Condition") -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.contradicts not implemented")
    
    def __str__(self) -> str:
        return f"{self.variable}{self.operator}{self.value}"
    
    def __eq__(self, other: "Condition") -> bool:
        return self.variable == other.variable and self.value == other.value and self.operator == other.operator

class EqualsCondition(Condition):

    def negate(self) -> Self:
        return NotEqualsCondition(self.variable, self.value)
    
    def contradicts(self, other: Condition) -> bool:
        if isinstance(other, EqualsCondition):
            return self.variable == other.variable and self.value != other.value
        elif isinstance(other, NotEqualsCondition):
            return self.variable == other.variable and self.value == other.value
        elif isinstance(other, GreaterThanCondition):
            return self.variable == other.variable and self.value <= other.value
        elif isinstance(other, GreaterThanOrEqualCondition):
            return self.variable == other.variable and self.value < other.value
        elif isinstance(other, LessThanCondition):
            return self.variable == other.variable and self.value >= other.value
        elif isinstance(other, LessThanOrEqualCondition):
            return self.variable == other.variable and self.value > other.value
        return False
        
    @property
    def operator(self) -> str:
        return "="

class NotEqualsCondition(Condition):

    def negate(self) -> Self:
        return EqualsCondition(self.variable, self.value)
    
    def contradicts(self, other: Condition) -> bool:
        if isinstance(other, EqualsCondition):
            return self.variable == other.variable and self.value == other.value
        return False
    
    @property
    def operator(self) -> str:
        return "!="
    
class GreaterThanCondition(Condition):

    def negate(self) -> Self:
        return LessThanOrEqualCondition(self.variable, self.value)
    
    def contradicts(self, other: Condition) -> bool:
        if isinstance(other, EqualsCondition):
            return self.variable == other.variable and self.value >= other.value
        if isinstance(other, LessThanCondition):
            return self.variable == other.variable and self.value >= other.value
        if isinstance(other, LessThanOrEqualCondition):
            return self.variable == other.variable and self.value >= other.value
        return False
        
    @property
    def operator(self) -> str:
        return ">"

class GreaterThanOrEqualCondition(Condition):
   
    def negate(self) -> Self:
        return LessThanCondition(self.variable, self.value)
    
    def contradicts(self, other: Condition) -> bool:
        if isinstance(other, EqualsCondition):
            return self.variable == other.variable and self.value > other.value
        if isinstance(other, LessThanCondition):
            return self.variable == other.variable and self.value > other.value
        if isinstance(other, LessThanOrEqualCondition):
            return self.variable == other.variable and self.value > other.value
        return False
    
    @property
    def operator(self) -> str:
        return ">="

class LessThanCondition(Condition):

    def negate(self) -> Self:
        return GreaterThanOrEqualCondition(self.variable, self.value)
    
    def contradicts(self, other: Condition) -> bool:
        if isinstance(other, EqualsCondition):
            return self.variable == other.variable and self.value <= other.value
        if isinstance(other, GreaterThanCondition):
            return self.variable == other.variable and self.value <= other.value
        if isinstance(other, GreaterThanOrEqualCondition):
            return self.variable == other.variable and self.value <= other.value
        return False
    
    @property
    def operator(self) -> str:
        return "<"

class LessThanOrEqualCondition(Condition): 
    
    def negate(self) -> Self:
        return GreaterThanCondition(self.variable, self.value)
    
    def contradicts(self, other: Condition) -> bool:
        if isinstance(other, EqualsCondition):
            return self.variable == other.variable and self.value < other.value
        if isinstance(other, GreaterThanCondition):
            return self.variable == other.variable and self.value <= other.value
        if isinstance(other, GreaterThanOrEqualCondition):
            return self.variable == other.variable and self.value < other.value
        return False
        
    @property
    def operator(self) -> str:
        return "<="
