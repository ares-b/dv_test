import pytest
from strategy_tree import (
    StrategyTree, ConditionNode, LeafNode
)
from strategy import Strategy
from conditions import (
    Condition,
    EqualsCondition, NotEqualsCondition,
    GreaterThanCondition, GreaterThanOrEqualCondition,
    LessThanCondition, LessThanOrEqualCondition
)

class TestLeafNode:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.leaf_node = LeafNode(1, 0.5)
    
    def test_leaf_node_constructor(self):
        assert self.leaf_node.id == 1
        assert self.leaf_node.value == 0.5
    
    def test_leaf_node_str(self):
        assert str(self.leaf_node) == "leaf=0.5"

class TestConditionNode:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.condition_node = ConditionNode(
            id=0,
            conditions=[
                EqualsCondition("age", 18),
                NotEqualsCondition("status", "inactive"),
                GreaterThanCondition("score", 90),
                GreaterThanOrEqualCondition("points", 100),
                LessThanCondition("time", 60),
            ],
            true_branch=ConditionNode(
                id=1,
                conditions=[
                    LessThanOrEqualCondition("distance", 5)
                ],
                true_branch=LeafNode(3, 1.0),
                false_branch=LeafNode(4, 2.0)
            ),
            false_branch=LeafNode(2, 3.0)
        )
    
    def test_condition_node_constructor(self):
        assert self.condition_node.id == 0
        assert self.condition_node.conditions == [
            EqualsCondition("age", 18),
            NotEqualsCondition("status", "inactive"),
            GreaterThanCondition("score", 90),
            GreaterThanOrEqualCondition("points", 100),
            LessThanCondition("time", 60),
        ]

        assert type(self.condition_node.true_branch) == ConditionNode
        assert self.condition_node.true_branch.id == 1
        assert self.condition_node.true_branch.conditions == [LessThanOrEqualCondition("distance", 5)]
        assert type(self.condition_node.true_branch.true_branch) == LeafNode
        assert self.condition_node.true_branch.true_branch.id == 3
        assert self.condition_node.true_branch.true_branch.value == 1.0
        assert type(self.condition_node.true_branch.false_branch) == LeafNode
        assert self.condition_node.true_branch.false_branch.id == 4
        assert self.condition_node.true_branch.false_branch.value == 2.0

        assert type(self.condition_node.false_branch) == LeafNode
        assert self.condition_node.false_branch.id == 2 
        assert self.condition_node.false_branch.value == 3.0 
    
    def test_condition_node_str(self):
        
        assert str(self.condition_node) == "[age=18||or||status!=inactive||or||score>90||or||points>=100||or||time<60] yes=1, no=2"

class TestStrategyTree:

    @pytest.fixture(autouse=True)
    def setup(self):
        cond_device_type_pc = EqualsCondition(variable="device_type", value="pc")
        cond_browser_7 = EqualsCondition(variable="browser", value=7)
        cond_os_family_5 = EqualsCondition(variable="os_family", value=5)
        cond_browser_8 = EqualsCondition(variable="browser", value=8)
        cond_language_2 = EqualsCondition(variable="language", value=2)
        cond_size_300x600 = EqualsCondition(variable="size", value="300x600")
        cond_browser_5 = EqualsCondition(variable="browser", value=5)
        cond_position_2 = EqualsCondition(variable="position", value=2)
        cond_region_FR_A5 = EqualsCondition(variable="region", value="FR:A5")

        node_4 = LeafNode(4, 0.000881108)
        node_8 = LeafNode(8, 0.000842268)
        node_10 = LeafNode(10, 0.000625534)
        node_13 = LeafNode(13, 0.000999001)
        node_14 = LeafNode(14, 0.000939982)
        node_15 = LeafNode(15, 0.000708484)
        node_16 = LeafNode(16, 0.00066727)
        node_17 = LeafNode(17, 0.00063461)
        node_18 = LeafNode(18, 0.000597397)
        node_19 = LeafNode(19, 0.000594593)
        node_20 = LeafNode(20, 0.000559453)

        node_12 = ConditionNode(12, [cond_language_2], node_20, node_19)
        node_11 = ConditionNode(11, [cond_size_300x600], node_18, node_17)
        node_9 = ConditionNode(9, [cond_position_2], node_16, node_15)
        node_7 = ConditionNode(7, [cond_region_FR_A5], node_14, node_13)
        node_6 = ConditionNode(6, [cond_browser_8], node_12, node_11)
        node_5 = ConditionNode(5, [cond_browser_8, cond_browser_5], node_10, node_9)
        node_3 = ConditionNode(3, [cond_os_family_5], node_8, node_7)
        node_2 = ConditionNode(2, [cond_os_family_5], node_6, node_5)
        node_1 = ConditionNode(1, [cond_browser_8], node_4, node_3)
        node_0 = ConditionNode(0, [cond_device_type_pc, cond_browser_7], node_2, node_1)

        self.strategy_tree = StrategyTree(
            root=node_0
        )
    
    def test_strategy_tree_constructor(self):
        assert self.strategy_tree.root.id == 0
        assert self.strategy_tree.root.conditions == [
            EqualsCondition(variable="device_type", value="pc"),
            EqualsCondition(variable="browser", value=7)
        ]
    
    def test_strategy_tree_get_strategies(self):
        assert str(self.strategy_tree) == "0:[device_type=pc||or||browser=7] yes=2, no=1\n\t2:[os_family=5] yes=6, no=5\n\t\t6:[browser=8] yes=12, no=11\n\t\t\t12:[language=2] yes=20, no=19\n\t\t\t\t20:leaf=0.000559453\n\t\t\t\t19:leaf=0.000594593\n\t\t\t11:[size=300x600] yes=18, no=17\n\t\t\t\t18:leaf=0.000597397\n\t\t\t\t17:leaf=0.00063461\n\t\t5:[browser=8||or||browser=5] yes=10, no=9\n\t\t\t10:leaf=0.000625534\n\t\t\t9:[position=2] yes=16, no=15\n\t\t\t\t16:leaf=0.00066727\n\t\t\t\t15:leaf=0.000708484\n\t1:[browser=8] yes=4, no=3\n\t\t4:leaf=0.000881108\n\t\t3:[os_family=5] yes=8, no=7\n\t\t\t8:leaf=0.000842268\n\t\t\t7:[region=FR:A5] yes=14, no=13\n\t\t\t\t14:leaf=0.000939982\n\t\t\t\t13:leaf=0.000999001"
    
    def test_strategy_tree_from_string(self):
        content = """0:[device_type=pc||or||browser=7] yes=2,no=1
            2:[os_family=5] yes=6,no=5
                6:[browser=8] yes=12,no=11
                    12:[language=2] yes=20,no=19
                        20:leaf=0.000559453
                        19:leaf=0.000594593
                    11:[size=300x600] yes=18,no=17
                        18:leaf=0.000597397
                        17:leaf=0.00063461
                5:[browser=8||or||browser=5] yes=10,no=9
                    10:leaf=0.000625534
                    9:[position=2] yes=16,no=15
                        16:leaf=0.00066727
                        15:leaf=0.000708484
            1:[browser=8] yes=4,no=3
                4:leaf=0.000881108
                3:[os_family=5] yes=8,no=7
                    8:leaf=0.000842268
                    7:[region=FR:A5] yes=14,no=13
                        14:leaf=0.000939982
                        13:leaf=0.000999001
        """
        assert StrategyTree.from_string(content) == self.strategy_tree
    
    def test_strategy_tree_from_file(self, resources_path):
        from os import path
        
        assert StrategyTree.from_file(path.join(resources_path, "tree_to_convert__288_29.txt")) == self.strategy_tree
    
    def test_simple_tree(self, resources_path):
        from os import path
        
        tree = StrategyTree.from_file(path.join(resources_path, "simple_tree.txt"))
        tree_strategies = tree.get_strategies()

        strategies = [
            Strategy(
                conditions=[EqualsCondition("browser", 8)],
                value=10
            ),
            Strategy(
                conditions=[EqualsCondition("browser", 7)],
                value=30
            ),
            Strategy(
                conditions=[NotEqualsCondition("browser", 8), NotEqualsCondition("device_type", "pc")],
                value=20
            ),
            Strategy(
                conditions=[EqualsCondition("browser", 8), NotEqualsCondition("device_type", "pc")],
                value=10
            ),
            Strategy(
                conditions=[EqualsCondition("device_type", "pc")],
                value=30
            ),
        ]
        assert tree_strategies == strategies
        