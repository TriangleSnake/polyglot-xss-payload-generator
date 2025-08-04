from module import mcts



if __name__ == "__main__":
    best_payload, avg_reward = mcts()
    print("最佳 XSS polyglot payload：", best_payload)
    print("平均覆蓋 context 數：", avg_reward)