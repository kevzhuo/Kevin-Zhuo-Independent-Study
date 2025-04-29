import random
from collections import defaultdict
from preprocess import graph


net_degree = defaultdict(int)

#Calculate out degree - in degree
for node in graph:
    for neighbor in graph[node]:
        net_degree[node] += 1
        net_degree[neighbor] -= 1

# Sort nodes by net degree
sorted_nodes = sorted(net_degree, key=net_degree.get, reverse=True)
color = [0] * (max(graph)+5)
back_edges = set()
feedback_arc_set = 0
starting_node = sorted_nodes[0]
stack = [starting_node]

while stack:
    current_node = stack[-1]
    if color[current_node] != 1:
        color[current_node] = 1
        neighbors = sorted(graph[current_node], key=net_degree.get, reverse=True)
        for neighbor in graph[current_node]:
            net_degree[neighbor] += 1
            if color[neighbor] == 0:
                stack.append(neighbor)
            elif color[neighbor] == 1:
                back_edges.add((current_node, neighbor))
    elif color[current_node] == 1:
        color[current_node] = 2
        stack.pop()


print("Starting Node: " + str(sorted_nodes[0]))

#print("Back Edges: " + str(back_edges))
print("Feedback Arc Set: ",len(back_edges))