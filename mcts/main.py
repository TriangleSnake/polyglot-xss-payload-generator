from module import mcts

ITERATIONS = 1000
C = 1.1

if __name__ == "__main__":
    best_payload, avg_reward = mcts(ITERATIONS)
    print("最佳 XSS polyglot payload：", best_payload)
    print("平均覆蓋 context 數：", avg_reward)