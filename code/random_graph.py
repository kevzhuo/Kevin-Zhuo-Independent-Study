import random

def generate_random_directed_graph(num_vertices, output_file):
    edges = []

    for i in range(num_vertices):
        threshold = random.uniform(0.01, 0.3)  # Random threshold for the current node
        for j in range(num_vertices):
            if i != j:  # No self-loops
                edge_probability = random.random()  # Random number for each possible directed edge
                if edge_probability < threshold:
                    edges.append((i, j))

    # Save the edges to a file
    with open(output_file, 'w') as file:
        for edge in edges:
            file.write(f"{edge[0]} {edge[1]}\n")

if __name__ == "__main__":
    num_vertices = int(input("Enter the number of vertices: "))
    output_file = "directed_random_graph_edges.txt"
    generate_random_directed_graph(num_vertices, output_file)
    print(f"Directed random graph with edges saved to {output_file}.")
