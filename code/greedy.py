from preprocess import graph, transpose_graph
import sort
import time

class ArrayFAS:
    def __init__(self, graph, transpose_graph):
        self.G = graph
        self.I = transpose_graph
        self.n = max(graph) + 10
        self.num_classes = 2 * self.n - 3
        self.deltas = [0] * self.n # Delta class for a vertex, determines if a vertex is present
        self.next = [-1] * self.n # Holds reference to next node for vertex i
        self.prev = [-1] * self.n # Holds reference to next node for vertex i
        self.bins = [-1] * self.num_classes 
        self.max_delta = float('-inf')
        self.seq = None
        self.create_bins()

    def degree(self, graph, u):
        return sum(1 for v in graph.get(u, []) if v != u)

    def create_bins(self):
        for u in range(self.n):
            out_deg = self.degree(self.G, u)
            in_deg = self.degree(self.I, u)
            if out_deg == 0:
                self.add_to_bin(2 - self.n, u)
                self.deltas[u] = 2 - self.n
            elif in_deg == 0 and out_deg > 0:
                self.add_to_bin(self.n - 2, u)
                self.deltas[u] = self.n - 2
            else:
                delta = out_deg - in_deg
                self.add_to_bin(delta, u)
                self.deltas[u] = delta

    def add_to_bin(self, delta, v):
        bin_index = delta - (2 - self.n)
        if self.bins[bin_index] == -1:
            self.bins[bin_index] = v
            self.prev[v] = -1
        else:
            self.next[self.bins[bin_index]] = v
            self.prev[v] = self.bins[bin_index]
            self.bins[bin_index] = v
        self.next[v] = -1
        if delta < self.n - 2 and self.max_delta < delta:
            self.max_delta = delta

    def update_max_delta(self, delta):
        bin_index = delta - (2 - self.n)
        if delta == self.max_delta and self.bins[bin_index] == -1:
            while self.bins[self.max_delta - (2 - self.n)] == -1:
                self.max_delta -= 1
                if self.max_delta == (2 - self.n):
                    break

    def delete_node(self, u):
        self.deltas[u] = float('-inf')
        self._delete_node_from_graph(self.G, u, True)
        self._delete_node_from_graph(self.I, u, False)
        self.prev[u] = -1
        self.next[u] = -1

    def _delete_node_from_graph(self, graph, u, out):
        for v in graph.get(u, []):
            if v == u:
                continue
            if self.deltas[v] > float('-inf'):
                old_delta = self.deltas[v]
                new_delta = old_delta + 1 if out else old_delta - 1
                self.deltas[v] = new_delta

                bin_index = old_delta - (2 - self.n)
                if self.bins[bin_index] == v:
                    self.bins[bin_index] = self.prev[v]
                if self.prev[v] != -1:
                    self.next[self.prev[v]] = self.next[v]
                if self.next[v] != -1:
                    self.prev[self.next[v]] = self.prev[v]

                self.add_to_bin(new_delta, v)
                self.update_max_delta(old_delta)

    def compute_sequence(self):
        s1 = []
        s2 = []
        num_deleted = 0

        while num_deleted < self.n:
            while self.bins[0] != -1:
                u = self.bins[0]
                self.bins[0] = self.prev[u]
                if self.prev[u] != -1:
                    self.next[self.prev[u]] = -1
                self.delete_node(u)
                num_deleted += 1
                s2.insert(0, u)

            while self.bins[self.num_classes - 1] != -1:
                u = self.bins[self.num_classes - 1]
                self.bins[self.num_classes - 1] = self.prev[u]
                if self.prev[u] != -1:
                    self.next[self.prev[u]] = -1
                self.delete_node(u)
                num_deleted += 1
                s1.append(u)

            if num_deleted < self.n:
                if self.bins[self.max_delta - (2 - self.n)] == -1:
                    print(f"Max delta bin is empty: {self.max_delta}")
                u = self.bins[self.max_delta - (2 - self.n)]
                self.bins[self.max_delta - (2 - self.n)] = self.prev[u]
                if self.prev[u] != -1:
                    self.next[self.prev[u]] = -1
                self.update_max_delta(self.max_delta)
                self.delete_node(u)
                num_deleted += 1
                s1.append(u)

        s1.extend(s2)
        self.seq = s1
        return self.seq

    def compute_fas(self):
        if self.seq is None:
            self.compute_sequence()

        varray = [0] * self.n
        for i, u in enumerate(self.seq):
            varray[u] = i

        fvs = set()
        fas = 0

        for v, neighbors in self.G.items():
            for w in neighbors:
                if v == w:  
                    continue
                if varray[v] > varray[w]:
                    fvs.add(v)
                    fas += 1

        return fas

if __name__ == "__main__":
    greedy = ArrayFAS(graph, transpose_graph)
    start = time.time()
    order = greedy.compute_sequence()
    fas_size = greedy.compute_fas()
    end = time.time()
    print("Greedy time taken:", end - start)
    print("Greedy FAS size:", fas_size)
    # To test out the Sort method with a Greedy ordering already calculated
    start = time.time()
    sort_fas = sort.SortFAS(graph, order)
    steps, fas = sort_fas.compute_fas()
    print("Sort FAS size:", fas)
    end = time.time()
    print("Steps taken:", steps)
    print("Sort time taken:", end - start)