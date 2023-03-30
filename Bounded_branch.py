from heapq import heappush, heappop

class Item:
    def __init__(self, weight, value, c):
        self.weight = weight
        self.value = value
        self.c = c

class Node:
    def __init__(self, level, value, weight, included, bound):
        self.level = level
        self.value = value
        self.weight = weight
        self.included = included
        self.bound = bound
        
    def __lt__(self, other):
        return self.bound > other.bound

class BranchAndBound:
    def __init__(self, W, m, w, v, c):
        self.W = W
        self.m = m
        self.items = [Item(w[i], v[i], c[i]) for i in range(len(w))]
        self.classes = set(c)

    def bound(self, node):
        if node.weight > self.W:
            return 0
        remaining_classes = self.classes - set([item.c for item in node.included])
        remaining_items = [item for item in self.items[node.level+1:] if item.c in remaining_classes]
        remaining_weight = self.W - node.weight
        bound = node.value
        for item in remaining_items:
            if item.weight <= remaining_weight:
                bound += item.value
                remaining_weight -= item.weight
            else:
                bound += item.value * (remaining_weight / item.weight)
                break
        return bound

    def solve(self):
        root = Node(-1, 0, 0, [], 0)
        heap = [root]
        max_value = 0
        solution = []
        while heap:
            node = heappop(heap)
            if node.bound <= max_value:
                continue
            if node.level == len(self.items) - 1:
                if node.value > max_value:
                    max_value = node.value
                    solution = node.included
                continue
            included = node.included + [self.items[node.level+1]]
            with_item = Node(node.level+1, node.value+self.items[node.level+1].value, node.weight+self.items[node.level+1].weight, included, self.bound(node))
            if with_item.bound > max_value:
                heappush(heap, with_item)
            without_item = Node(node.level+1, node.value, node.weight, node.included, self.bound(node))
            if without_item.bound > max_value:
                heappush(heap, without_item)

        return str(max_value), solution

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

    bb = BranchAndBound(W, m, w, v, c)
    value, state = bb.solve()

write_result(test_seq, value, state)