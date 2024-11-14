from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Condition(ABC):
    variable: str
    value: int | str

    @property
    @abstractmethod
    def operator(self):
        raise NotImplementedError(f"{self.__class__.__name__}.operator not implemented")
    
    @abstractmethod
    def negate(self):
        raise NotImplementedError(f"{self.__class__.__name__}.negate not implemented")
    
    @abstractmethod
    def contradicts(self):
        raise NotImplementedError(f"{self.__class__.__name__}.contradicts not implemented")
    
    def __str__(self):
        raise NotImplementedError(f"{self.__class__.__name__}.__str__ not implemented")
    
    def __eq__(self):
        raise NotImplementedError(f"{self.__class__.__name__}.__eq__ not implemented")

class EqualsCondition(Condition):

    @property
    def operator(self):
        raise NotImplementedError(f"{self.__class__.__name__}.operator not implemented")
    
    def negate(self):
        raise NotImplementedError(f"{self.__class__.__name__}.negate not implemented")
    
    def contradicts(self):
        raise NotImplementedError(f"{self.__class__.__name__}.contradicts not implemented")

class NotEqualsCondition(Condition):
    
    @property
    def operator(self):
        raise NotImplementedError(f"{self.__class__.__name__}.operator not implemented")
    
    def negate(self):
        raise NotImplementedError(f"{self.__class__.__name__}.negate not implemented")
    
    def contradicts(self):
        raise NotImplementedError(f"{self.__class__.__name__}.contradicts not implemented")
    
class GreaterThanCondition(Condition):
    
    @property
    def operator(self):
        raise NotImplementedError(f"{self.__class__.__name__}.operator not implemented")
    
    def negate(self):
        raise NotImplementedError(f"{self.__class__.__name__}.negate not implemented")
    
    def contradicts(self):
        raise NotImplementedError(f"{self.__class__.__name__}.contradicts not implemented")

class GreaterThanOrEqualCondition(Condition):
    
    @property
    def operator(self):
        raise NotImplementedError(f"{self.__class__.__name__}.operator not implemented")
    
    def negate(self):
        raise NotImplementedError(f"{self.__class__.__name__}.negate not implemented")
    
    def contradicts(self):
        raise NotImplementedError(f"{self.__class__.__name__}.contradicts not implemented")

class LessThanCondition(Condition):
    
    @property
    def operator(self):
        raise NotImplementedError(f"{self.__class__.__name__}.operator not implemented")
    
    def negate(self):
        raise NotImplementedError(f"{self.__class__.__name__}.negate not implemented")
    
    def contradicts(self):
        raise NotImplementedError(f"{self.__class__.__name__}.contradicts not implemented")

class LessThanOrEqualCondition(Condition): 

    @property
    def operator(self):
        raise NotImplementedError(f"{self.__class__.__name__}.operator not implemented")
    
    def negate(self):
        raise NotImplementedError(f"{self.__class__.__name__}.negate not implemented")
    
    def contradicts(self):
        raise NotImplementedError(f"{self.__class__.__name__}.contradicts not implemented")
