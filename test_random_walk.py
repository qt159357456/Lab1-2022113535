import unittest
import random
from unittest.mock import patch
from lab1 import build_graph, random_walk

class TestRandomWalkWhiteBox(unittest.TestCase):
    """白盒测试：针对random_walk函数"""
    
    @classmethod
    def setUpClass(cls):
        """创建测试用的图结构"""
        # 路径1：空图
        cls.empty_graph = {}
        cls.empty_nodes = []

        # 路径2：单节点无出边
        cls.graph_path2 = {
            "A": {}  # 无出边
        }
        cls.nodes_path2 = list(cls.graph_path2.keys())
        
        # 路径3：单节点有出边，但下一步无出边
        cls.graph_path3 = {
            "A": {"B": 1},
            "B": {}  # 死胡同
        }
        cls.nodes_path3 = list(cls.graph_path3.keys())
        
        # 路径4：带自环的节点
        cls.graph_path4 = {
            "A": {"A": 1},  # 自环
        }
        cls.nodes_path4 = list(cls.graph_path4.keys())

    def test_path1_empty_graph(self):
        """基本路径1: 137-138-155 (空节点列表)"""
        result = random_walk(self.empty_graph, self.empty_nodes)
        self.assertEqual(result, "")
        print('pass path1')

    def test_path2_empty_graph(self):
        """基本路径2: 137-138-140-144-145-155"""
        result = random_walk(self.graph_path2, self.nodes_path2)
        self.assertEqual(result, "A")
        print('pass path2')
    
    def test_path3_single_step_then_dead_end(self):
        """基本路径3: 137-138-140-144-145-147-150-152-144-145-155"""
        # 固定随机选择顺序：A -> B
        with patch('random.choice', side_effect=["A", "B"]):
            result = random_walk(self.graph_path3, self.nodes_path3)
            self.assertEqual(result, "A B")
            print('pass path3')
    
    def test_path4_self_loop_with_repeat(self):
        """基本路径4: 137-138-140-144-145-147-150-152-144-145-147-150-155"""
        # 固定随机选择顺序：A -> A -> A
        with patch('random.choice', side_effect=["A", "A", "A"]):
            result = random_walk(self.graph_path4, self.nodes_path4)
            self.assertEqual(result, "A A")
            print('pass path4')

if __name__ == '__main__':
    unittest.main()