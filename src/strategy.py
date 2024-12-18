from dataclasses import dataclass
from conditions import (
    Condition,
    EqualsCondition, NotEqualsCondition,
    GreaterThanOrEqualCondition, GreaterThanCondition,
    LessThanOrEqualCondition, LessThanCondition
)
from typing import Self

@dataclass
class Strategy:
    conditions: frozenset[Condition]
    value: float

    def __str__(self) -> str:
        conditions=" && ".join([str(st) for st in self.conditions])
        return f"if ({conditions}) then {self.value}"
    
    def __eq__(self, other: object) -> bool:
        from collections import Counter

        if not isinstance(other, Strategy):
            return False
        
        return Counter(self.conditions) == Counter(other.conditions) and self.value == other.value

    def __hash__(self):
        return hash(self.conditions) + hash(self.value)
    
    def prune(self) -> Self | None:
        from collections import defaultdict

        grouped_conditions = defaultdict(list)

        # O(n*m), find a better way to filter out contradictions
        for condition in self.conditions:
            if any(condition.contradicts(existing) for existing in grouped_conditions[condition.variable]):
                return None
            grouped_conditions[condition.variable].append(condition)
        
        simplified_conditions = []

        # Putting the pruning logic on the condition object can make future evolutions easier (add new condition type, like contains, etc)
        # But it would incrase the pruning overhead, since we would also need to put the priority logic in the condition object
        for conditions in grouped_conditions.values():
            track_equal_condition = None
            track_not_equal_condition = []
            tack_greater_than_condition = None
            track_less_than_condition = None

            for condition in conditions:
                if isinstance(condition, (EqualsCondition)):
                    track_equal_condition = condition
                    break
                elif isinstance(condition, NotEqualsCondition):
                    track_not_equal_condition.append(condition)
                elif isinstance(condition, (GreaterThanCondition, GreaterThanOrEqualCondition)):
                    if tack_greater_than_condition is None or condition.value > tack_greater_than_condition.value or condition.value == tack_greater_than_condition.value:
                        tack_greater_than_condition = condition
                elif isinstance(condition, (LessThanCondition, LessThanOrEqualCondition)):
                    if track_less_than_condition is None or condition.value < track_less_than_condition.value or condition.value == track_less_than_condition.value:
                        track_less_than_condition = condition
                else:
                    raise TypeError(f"Cannot prune condition of type {type(condition)}")
            
            if track_equal_condition is not None:
                simplified_conditions.append(track_equal_condition)
                continue

            if track_not_equal_condition:
                simplified_conditions.extend(track_not_equal_condition)
            if tack_greater_than_condition:
                simplified_conditions.append(tack_greater_than_condition)
            if track_less_than_condition:
                simplified_conditions.append(track_less_than_condition)

        return self.__class__(
            conditions=frozenset(simplified_conditions),
            value=self.value
        )