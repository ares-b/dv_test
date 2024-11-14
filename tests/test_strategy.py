import pytest
from conditions import (
    EqualsCondition, NotEqualsCondition,
    GreaterThanCondition, GreaterThanOrEqualCondition,
    LessThanCondition, LessThanOrEqualCondition
)
from strategy import Strategy

class TestStrategy:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.strategy = Strategy(
            conditions=[
                EqualsCondition("age", 18),
                NotEqualsCondition("status", "inactive"),
                GreaterThanCondition("score", 90),
                GreaterThanOrEqualCondition("points", 100),
                LessThanCondition("time", 60),
                LessThanOrEqualCondition("distance", 5)
            ],
            value=0.5
        )
    
    def test_strategy_constructor(self):
        assert self.strategy.value == 0.5
        assert self.strategy.conditions == [
            EqualsCondition("age", 18),
            NotEqualsCondition("status", "inactive"),
            GreaterThanCondition("score", 90),
            GreaterThanOrEqualCondition("points", 100),
            LessThanCondition("time", 60),
            LessThanOrEqualCondition("distance", 5)
        ]
    
    def test_strategy_prune(self):
        assert Strategy(
            conditions=[
                EqualsCondition("age", 18),
                NotEqualsCondition("age", 17),
                NotEqualsCondition("status", "inactive"),
                GreaterThanCondition("score", 90),
                GreaterThanOrEqualCondition("points", 100),
                LessThanCondition("time", 60),
                LessThanOrEqualCondition("distance", 5)
            ],
            value=0.5
        ).prune() == Strategy(
            conditions=[
                EqualsCondition("age", 18),
                NotEqualsCondition("status", "inactive"),
                GreaterThanCondition("score", 90),
                GreaterThanOrEqualCondition("points", 100),
                LessThanCondition("time", 60),
                LessThanOrEqualCondition("distance", 5)
            ],
            value=0.5
        )

        assert str(Strategy(
            conditions=[
                EqualsCondition("age", 18),
                NotEqualsCondition("age", 17),
                NotEqualsCondition("status", "inactive"),
                GreaterThanCondition("score", 90),
                GreaterThanOrEqualCondition("score", 100),
                LessThanCondition("time", 60),
                LessThanOrEqualCondition("time", 50),
            ],
            value=0.5
        ).prune()) == str(Strategy(
            conditions=[
                EqualsCondition("age", 18),
                NotEqualsCondition("status", "inactive"),
                GreaterThanOrEqualCondition("score", 100),
                LessThanOrEqualCondition("time", 50),
            ],
            value=0.5
        ))

        assert Strategy(
            conditions=[
                GreaterThanCondition("price", 100),
                LessThanCondition("price", 90)
            ],
            value=0.5
        ).prune() is None

        assert Strategy(
            conditions=[
                GreaterThanCondition("value", 50),
                GreaterThanOrEqualCondition("value", 60),
                EqualsCondition("type", "premium"),
                LessThanOrEqualCondition("weight", 100),
                LessThanCondition("weight", 150),
            ],
            value=1.0
        ).prune() == Strategy(
            conditions=[
                GreaterThanOrEqualCondition("value", 60),
                EqualsCondition("type", "premium"),
                LessThanOrEqualCondition("weight", 100),
            ],
            value=1.0
        )

        assert Strategy(
            conditions=[
                NotEqualsCondition("category", "electronics"),
                NotEqualsCondition("category", "furniture"),
                EqualsCondition("status", "active"),
            ],
            value=1.0
        ).prune() == Strategy(
            conditions=[
                NotEqualsCondition("category", "electronics"),
                NotEqualsCondition("category", "furniture"),
                EqualsCondition("status", "active"),
            ],
            value=1.0
        )

        assert Strategy(
            conditions=[
                GreaterThanOrEqualCondition("rating", 4),
                LessThanCondition("rating", 3),
                EqualsCondition("status", "approved")
            ],
            value=1.0
        ).prune() is None

        assert Strategy(
            conditions=[
                GreaterThanCondition("temperature", 0),
                GreaterThanOrEqualCondition("temperature", 10),
                LessThanCondition("temperature", 50),
                LessThanOrEqualCondition("temperature", 45),
            ],
            value=0.75
        ).prune() == Strategy(
            conditions=[
                GreaterThanOrEqualCondition("temperature", 10),
                LessThanOrEqualCondition("temperature", 45),
            ],
            value=0.75
        )
    
    def test_strategy_str(self):
        assert str(self.strategy) == "if (age=18 && status!=inactive && score>90 && points>=100 && time<60 && distance<=5) then 0.5"

