import re
import sys
import random
import heapq
from collections import defaultdict
def showDirectedGraph(graph):
    """以文本形式展示有向图结构"""
    print("\nDirected Graph Structure:")
    # 按字母顺序排序节点
    sorted_nodes = sorted(graph.keys())
    for node in sorted_nodes:
        # 获取当前节点的所有邻接节点
        neighbors = graph[node]
        if not neighbors:
            print(f"{node} -> (no outgoing edges)")
            continue
        # 按字母顺序排序邻接节点
        sorted_neighbors = sorted(neighbors.items(), key=lambda x: x[0])
        # 格式化输出: 邻接节点(权重)
        neighbor_str = ", ".join([f"{n}({w})" for n, w in sorted_neighbors])
        print(f"{node} -> {neighbor_str}")
def process_text(text):
    text = re.sub(r'[^a-zA-Z]', ' ', text).lower()
    words = text.split()
    return words

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def build_graph(words):
    graph = defaultdict(lambda: defaultdict(int))
    for i in range(len(words) - 1):
        current = words[i]
        next_word = words[i+1]
        graph[current][next_word] += 1
    nodes = sorted(set(words))
    return {k: dict(v) for k, v in graph.items()},nodes

def query_bridge_words(graph, nodes, word1, word2):
    word1, word2 = word1.lower(), word2.lower()
    if word1 not in nodes or word2 not in nodes:
        if word1 not in nodes and word2 not in nodes:
            return f"No {word1} and {word2} in the graph!"
        elif word1 not in nodes:
            return f"No {word1} in the graph!"
        else:
            return f"No {word2} in the graph!"
    bridge = []
    # print(graph.get(word1, {}))
    for candidate in graph.get(word1, {}):
        if word2 in graph.get(candidate, {}):
            bridge.append(candidate)
    if not bridge:
        return f"No bridge words from {word1} to {word2}!"
    elif len(bridge) == 1:
        return f"The bridge words from {word1} to {word2} is: {bridge[0]}."
    else:
        return f"The bridge words from {word1} to {word2} are: {', '.join(bridge[:-1])} and {bridge[-1]}."

def generate_new_text(graph, input_text):
    words = process_text(input_text)
    new_words = []
    for i in range(len(words)):
        new_words.append(words[i])
        if i < len(words) - 1:
            current = words[i].lower()
            next_word = words[i+1].lower()
            candidates = []
            if current in graph:
                for candidate in graph[current]:
                    if next_word in graph.get(candidate, {}):
                        candidates.append(candidate)
            if candidates:
                new_words.append(random.choice(candidates))
    return ' '.join(new_words)

def dijkstra(graph, nodes, start, end):
    # nodes = list(graph.keys())
    dist = {n: float('inf') for n in nodes}
    prev = {n: None for n in nodes}
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if u == end:
            break
        if d > dist[u]:
            continue
        if u not in graph:
            continue
        for v, w in graph[u].items():
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))
    path = []
    u = end
    while prev.get(u) is not None:
        path.append(u)
        u = prev[u]
    path.append(start)
    if path[0] == start:
        return [], float('inf')
    path.reverse()
    return path, dist.get(end, float('inf'))

def calc_shortest_path(graph, nodes,word1, word2):
    word1, word2 = word1.lower(), word2.lower()
    if word1 not in nodes or word2 not in nodes:
        return f"One or both words not in graph."
    path, dist = dijkstra(graph, nodes,word1, word2)
    if not path:
        return f"No path from {word1} to {word2}."
    return f"Shortest path: {' → '.join(path)} (length {dist})"

def calculate_pagerank(graph, nodes, d=0.85, max_iter=100, tol=1e-6):
    # nodes = list(graph.keys())
    n = len(nodes)
    pr = {node: 1/n for node in nodes}
    for _ in range(max_iter):
        new_pr = {}
        dangling_sum = sum(pr[node] for node in nodes if not graph.get(node))
        for node in nodes:
            incoming = sum(pr[p]/len(graph[p]) for p in nodes if p in graph and node in graph[p])
            random_jump = (1 - d) / n
            new_pr[node] = random_jump + d * (incoming + dangling_sum / n)
        delta = sum(abs(new_pr[node] - pr[node]) for node in nodes)
        pr = new_pr
        if delta < tol:
            break
    return pr

def random_walk(graph,nodes):
    if not nodes:
        return ""
    start = random.choice(nodes)
    path = [start]
    visited_edges = set()
    current = start
    while True:
        if current not in graph or not graph[current]:
            break
        neighbors = list(graph[current].keys())
        next_node = random.choice(neighbors)
        edge = (current, next_node)
        if edge in visited_edges:
            break
        visited_edges.add(edge)
        path.append(next_node)
        current = next_node
    return ' '.join(path)

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        text = read_file(filename)
        words = process_text(text)
        graph,nodes = build_graph(words)
        showDirectedGraph(graph)
    while True:
        print("\n1. Read file\n2. Show graph\n3. Query bridge words\n4. Generate new text\n5. Shortest path\n6. PageRank\n7. Random walk\n8. Exit")
        choice = input("Choose: ")
        if choice == '1':
            filename = input("Enter filename: ")
            text = read_file(filename)
            words = process_text(text)
            graph,nodes = build_graph(words)
        elif choice == '2':
            showDirectedGraph(graph)
        elif choice == '3':
            w1 = input("Word1: ")
            w2 = input("Word2: ")
            print(query_bridge_words(graph, nodes, w1, w2))
        elif choice == '4':
            text = input("Enter text: ")
            print("New text:", generate_new_text(graph, text))
        elif choice == '5':
            w1 = input("From: ")
            w2 = input("To: ")
            print(calc_shortest_path(graph, nodes,w1, w2))
        elif choice == '6':
            pr = calculate_pagerank(graph, nodes)
            x = 0
            for word, score in sorted(pr.items(), key=lambda x: -x[1]):
                x+=score
                print(f"{word}: {score:.4f}")
            print("Sum of PageRank scores:", x)
        elif choice == '7':
            walk = random_walk(graph, nodes)
            print("Walk:", walk)
            with open('walk.txt', 'w') as f:
                f.write(walk)
        elif choice == '8':
            break

if __name__ == "__main__":
    main()