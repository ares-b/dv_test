from dataclasses import dataclass
from abc import ABC
from typing import List

from conditions import (
    Condition,
    EqualsCondition, NotEqualsCondition,
    GreaterThanCondition, GreaterThanOrEqualCondition,
    LessThanCondition, LessThanOrEqualCondition
)
from strategy import Strategy
    
@dataclass
class TreeNode(ABC):
    id: int

@dataclass
class LeafNode(TreeNode):
    value: float

    def __str__(self):
        raise NotImplementedError(f"{self.__class__.__name__}.__str__ not implemented")

    def __eq__(self):
        raise NotImplementedError(f"{self.__class__.__name__}.__str__ not implemented")

@dataclass
class ConditionNode(TreeNode):
    conditions: List[Condition]
    true_branch: TreeNode | None = None
    false_branch: TreeNode | None = None

    def __str__(self):
        raise NotImplementedError(f"{self.__class__.__name__}.__str__ not implemented")

    def __eq__(self):
        raise NotImplementedError(f"{self.__class__.__name__}.__str__ not implemented")

@dataclass(frozen=True)
class StrategyTree:

    root: TreeNode

    LEAF_REGEXP = r"(\d+):leaf=([\d.]+)"
    CONDITION_VALUE_REGEXP = r"(\d+):\[(.*)\]\s?yes=(\d+),\s?no=(\d+)"
    CONDITION_REGEXP = r"(\w+)(=|!=|>|<|>=|<=)(\S+)"
    CONDITION_CLASSES = {
        "=": EqualsCondition,
        "!=": NotEqualsCondition,
        ">": GreaterThanCondition,
        ">=": GreaterThanOrEqualCondition,
        "<": LessThanCondition,
        "<=": LessThanOrEqualCondition
    }

    def get_strategies(self) -> List[Strategy]:
        raise NotImplementedError(f"{self.__class__.__name__}.get_strategies not implemented")

    @classmethod
    def from_string(cls, content: str) -> "StrategyTree":
        raise NotImplementedError(f"{cls.__name__}.from_string not implemented")

    @classmethod
    def from_file(cls, filename: str) -> "StrategyTree":
        raise NotImplementedError(f"{cls.__name__}.from_file not implemented")

    def __str__(self):
        raise NotImplementedError(f"{self.__class__.__name__}.__str__ not implemented")
    
    def __eq__(self, other: "StrategyTree"):
        raise NotImplementedError(f"{self.__class__.__name__}.__eq__ not implemented")

def main():
    pass