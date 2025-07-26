# module.py

import math
import random
import copy
from tokens import TOKENS

class Node:
    def __init__(self, tokens=None, parent=None):
        self.tokens = tokens or []
        self.parent = parent
        self.children = []
        self.visits = 0
        self.total_reward = 0.0

    def is_terminal(self, max_len=10):
        return len(self.tokens) >= max_len

    def expand(self):
        tried = {tuple(child.tokens) for child in self.children}
        untried = []
        for tok in TOKENS:
            new_seq = self.tokens + [tok]
            if tuple(new_seq) not in tried:
                untried.append(tok)
        if not untried:
            return None
        action = random.choice(untried)
        child = Node(self.tokens + [action], parent=self)
        self.children.append(child)
        return child

    def score(self, c=1.41):
        if self.visits == 0:
            return float('inf')
        return (self.total_reward / self.visits) + c * math.sqrt(math.log(self.parent.visits) / self.visits)

def select(node: Node) -> Node: 
    current = node
    while current.children:
        current = max(current.children, key=lambda n: n.score())
    return current

def expand(node: Node) -> Node: 
    if node.is_terminal():
        return node
    return node.expand() or node

def simulate(node: Node, testbed_func, max_len=10) -> int:
    tokens = copy.deepcopy(node.tokens)
    while len(tokens) < max_len:
        tokens.append(random.choice(TOKENS))
        if random.random() < 0.2:
            break
    payload = ''.join(tokens)
    return testbed_func(payload)

def backpropagate(node: Node, reward):
    while node:
        node.visits += 1
        node.total_reward += reward
        node = node.parent

def mcts(root: Node, testbed_func, iterations=1000, max_len=10):
    for _ in range(iterations):
        leaf = select(root)
        child = expand(leaf)
        reward = simulate(child, testbed_func, max_len)
        backpropagate(child, reward)
    # 回傳 reward 最高的第一層子節點
    if not root.children:
        return '', 0
    best = max(root.children, key=lambda n: n.total_reward / (n.visits or 1))
    return ''.join(best.tokens), best.total_reward / (best.visits or 1)
