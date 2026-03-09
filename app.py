from flask import Flask, render_template, request, jsonify
from collections import deque
import heapq

app = Flask(__name__)

# -------------------------
# 8-PUZZLE SOLVER (A* + BFS)
# -------------------------

GOAL_STATE = (1,2,3,4,5,6,7,8,0)

MOVES = {
    "up": -3,
    "down": 3,
    "left": -1,
    "right": 1
}

def manhattan(state):
    distance = 0
    for i in range(9):
        if state[i] == 0:
            continue
        correct_pos = state[i] - 1
        distance += abs(i//3 - correct_pos//3) + abs(i%3 - correct_pos%3)
    return distance

def get_neighbors(state):
    neighbors = []
    zero_index = state.index(0)
    row, col = zero_index // 3, zero_index % 3

    for move, delta in MOVES.items():
        new_index = zero_index + delta

        if move == "up" and row == 0:
            continue
        if move == "down" and row == 2:
            continue
        if move == "left" and col == 0:
            continue
        if move == "right" and col == 2:
            continue

        new_state = list(state)
        new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
        neighbors.append((tuple(new_state), move))

    return neighbors

def astar(start):
    pq = []
    heapq.heappush(pq, (manhattan(start), 0, start, []))
    visited = set()

    while pq:
        f, g, current, path = heapq.heappop(pq)

        if current == GOAL_STATE:
            return path

        if current in visited:
            continue

        visited.add(current)

        for neighbor, move in get_neighbors(current):
            if neighbor not in visited:
                heapq.heappush(pq, (
                    g + 1 + manhattan(neighbor),
                    g + 1,
                    neighbor,
                    path + [move]
                ))

    return []

def bfs(start):
    queue = deque([(start, [])])
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current == GOAL_STATE:
            return path

        visited.add(current)

        for neighbor, move in get_neighbors(current):
            if neighbor not in visited:
                queue.append((neighbor, path + [move]))

    return []

# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    data = request.json
    board = data["board"]
    algorithm = data["algorithm"]

    # convert 2D -> tuple
    flat = tuple([num for row in board for num in row])

    import time
    start = time.time()

    if algorithm == "astar":
        solution = astar(flat)
    else:
        solution = bfs(flat)

    end = time.time()

    return jsonify({
        "solution_path": solution,
        "moves": len(solution),
        "time": round(end - start, 3)
    })

# -------------------------
# RUN APP
# -------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)