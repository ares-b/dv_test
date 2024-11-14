import pytest
from conditions import (
    EqualsCondition, NotEqualsCondition,
    GreaterThanCondition, GreaterThanOrEqualCondition,
    LessThanCondition, LessThanOrEqualCondition
)

class TestEqualsCondition:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.condition = EqualsCondition("test", 50)
    
    def test_condition_constructor(self):
        assert self.condition.variable == "test"
        assert self.condition.value == 50
        assert self.condition.operator == "="
    
    def test_condition_eq(self):
        assert self.condition == EqualsCondition("test", 50)
    
    def test_condition_negate(self):
        assert self.condition.negate() == NotEqualsCondition("test", 50)
    
    def test_condition_contradicts(self):
        assert self.condition.contradicts(EqualsCondition("test", 20))
        assert self.condition.contradicts(NotEqualsCondition("test", 50))

        assert not self.condition.contradicts(GreaterThanCondition("test", 40))
        assert self.condition.contradicts(GreaterThanCondition("test", 50))
        assert self.condition.contradicts(GreaterThanCondition("test", 60))

        assert not self.condition.contradicts(GreaterThanOrEqualCondition("test", 40))
        assert not self.condition.contradicts(GreaterThanOrEqualCondition("test", 50))
        assert self.condition.contradicts(GreaterThanOrEqualCondition("test", 60))

        assert self.condition.contradicts(LessThanCondition("test", 40))
        assert self.condition.contradicts(LessThanCondition("test", 50))
        assert not self.condition.contradicts(LessThanCondition("test", 60))

        assert self.condition.contradicts(LessThanOrEqualCondition("test", 40))
        assert not self.condition.contradicts(LessThanOrEqualCondition("test", 50))
        assert not self.condition.contradicts(LessThanOrEqualCondition("test", 60))

    def test_condition_str(self):
        assert str(self.condition) == "test=50"

class TestNotEqualsCondition:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.condition = NotEqualsCondition("test", 50)
    
    def test_condition_constructor(self):
        assert self.condition.variable == "test"
        assert self.condition.value == 50
        assert self.condition.operator == "!="
    
    def test_condition_eq(self):
        assert self.condition == NotEqualsCondition("test", 50)
    
    def test_condition_negate(self):
        assert self.condition.negate() == EqualsCondition("test", 50)
    
    def test_condition_contradicts(self):
        assert self.condition.contradicts(NotEqualsCondition("test", 20))
        assert self.condition.contradicts(EqualsCondition("test", 50))

        assert not self.condition.contradicts(GreaterThanCondition("test", 40))
        assert not self.condition.contradicts(GreaterThanCondition("test", 50))
        assert not self.condition.contradicts(GreaterThanCondition("test", 60))

        assert not self.condition.contradicts(GreaterThanOrEqualCondition("test", 40))
        assert not self.condition.contradicts(GreaterThanOrEqualCondition("test", 50))
        assert not self.condition.contradicts(GreaterThanOrEqualCondition("test", 60))

        assert not self.condition.contradicts(LessThanCondition("test", 40))
        assert not self.condition.contradicts(LessThanCondition("test", 50))
        assert not self.condition.contradicts(LessThanCondition("test", 60))

        assert not self.condition.contradicts(LessThanOrEqualCondition("test", 40))
        assert not self.condition.contradicts(LessThanOrEqualCondition("test", 50))
        assert not self.condition.contradicts(LessThanOrEqualCondition("test", 60))
    
    def test_condition_str(self):
        assert str(self.condition) == "test!=50"

class TestGreaterThanCondition:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.condition = GreaterThanCondition("test", 50)
    
    def test_condition_constructor(self):
        assert self.condition.variable == "test"
        assert self.condition.value == 50
        assert self.condition.operator == ">"
    
    def test_condition_eq(self):
        assert self.condition == GreaterThanCondition("test", 50)
    
    def test_condition_negate(self):
        assert self.condition.negate() == LessThanOrEqualCondition("test", 50)
    
    def test_condition_contradicts(self):
        assert self.condition.contradicts(EqualsCondition("test", 20))
        assert self.condition.contradicts(EqualsCondition("test", 50))
        assert not self.condition.contradicts(NotEqualsCondition("test", 20))

        assert not self.condition.contradicts(GreaterThanCondition("test", 40))
        assert not self.condition.contradicts(GreaterThanCondition("test", 50))
        assert not self.condition.contradicts(GreaterThanCondition("test", 60))

        assert not self.condition.contradicts(GreaterThanOrEqualCondition("test", 40))
        assert not self.condition.contradicts(GreaterThanOrEqualCondition("test", 50))
        assert not self.condition.contradicts(GreaterThanOrEqualCondition("test", 60))

        assert self.condition.contradicts(LessThanCondition("test", 40))
        assert self.condition.contradicts(LessThanCondition("test", 50))
        assert not self.condition.contradicts(LessThanCondition("test", 60))

        assert self.condition.contradicts(LessThanOrEqualCondition("test", 40))
        assert self.condition.contradicts(LessThanOrEqualCondition("test", 50))
        assert not self.condition.contradicts(LessThanOrEqualCondition("test", 60))

    def test_condition_str(self):
        assert str(self.condition) == "test>50"

class TestGreaterThanOrEqualCondition:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.condition = GreaterThanOrEqualCondition("test", 50)
    
    def test_condition_constructor(self):
        assert self.condition.variable == "test"
        assert self.condition.value == 50
        assert self.condition.operator == ">="
    
    def test_condition_eq(self):
        assert self.condition == GreaterThanOrEqualCondition("test", 50)
    
    def test_condition_negate(self):
        assert self.condition.negate() == LessThanCondition("test", 50)
    
    def test_condition_contradicts(self):
        assert self.condition.contradicts(EqualsCondition("test", 20))
        assert not self.condition.contradicts(EqualsCondition("test", 50))
        assert not self.condition.contradicts(NotEqualsCondition("test", 20))

        assert not self.condition.contradicts(GreaterThanCondition("test", 40))
        assert not self.condition.contradicts(GreaterThanCondition("test", 50))
        assert not self.condition.contradicts(GreaterThanCondition("test", 60))

        assert not self.condition.contradicts(GreaterThanOrEqualCondition("test", 40))
        assert not self.condition.contradicts(GreaterThanOrEqualCondition("test", 50))
        assert not self.condition.contradicts(GreaterThanOrEqualCondition("test", 60))

        assert self.condition.contradicts(LessThanCondition("test", 40))
        assert not self.condition.contradicts(LessThanCondition("test", 50))
        assert not self.condition.contradicts(LessThanCondition("test", 60))

        assert self.condition.contradicts(LessThanOrEqualCondition("test", 40))
        assert not self.condition.contradicts(LessThanOrEqualCondition("test", 50))
        assert not self.condition.contradicts(LessThanOrEqualCondition("test", 60))
    
    def test_condition_str(self):
        assert str(self.condition) == "test>=50"

class TestLessThanCondition:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.condition = LessThanCondition("test", 50)
    
    def test_condition_constructor(self):
        assert self.condition.variable == "test"
        assert self.condition.value == 50
        assert self.condition.operator == "<"
    
    def test_condition_eq(self):
        assert self.condition == LessThanCondition("test", 50)
    
    def test_condition_negate(self):
        assert self.condition.negate() == GreaterThanOrEqualCondition("test", 50)
    
    def test_condition_contradicts(self):
        assert not self.condition.contradicts(EqualsCondition("test", 20))
        assert self.condition.contradicts(EqualsCondition("test", 50))
        assert not self.condition.contradicts(NotEqualsCondition("test", 20))

        assert not self.condition.contradicts(GreaterThanCondition("test", 40))
        assert self.condition.contradicts(GreaterThanCondition("test", 50))
        assert self.condition.contradicts(GreaterThanCondition("test", 60))

        assert not self.condition.contradicts(GreaterThanOrEqualCondition("test", 40))
        assert self.condition.contradicts(GreaterThanOrEqualCondition("test", 50))
        assert self.condition.contradicts(GreaterThanOrEqualCondition("test", 60))

        assert not self.condition.contradicts(LessThanCondition("test", 40))
        assert not self.condition.contradicts(LessThanCondition("test", 50))
        assert not self.condition.contradicts(LessThanCondition("test", 60))

        assert not self.condition.contradicts(LessThanOrEqualCondition("test", 40))
        assert not self.condition.contradicts(LessThanOrEqualCondition("test", 50))
        assert not self.condition.contradicts(LessThanOrEqualCondition("test", 60))
        
    def test_condition_str(self):
        assert str(self.condition) == "test<50"

class TestLessThanOrEqualCondition:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.condition = LessThanOrEqualCondition("test", 50)
    
    def test_condition_constructor(self):
        assert self.condition.variable == "test"
        assert self.condition.value == 50
        assert self.condition.operator == "<="
    
    def test_condition_eq(self):
        assert self.condition == LessThanOrEqualCondition("test", 50)
    
    def test_condition_negate(self):
        assert self.condition.negate() == GreaterThanCondition("test", 50)
    
    def test_condition_contradicts(self):
        assert not self.condition.contradicts(EqualsCondition("test", 20))
        assert not self.condition.contradicts(EqualsCondition("test", 50))
        assert not self.condition.contradicts(NotEqualsCondition("test", 20))

        assert not self.condition.contradicts(GreaterThanCondition("test", 40))
        assert self.condition.contradicts(GreaterThanCondition("test", 50))
        assert self.condition.contradicts(GreaterThanCondition("test", 60))

        assert not self.condition.contradicts(GreaterThanOrEqualCondition("test", 40))
        assert not self.condition.contradicts(GreaterThanOrEqualCondition("test", 50))
        assert self.condition.contradicts(GreaterThanOrEqualCondition("test", 60))

        assert not self.condition.contradicts(LessThanCondition("test", 40))
        assert not self.condition.contradicts(LessThanCondition("test", 50))
        assert not self.condition.contradicts(LessThanCondition("test", 60))

        assert not self.condition.contradicts(LessThanOrEqualCondition("test", 40))
        assert not self.condition.contradicts(LessThanOrEqualCondition("test", 50))
        assert not self.condition.contradicts(LessThanOrEqualCondition("test", 60))
    
    def test_condition_str(self):
        assert str(self.condition) == "test<=50"
