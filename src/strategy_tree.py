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
        return f"leaf={self.value}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LeafNode):
            return False
        return self.id == other.id and self.value == other.value
    
@dataclass
class ConditionNode(TreeNode):
    conditions: List[Condition]
    true_branch: TreeNode
    false_branch: TreeNode

    def __str__(self):
        conditions_str = "||or||".join(str(cond) for cond in self.conditions)
        return f"[{conditions_str}] yes={self.true_branch.id}, no={self.false_branch.id}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ConditionNode):
            return False
        return (
            self.id == other.id and
            self.conditions == other.conditions and
            self.true_branch == other.true_branch and
            self.false_branch == other.false_branch
        )
    
@dataclass
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
        stack = [(self.root, [])]
        results = []

        while stack:
            node, accumulator = stack.pop()

            if isinstance(node, LeafNode):
                strategy = Strategy(conditions=accumulator, value=node.value).prune()
                if strategy is not None:
                    results.append(strategy)

            elif isinstance(node, ConditionNode):
                for condition in node.conditions:
                    stack.append((node.true_branch, accumulator + [condition]))

                    stack.append((node.false_branch, accumulator + [condition.negate()]))

        return results

    @classmethod
    def from_string(cls, content: str) -> "StrategyTree":
        import re
        
        nodes = {}
        for line in content.splitlines():
            line = line.strip()

            leaf_match = re.match(cls.LEAF_REGEXP, line)
            if leaf_match:
                node_id, node_value = int(leaf_match.group(1)), float(leaf_match.group(2))
                nodes[node_id] = LeafNode(node_id, node_value)
            else:
                condition_match = re.match(cls.CONDITION_VALUE_REGEXP, line)
                if condition_match:
                    condition_regex = re.compile(cls.CONDITION_REGEXP)
                    node_id, condition_str, yes_id, no_id = int(condition_match.group(1)), condition_match.group(2), int(condition_match.group(3)), int(condition_match.group(4))

                    condition_list = []
                    for condition in condition_str.split("||or||"):
                        condition_match = condition_regex.match(condition.strip())
                        if not condition_match:
                            raise ValueError(f"Invalid condition format: {condition_str}")
                        
                        variable, operator, value = condition_match.groups()
                        value = int(value) if value.isdigit() else value

                        condition_class = cls.CONDITION_CLASSES.get(operator)
                        if not condition_class:
                            raise ValueError(f"Unsupported operator '{operator}' in condition: {condition_str}")

                        condition_list.append(condition_class(variable, value))

                    nodes[node_id] = ConditionNode(node_id, condition_list, yes_id, no_id)
        
        for node in nodes.values():
            if isinstance(node, ConditionNode):
                node.true_branch = nodes.get(node.true_branch)
                node.false_branch = nodes.get(node.false_branch)
        
        return StrategyTree(nodes[0])

    @classmethod
    def from_file(cls, file_path: str) -> "StrategyTree":
        with open(file_path, 'r') as file:
            content = file.read()
        return cls.from_string(content)

    def __str__(self):
        def recursive_str(node, depth=0):
            indent = '\t' * depth
            result = f"{indent}{node.id}:{node}\n"

            if isinstance(node, ConditionNode):
                if node.true_branch:
                    result += recursive_str(node.true_branch, depth + 1)
                if node.false_branch:
                    result += recursive_str(node.false_branch, depth + 1)

            return result
        
        return recursive_str(self.root).strip()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StrategyTree):
            return False
        return self.root == other.root

def main():
    from os import environ

    dv_tree_file_path = environ.get("DV_TREE_FILE_PATH")
    if dv_tree_file_path is None:
        raise ValueError(f"Cannot find env variable DV_TREE_FILE_PATH")

    tree = StrategyTree.from_file(dv_tree_file_path)

    for strategy in tree.get_strategies():
        print(strategy)
