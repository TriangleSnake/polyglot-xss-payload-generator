from tokens import TOKENS
import testbed
import asyncio

class Node():
    def __init__(self, payload='', parent=None):
        self.parent = parent
        self.payload = payload if parent is None else parent.payload + payload
        self.children = []
        self.visits = 0
        self.score = 0

def expand(node: Node):

    children = TOKENS
    
    for i in ["<script>","<svg","<img"]:
        if i in node.payload:
            children.remove(i)
    node.children = [Node(payload=token, parent=node) for token in children]
    print(f"Expanding: {node.payload} -> {len(node.children)} children")

def select(node: Node) -> Node:
    def uct_value(child: Node, parent_visits: int) -> float:
        if child.visits == 0:
            return float('inf')
        return child.score / child.visits + (2 * (2 * (parent_visits ** 0.5) / child.visits) ** 0.5)
    while node.children:
        node = max(node.children, key=lambda n: uct_value(n, node.visits))
        print(f"Selecting: {node.payload} -> visits={node.visits}, score={node.score}")
    return node

def simulate(node: Node) -> int:
    node.visits += 1
    reward = asyncio.run(testbed.testbed(node.payload))
    print(f"Simulating: {node.payload} -> reward={reward}")
    return reward
def backpropagate(node: Node, reward: int):
    while node:
        node.visits += 1
        node.score += reward
        print(f"Backpropagating: {node} visits={node.visits}, score={node.score}")
        node = node.parent
        

def mcts(iterations: int = 100):
    root = Node()
    for _ in range(iterations):  # Example iterations
        current_node = root
        while current_node.children:
            current_node = select(current_node)
        if current_node.visits > 0:
            expand(current_node)
            current_node = current_node.children[0]
        reward = simulate(current_node)
        backpropagate(current_node, reward)
        # Simulate a random game from the current node
    best_child = max(root.children, key=lambda n: n.score / n.visits if n.visits > 0 else 0)
    return best_child.payload, best_child.score / best_child.visits if best_child.visits > 0 else 0


if __name__ == "__main__":
    best_payload, avg_reward = mcts(iterations=3000)
    print("最佳 XSS polyglot payload：", best_payload)
    print("平均覆蓋 context 數：", avg_reward)