import heapq
from state import PuzzleState
from heuristic import manhattan_distance


def astar(start_board):
    start_state = PuzzleState(start_board)
    goal = [[1,2,3],[4,5,6],[7,8,0]]

    open_list = []
    counter = 0
    heapq.heappush(open_list, (0, counter, start_state))

    visited = set()
    nodes_explored = 0

    while open_list:
        _, _, current = heapq.heappop(open_list)
        nodes_explored += 1

        if current.board == goal:
            return reconstruct_path(current), nodes_explored

        visited.add(current)

        for child in current.generate_children():
            if child not in visited:
                counter += 1
                f = child.depth + manhattan_distance(child.board)
                heapq.heappush(open_list, (f, counter, child))

    return None, nodes_explored 


from collections import deque
import time

def bfs(start_board):
    start_state = PuzzleState(start_board)
    goal = [[1,2,3],[4,5,6],[7,8,0]]

    queue = deque([start_state])
    visited = set()
    visited.add(start_state)

    nodes_explored = 0

    while queue:
        current = queue.popleft()
        nodes_explored += 1

        if current.board == goal:
            return reconstruct_path(current), nodes_explored

        for child in current.generate_children():
            if child not in visited:
                visited.add(child)
                queue.append(child)

    return None, nodes_explored



def reconstruct_path(state):
    path = []
    while state.parent:
        path.append(state.move)
        state = state.parent
    return path[::-1]



def is_solvable(board):
    flat = sum(board, [])
    inversions = 0

    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] != 0 and flat[j] != 0 and flat[i] > flat[j]:
                inversions += 1

    return inversions % 2 == 0

