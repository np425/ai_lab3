""" 
Task 2.
- Implement A* search
- Test A* search path 1 => 9
- Test A* search with various starting and ending positions
"""

from graph import GRAPH
from test import test, compare_tests, random_node, display
from math import sqrt
import heapq

def graph_coords(graph):
    coords = {}

    start = next(iter(graph.keys()))
    queue = [(start, 0, 0)]

    while queue:
        node, x, y = queue.pop(0)

        if node in coords.keys():
            continue

        coords[node] = (x,y)

        siblings = graph[node]
        undiscovered = set(siblings) - set(coords.keys())
        elements = [(sibling, x+1, y) for y, sibling in enumerate(undiscovered)]

        queue.extend(elements)
    
    return coords

def euclidean_heuristic(graph, coords, start, end):
    start_x, start_y = coords[start]
    end_x, end_y = coords[end]

    x = abs(end_x - start_x)
    y = abs(end_y - start_y)

    dist = sqrt(x**2 + y**2)
    return dist

def node_distance(current, other):
    return 1

def a_search(graph, distance_f, heuristic_f, start, end):
    visited = []
    heap = [(0 + heuristic_f(start, end), 0, None, start)]

    while heap:
        weight, dist, prev, root = heapq.heappop(heap)

        if root in visited:
            continue

        visited.append(root)

        if root is end:
            return visited

        siblings = graph[root]
        for sibling in siblings:
            new_dist = dist + distance_f(root, sibling)
            new_weight = new_dist + heuristic_f(sibling, end)
            heapq.heappush(heap, (new_weight, new_dist, root, sibling))
    

if __name__ == "__main__":
    coords = graph_coords(GRAPH)

    def h(start, end):
        return euclidean_heuristic(GRAPH, coords, start, end)

    display(test(a_search, GRAPH, node_distance, h, 1, 9))

    tests = []
    for start in GRAPH.keys():
        for end in GRAPH.keys():
            tests.append(test(a_search, GRAPH, node_distance, h, start, end))

    compare_tests('all a* combinations', *tests)

    tests = []
    for _ in range(10000):
        start = random_node(GRAPH)
        end = random_node(GRAPH)

        tests.append(test(a_search, GRAPH, node_distance, h, start, end))

    compare_tests('random a* tests', *tests)
