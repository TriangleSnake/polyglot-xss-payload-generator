from tokens import TOKENS
import testbed
import asyncio
import random
import math

class Node():
    def __init__(self,payload: dict = {}, parent=None):
        self.parent = parent
        self.payload = payload
        if self.payload == {}:
            self.payload["type"] = "trigger_exploits"
            self.payload["data"] = random.choice(TOKENS["sets"][self.payload["type"]])
        else :
            self.payload["data"] = parent.payload["data"] + self.payload["data"]
        self.children = []
        self.visits = 0
        self.score = 0

def expand(node: Node):

    next_type = TOKENS["trans"][node.payload["type"]]
    if next_type == []:
        next_type = list(TOKENS["sets"])

    node.children = []
    for i in next_type:
        for j in TOKENS["sets"][i]:
            node.children.append(Node(payload={"type": i, "data": j}, parent=node))

    print(f"Expanding: {node.payload} -> {len(node.children)} children")

def select(node: Node) -> Node:
    def uct_value(child: Node, parent_visits: int, c: float = 1.5) -> float:
        if child.visits == 0:
            return float('inf')                 
        exploit = child.score / child.visits
        explore = c * math.sqrt(math.log(parent_visits) / child.visits)
        return exploit + explore
    while node.children:
        node = max(node.children, key=lambda n: uct_value(n, node.visits))
        print(f"Selecting: {node.payload} -> visits={node.visits}, uct_value={uct_value(node, node.parent.visits)}")
    return node

def simulate(node: Node) -> int:
    global best_payload
    def _choose_random_token(payload: dict) -> str:
        cpayload = payload.copy()
        while len(cpayload["data"]) < 40:
            type_lst = list(TOKENS["trans"][cpayload["type"]])
            if type_lst == []:
                type_lst = list(TOKENS["sets"])
            cpayload["type"] = random.choice(type_lst)
            cpayload["data"] += random.choice(TOKENS["sets"][cpayload["type"]])
        return cpayload

    node.visits += 1
    
    #reward = asyncio.run(testbed.testbed(node.payload))
    if random.random() < 0.5:
        print("Cut!")
        payload = node.payload
    else:
        print("Fill random token")
        payload = _choose_random_token(node.payload)
    print(f"Simulating payload: {payload}",end=' ')
    reward = asyncio.run(testbed.local_testbed(payload["data"]))
    if reward > best_payload["score"]:
        best_payload["node"] = node
        best_payload["score"] = reward
        print(f"-> New best payload: {node.payload["data"]} with score={reward}")
    print(f"-> reward={reward}")
    return reward
def backpropagate(node: Node, reward: int):
    while node:
        node.visits += 1
        node.score += reward
        print(f"Backpropagating: {node} visits={node.visits}, score={node.score}")
        node = node.parent
        

def mcts(iterations: int = 100):
    root = Node()
    global best_payload
    best_payload = {"node": root, "score": 0}
    for _ in range(iterations):  # Example iterations
        print(f"Iteration {_+1}/{iterations}")
        current_node = root
        while current_node.children:
            current_node = select(current_node)
        if current_node.visits > 0:
            expand(current_node)
            current_node = current_node.children[0]
        reward = simulate(current_node)
        backpropagate(current_node, reward)
        # Simulate a random game from the current node
    return best_payload["node"].payload, best_payload["score"]