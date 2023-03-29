

class BranchAndBound:
    def __init__(self, W: int, m: int, w: 'list[int]', v: 'list[int]', c: 'list[int]') -> None:
        self.W = W
        self.m = m
        self.w = w
        self.v = v
        self.c = c
        self.n = len(w)
        self.best_value = 0
        self.best_items = []

    def bound(self, k: int, weight: int, value: int, taken: 'list[bool]') -> float:
        if weight >= self.W:
            return 0
        remaining_classes = set(self.c[k:])
        for i in range(k, self.n):
            if self.c[i] in remaining_classes:
                remaining_classes.remove(self.c[i])
                weight += self.w[i]
                value += self.v[i]
                taken[i] = True
        for i in range(k, self.n):
            if not taken[i] and self.c[i] not in remaining_classes:
                frac = min(1, (self.W - weight) / self.w[i])
                weight += frac * self.w[i]
                value += frac * self.v[i]
        return value

    def knapsack(self, k: int, weight: int, value: int, taken: 'list[bool]'):
        if weight <= self.W and value > self.best_value:
            self.best_value = value
            self.best_items = taken[:]
        if k == self.n:
            return
        if weight + self.w[k] <= self.W:
            taken[k] = True
            self.knapsack(k + 1, weight + self.w[k], value + self.v[k], taken)
            taken[k] = False
        if self.bound(k + 1, weight, value, taken) > self.best_value:
            taken[k] = False
            self.knapsack(k + 1, weight, value, taken)

    def solve(self) -> 'tuple[int, list[int]]':
        taken = [False] * self.n
        self.knapsack(0, 0, 0, taken)
        return str(self.best_value), ', '.join([str(int(i)) for i in self.best_items])

test_seq = 1
test_num = 1
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
    bin_arr = [0] * len(w)

    bb = BranchAndBound(W, m, w, v, c)
    value, state = bb.solve()

    write_result(test_seq, value, state)