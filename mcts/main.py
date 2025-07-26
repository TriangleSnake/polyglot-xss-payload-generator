# main.py

from mcts import mcts, Node
from testbed import testbed

if __name__ == "__main__":
    root = Node()
    best_payload, avg_reward = mcts(root, testbed_func=testbed, iterations=3000, max_len=10)
    print("最佳 XSS polyglot payload：", best_payload)
    print("平均覆蓋 context 數：", avg_reward)
