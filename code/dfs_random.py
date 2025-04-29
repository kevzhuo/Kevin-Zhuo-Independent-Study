import random
from preprocess import graph

visited = [0] * (max(graph) + 5)
rec_stack = [0] * (max(graph) + 5)
back_edges = set()
feedback_arc_set = 0

def dfs(graph, node):
    visited[node] = 1
    rec_stack[node] = 1
    neighbors = random.sample(graph[node], len(graph[node]))
    for neighbor in neighbors:
        if visited[neighbor] == 0:
            dfs(graph, neighbor)
        elif rec_stack[neighbor] == 1:
            global feedback_arc_set
            back_edges.add((node, neighbor))
            feedback_arc_set += 1
    rec_stack[node] = 0

starting_node = random.choice(list(graph.keys()))
print("Starting Node: " + str(starting_node))

dfs(graph, starting_node)
print("Feedback Arc Set: " + str(feedback_arc_set))