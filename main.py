import random

class Genetic:
  POPULATION_SIZE = 100
  MUTATION_PROB = 0.1
  MAX_GEN = 100
  def __init__(self, W: int, m: int, w: 'list[int]', v: 'list[int]', c: 'list[int]') -> None:
    if len(w) != len(v) or len(w) != len(c) or len(v) != len(c):
      raise Exception("Invalid parameters")
    self.n = len(w)
    self.W = W
    self.m = m
    self.w = w
    self.v = v
    self.c = c
    self.population = [random.getrandbits(self.n) for _ in range(Genetic.POPULATION_SIZE)]

  def fitness(self, chromosome: int):
    total_v = 0
    total_w = 0
    classes = set()
    for i in range(self.n):
      choose = (chromosome & (1 << i))
      if not choose:
        continue

      total_v += self.v[-1 - i]
      total_w += self.w[-1 - i]
      if total_w > self.W:
        return 0
      classes.add(self.c[-1 - i])

    if len(classes) != self.m:
      return 0
    
    return total_v
  
  def selection(self, fitnesses: 'list[int]', max_per_tournament=2):
    choices = random.sample(range(len(self.population)), max_per_tournament * 2)
    first_winner = 0
    max_fitness = -1
    for i in choices[:max_per_tournament]:
      if fitnesses[i] > max_fitness:
        first_winner = i
        max_fitness = fitnesses[i]
    
    second_winner = 0
    max_fitness = -1
    for i in choices[max_per_tournament:]:
      if fitnesses[i] > max_fitness:
        second_winner = i
        max_fitness = fitnesses[i]

    return self.population[first_winner], self.population[second_winner]

  def cross_over(self, top: int, bot: int):
    c = random.randrange(self.n)
    first_child = (top & ((1 << c) - 1)) + (bot & (((1 << (self.n - c)) - 1) << c))
    second_child = (bot & ((1 << c) - 1)) + (top & (((1 << (self.n - c)) - 1) << c))
    return first_child, second_child

  def mutate(self, chromosome: int):
    c = random.randrange(0, self.n)
    return chromosome ^ (1 << c)

  def choose_best(self):
    fitnesses = [self.fitness(chrom) for chrom in self.population]
    max_fit = -1
    best = 0
    for i in range(len(self.population)):
      if fitnesses[i] > max_fit:
        max_fit = fitnesses[i]
        best = i
    return fitnesses[best], self.population[best]

  def solve(self):
    gen = 0
    while gen != Genetic.MAX_GEN:
      fitnesses = [self.fitness(chrom) for chrom in self.population]
      new_population = []
      for _ in range(0, Genetic.POPULATION_SIZE, 2):
        first_parent, second_parent = self.selection(fitnesses, 4)

        first_child, second_child = self.cross_over(first_parent, second_parent)

        if random.random() < Genetic.MUTATION_PROB:
          first_child = self.mutate(first_child)
        if random.random() < Genetic.MUTATION_PROB:
          second_child = self.mutate(second_child)

        new_population.append(first_child)
        new_population.append(second_child)

      del self.population
      self.population = new_population
      gen += 1
    
    sol = self.choose_best()
    state = ", ".join(bin(sol[1])[2:].rjust(self.n, '0'))
    return str(sol[0]), state


def write_result(seq: int, value: str, state: str):
  with open(f"OUTPUT_{seq}.txt", 'w') as f:
    f.write(value + '\n' + state)

with open("INPUT_1.txt") as f:
  lines = f.readlines() 
  W = int(lines[0])
  m = int(lines[1])
  w = [int(l) for l in lines[2].strip().split(', ')]
  v = [int(l) for l in lines[3].strip().split(', ')]
  c = [int(l) for l in lines[4].strip().split(', ')]

  gen = Genetic(W, m, w, v, c)
  write_result(1, *gen.solve())
  # print(W)
  # print(m)
  # print(w)
  # print(v)
  # print(c)