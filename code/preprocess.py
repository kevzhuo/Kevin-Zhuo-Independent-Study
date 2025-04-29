from collections import defaultdict

graph = defaultdict(list)
transpose_graph = defaultdict(list)

f = open("", "r")

for line in f:
    line = line.split()
    graph[int(line[0])].append(int(line[1]))
    transpose_graph[int(line[1])].append(int(line[0]))

f.close()

# graph1.txt = https://snap.stanford.edu/data/p2p-Gnutella08.html
# graph2.txt = https://snap.stanford.edu/data/soc-Epinions1.html
# graph3.txt = https://snap.stanford.edu/data/p2p-Gnutella31.html
# graph4.txt = https://snap.stanford.edu/data/facebook-large-page-page-network.html 