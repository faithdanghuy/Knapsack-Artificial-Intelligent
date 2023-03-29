import itertools

class BruteForce:
    def __init__(self, W: int, m: int, w: 'list[int]', v: 'list[int]', c: 'list[int]') -> None:
        self.W = W
        self.m = m
        self.w = w
        self.v = v
        self.c = c

    def solve(self):
        n = len(self.w)
        combos = itertools.product((0, 1), repeat=n)
        best_value = 0
        best_items = ()

        for combo in combos:
            classes = set()
            weight = 0
            value = 0
            for i in range(n):
                if not combo[i]:
                    continue
                classes.add(self.c[i])
                weight += self.w[i]
                value += self.v[i]

            if weight > self.W:
                continue
            if len(classes) != self.m:
                continue
            if value > best_value:
                best_value = value
                best_items = combo

        state = ', '.join([str(i) for i in best_items])
        return str(best_value), state

test_seq = 2
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

    # for _ in range(test_num):
    bf = BruteForce(W, m, w, v, c)
    value, state = bf.solve()

write_result(test_seq, value, state)