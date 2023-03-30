import random

import random

class LocalBeam:
    def __init__(self, W: int, m: int, w: 'list[int]', v: 'list[int]', c: 'list[int]') -> None:
        self.W = W
        self.m = m
        self.w = w
        self.v = v
        self.c = c
        self.n = len(w)
        self.k = m
    
    def random_solution(self):
        selected = [0] * self.n
        for c in range(self.m):
            items = [i for i in range(self.n) if self.c[i] == c]
            k = min(self.k, len(items))
            if k == 0:
                k = 1
            if k > len(items):
                k = len(items)
            selected_items = random.sample(items, k)
            for i in selected_items:
                selected[i] = 1
        return ''.join(map(str, selected))
    
    def evaluate(self, solution):
        total_value = 0
        total_weight = 0
        for i in range(self.n):
            if solution[i] == '1':
                total_value += self.v[i]
                total_weight += self.w[i]
        if total_weight > self.W:
            total_value = 0
        return total_value
    
    def generate_neighborhood(self, beam):
        neighborhood = []
        for i in range(self.n):
            neighbor = list(beam)
            neighbor[i] = '1' if neighbor[i] == '0' else '0'
            neighborhood.append(''.join(neighbor))
        return neighborhood
    
    def solve(self, k, max_iterations):
        beams = [self.random_solution() for _ in range(k)]
        best_solution = max(beams, key=self.evaluate)
        best_value = self.evaluate(best_solution)
        arr = [0] * self.n

        for i in range(max_iterations):
            neighborhood = []
            for beam in beams:
                neighborhood += self.generate_neighborhood(beam)
            beams = sorted(neighborhood, key=self.evaluate, reverse=True)[:k]
            new_best_solution = max(beams, key=self.evaluate)
            new_best_value = self.evaluate(new_best_solution)
            if new_best_value > best_value:
                best_solution = new_best_solution
                best_value = new_best_value

        chosen_items = [i for i in range(self.n) if best_solution[i] == '1']
        for item in chosen_items:
            arr[item] = 1
        return str(best_value), ', '.join([str(i) for i in arr])

test_seq = 3
def write_result(seq: int, value: str, state: str):
    with open(f"./Output/OUTPUT_{seq}.txt", 'w') as f:
        f.write(value + '\n' + state)
        print("Write file successfully!")

with open(f"./Tests/INPUT_{test_seq}.txt") as f:
    lines = f.readlines() 
    W = int(lines[0])
    m = int(lines[1])
    w = [int(l) for l in lines[2].strip().split(', ')]
    v = [int(l) for l in lines[3].strip().split(', ')]
    c = [int(l) for l in lines[4].strip().split(', ')]

    lb = LocalBeam(W, m, w, v, c)
    value, state = lb.solve(k=10, max_iterations=1000)
write_result(test_seq, value, state)