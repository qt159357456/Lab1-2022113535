import unittest
from lab1 import build_graph, query_bridge_words, read_file, process_text

class TestQueryBridgeWordsBlackBox(unittest.TestCase):
    """黑盒测试：针对query_bridge_words函数"""
    
    @classmethod
    def setUpClass(cls):
        """创建测试用的图结构"""
        text = read_file("test.txt")
        words = process_text(text)
        cls.graph, cls.nodes = build_graph(words)
    def test_no_bridge_words(self):
        """测试无桥接词情况"""
        result = query_bridge_words(self.graph, self.nodes, "to", "new")
        self.assertIn("No bridge words", result)
        print('pass test1')
    def test_single_bridge_word(self):
        """测试单桥接词情况"""
        result = query_bridge_words(self.graph, self.nodes, "seek", "new")
        self.assertIn("out", result)
        print('pass test2')
    
    def test_word_missing(self):
        """测试其中一个单词不存在的情况"""
        result = query_bridge_words(self.graph, self.nodes, "xyz", "to")
        self.assertIn("No xyz in the graph", result)
        print('pass test3')

    def test_both_words_missing(self):
        """测试两个单词都不存在的情况"""
        result = query_bridge_words(self.graph, self.nodes, "xyz", "abc")
        self.assertIn("No xyz and abc in the graph", result)
        print('pass test4')
    
    def test_more_bridge_word(self):
        """测试多桥接词情况"""
        tmp_graph = self.graph.copy()
        tmp_graph["explore"]["out"] = 1
        result = query_bridge_words(tmp_graph, self.nodes, "explore", "new")
        self.assertIn("strange", result)
        self.assertIn("out", result)
        print('pass test5')
    def test_self_reference(self):
        """自引用节点，有自引用边"""
        tmp_graph = {"only_node": {"only_node": 1}}
        tmp_nodes = ["only_node"]
        result = query_bridge_words(tmp_graph, tmp_nodes, "only_node", "only_node")
        self.assertIn("Self-reference path exists from only_node to itself.", result)
        print('pass test6')
    def test_self_reference_no_path(self):
        """自引用节点，无自引用边"""
        tmp_graph = {"only_node": {}}
        tmp_nodes = ["only_node"]
        result = query_bridge_words(tmp_graph, tmp_nodes, "only_node", "only_node")
        self.assertIn("No bridge words needed for self-reference.", result)
        print('pass test7')

if __name__ == '__main__':
    unittest.main()