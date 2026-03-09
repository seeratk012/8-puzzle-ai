import time
from solver import astar, bfs, is_solvable

initial_board = [
    [8,6,7],
    [2,5,4],
    [3,0,1]
]

if not is_solvable(initial_board):
    print("Not solvable")
else:
    print("Running A*...")
    start = time.time()
    sol_astar, nodes_astar = astar(initial_board)
    end = time.time()
    time_astar = end - start

    print("Running BFS...")
    start = time.time()
    sol_bfs, nodes_bfs = bfs(initial_board)
    end = time.time()
    time_bfs = end - start

    print("\n--- Comparison ---")
    print("Algorithm | Moves | Nodes Explored | Time (sec)")
    print("A*        |", len(sol_astar), "|", nodes_astar, "|", round(time_astar,4))
    print("BFS       |", len(sol_bfs), "|", nodes_bfs, "|", round(time_bfs,4))
