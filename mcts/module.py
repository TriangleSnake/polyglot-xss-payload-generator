from tokens import TOKENS
import testbed
import asyncio
import random
import math
from config import *

class Node():
    def __init__(self,payload: dict = {}, parent=None):
        self.parent = parent
        self.payload = payload
        if self.payload == {}:
            self.payload["type"] = "inline"
            self.payload["data"] = "jAvAsCriPt:"
        else :
            self.payload["data"] = parent.payload["data"] + self.payload["data"]
        self.reward = 0
        self.children = []
        self.visits = 0
        self.score = 0

def expand(node: Node):
    if node.children != []:
        return
    next_type = TOKENS["trans"][node.payload["type"]]
    if next_type == []:
        next_type = list(TOKENS["sets"])

    node.children = []
    for i in next_type:
        for j in TOKENS["sets"][i]:
            node.children.append(Node(payload={"type": i, "data": j}, parent=node))

    #print(f"Expanding: {node.payload} -> {len(node.children)} children")

def select(node: Node) -> Node:
    def uct_value(child: Node, parent_visits: int) -> float:
        global C
        if child.visits == 0:
            return float('inf')                 
        exploit = child.reward / child.visits
        explore = C * math.sqrt(2*math.log(parent_visits) / child.visits)
        return exploit + explore
    while node.children:
        node = max(node.children, key=lambda n: uct_value(n, node.visits))
        #print(f"Selecting: {node.payload} -> visits={node.visits}, uct_value={uct_value(node, node.parent.visits)}")
    return node

def simulate(node: Node,root: Node) -> int:
    global best_payload
    def _choose_random_token(payload: dict) -> str:
        cpayload = payload.copy()
        while len(cpayload["data"]) < MAX_DEPTH*5:
            type_lst = list(TOKENS["trans"][cpayload["type"]])
            if type_lst == []:
                type_lst = list(TOKENS["sets"])
            cpayload["type"] = random.choice(type_lst)
            cpayload["data"] += random.choice(TOKENS["sets"][cpayload["type"]])
        return cpayload

    node.visits += 1
    
    #reward = asyncio.run(testbed.testbed(node.payload))
    if random.random() < .2:
        payload = node.payload
    else:
        payload = _choose_random_token(node.payload)
    print(f"Simulating payload: {payload}",end='')
    score = asyncio.run(testbed.local_testbed(payload["data"]))
    print(score,root.score)
    score = max(0,score-root.score)
    print(f"-> score={score}")
    return payload,score
def backpropagate(node: Node, reward: int):
    while node:
        node.visits += 1
        node.reward += reward
        #print(f"Backpropagating: {node} visits={node.visits}, score={round(node.score,2)}, reward={round(node.score/node.visits,2)}")
        node = node.parent

def choose_best(node: Node) -> Node:
    if not node.children:
        return node
    best_child = max(node.children, key=lambda n: n.reward/n.visits)
    print(f"Choosing best child: {best_child.payload} with score={best_child.reward/best_child.visits}")
    return best_child

def mcts() -> tuple:
    root = Node()
    for _ in range(MAX_DEPTH):
        best_reward = 0
        root.score = asyncio.run(testbed.local_testbed(root.payload["data"]))
        for __ in range(ITERATIONS):  # Example iterations
            print(f"Iteration {__+1}/{ITERATIONS}")
            leaf = select(root)
            expand(leaf)
            polyglot, score = simulate(leaf,root)
            backpropagate(leaf, score)
            if leaf.reward > best_reward:
                best_reward, best_polyglot = leaf.reward, polyglot
            # Simulate a random game from the current node
        root = choose_best(root)
    return best_reward, best_polyglot