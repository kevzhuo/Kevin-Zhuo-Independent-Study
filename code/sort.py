import random
import numpy as np
from typing import List
from preprocess import graph
import time

class SortFAS:
    def __init__(self, graph, order):
        self.G = graph 
        self.n = max(graph) + 10
        self.A = list(range(self.n)) if order == None else order
        self.rand = random.Random()

    def shuffle(self, array: List[int]):
        self.rand.shuffle(array)

    def edge_to(self, u: int, w: int) -> bool:
        return w in self.G[u] 

    def sort(self, A: List[int]):
        steps = 0
        for i in range(1, len(A)):
            curr = A[i]
            val = 0
            min_val = 0
            loc = i
            for j in range(i - 1, -1, -1):
                if self.edge_to(curr, A[j]):
                    val -= 1
                elif self.edge_to(A[j], curr):
                    val += 1

                if val <= min_val:
                    min_val = val
                    loc = j

            for t in range(i - 1, loc - 1, -1):
                A[t + 1] = A[t]
                steps += 1
            A[loc] = curr
            steps += 1
        return steps

    def compute_fas(self) -> int:
        steps = self.sort(self.A)
        varray = {v: i for i, v in enumerate(self.A)} 

        fvs = set()  
        fas = 0 
        
        for v in self.G:
            for w in self.G[v]: 
                if v == w:
                    continue 
                if varray[v] > varray[w]:  
                    fvs.add(v)
                    fas += 1

        return steps, fas

if __name__ == "__main__":
    sorter = SortFAS(graph, None)
    start = time.time()
    steps, fas = sorter.compute_fas()
    end = time.time()
    print("Time taken:", end - start)
    print("Steps taken:", steps)
    print("Final FAS size:", fas)