import argparse
from dataclasses import dataclass
from abc import ABC
from typing import List, Self

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

    def __str__(self) -> str:
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

    def __str__(self) -> str:
        conditions_str = "||or||".join(str(cond) for cond in self.conditions)
        return f"[{conditions_str}] yes={self.true_branch.id}, no={self.false_branch.id}"

    def __eq__(self, other: object) -> bool:
        from collections import Counter

        if not isinstance(other, ConditionNode):
            return False
        
        return (
            self.id == other.id and
            Counter(self.conditions) == Counter(other.conditions) and
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
    def from_string(cls, content: str) -> Self:
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
    def from_file(cls, file_path: str) -> Self:
        with open(file_path, 'r') as file:
            content = file.read()
        return cls.from_string(content)

    def write_strategies(self, output_file_path: str) -> None:
        with open(output_file_path, 'w') as strategies_file:
            for strategy in self.get_strategies():
                strategies_file.write(f"{strategy}\n")

    def __str__(self) -> str:
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

def get_arg_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description="Deserializes a DV tree file into a binary Tree and prints the strategies")
    parser.add_argument("-f", "--dv-tree-file-path", type=str, required=True, help="Path to the DV tree file")
    parser.add_argument("-o", "--strategies-file-path", type=str, default="strategies.txt", help="Path to output strategies file (default=strategies.txt)")

    return parser.parse_args()

def main():
    args = get_arg_parser()
    tree = StrategyTree.from_file(args.dv_tree_file_path)
    tree.write_strategies(args.strategies_file_path)

if __name__ == "__main__":
    main()
