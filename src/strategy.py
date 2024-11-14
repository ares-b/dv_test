from dataclasses import dataclass
from conditions import (
    Condition,
    EqualsCondition, NotEqualsCondition,
    GreaterThanOrEqualCondition, GreaterThanCondition,
    LessThanOrEqualCondition, LessThanCondition
)
from typing import List, Union

@dataclass
class Strategy:
    conditions: List[Condition]
    value: float

    def __str__(self):
        conditions=" && ".join([str(st) for st in self.conditions])
        return f"if ({conditions}) then {self.value}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Strategy):
            return False
        
        if self.value != other.value or len(self.conditions) != len(other.conditions):
            return False
        
        for self_cond in self.conditions:
            found = False
            for other_cond in other.conditions:
                if other_cond == self_cond:
                    found = True
            if not found:
                return False
        return True

    def prune(self) -> Union["Strategy", None]:
        from collections import defaultdict

        grouped_conditions = defaultdict(list)

        # TODO: O², find a better way to filter out contradictions
        for condition in self.conditions:
            if any(condition.contradicts(existing) for existing in grouped_conditions[condition.variable]):
                return None
            grouped_conditions[condition.variable].append(condition)
        
        simplified_conditions = []

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
                    if tack_greater_than_condition is None or condition.value > tack_greater_than_condition.value or (
                        isinstance(condition, GreaterThanOrEqualCondition) and
                        isinstance(tack_greater_than_condition, GreaterThanCondition) and
                        condition.value == tack_greater_than_condition.value
                    ):
                        tack_greater_than_condition = condition
                elif isinstance(condition, (LessThanCondition, LessThanOrEqualCondition)):
                    if track_less_than_condition is None or condition.value < track_less_than_condition.value or (
                        isinstance(condition, LessThanOrEqualCondition) and
                        isinstance(track_less_than_condition, LessThanCondition) and
                        condition.value == track_less_than_condition.value
                    ):
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
            conditions=simplified_conditions,
            value=self.value
        )