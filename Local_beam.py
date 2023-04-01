import itertools

class LocalBeam:
    def __init__(self, W: int, m: int, w: 'list[int]', v: 'list[int]', c: 'list[int]') -> None:
        self.W = W
        self.m = m
        self.w = w
        self.v = v
        self.c = c
        self.n = len(w)
        self.k = m
    
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
        initial_solution = max([''.join(map(str, x)) for x in itertools.product([0, 1], repeat=self.n)], key=self.evaluate)
        beams = [initial_solution] * k
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
        return best_value, ', '.join([str(i) for i in arr])

test_seq = 2
test_num = 3
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

    best_value = 0
    best_state = None
    for i in range(test_num):
        lb = LocalBeam(W, m, w, v, c)
        value, state = lb.solve(k=10, max_iterations=1000)

        if value > best_value:
            best_value = value
            best_state = state

        print(f"Finish test {i+1}")

write_result(test_seq, str(best_value), best_state)