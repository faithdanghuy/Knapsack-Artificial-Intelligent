import random
import matplotlib.pyplot as plt
class Genetic:
  POPULATION_SIZE = 200
  MUTATION_PROB = 0.1
  MAX_GEN = 500
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
    self.best_chromosome = 0
    self.best_value = 0

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
    
    if total_v > self.best_value:
      self.best_value = total_v
      self.best_chromosome = chromosome

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
    _ = [self.fitness(chrom) for chrom in self.population]
    # max_fit = -1
    # best = 0
    # for i in range(len(self.population)):
    #   if fitnesses[i] > max_fit:
    #     max_fit = fitnesses[i]
    #     best = i
    return self.best_value, self.best_chromosome

  def solve(self, trace: 'list[int]'=None):
    gen = 0
    while gen != Genetic.MAX_GEN:
      fitnesses = [self.fitness(chrom) for chrom in self.population]
      new_population = []
      
      if trace is not None:
        trace.append(self.best_value)
      # print(fitnesses[best], bin(self.population[best]))
      new_population.append(self.best_chromosome)

      for _ in range(0, Genetic.POPULATION_SIZE, 2):
        first_parent, second_parent = self.selection(fitnesses, 2)

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


test_seq = 8
test_num = 5
def write_result(seq: int, value: str, state: str):
  with open(f"OUTPUT_{seq}.txt", 'w') as f:
    f.write(value + '\n' + state)


with open(f"INPUT_{test_seq}.txt") as f:
  lines = f.readlines() 
  W = int(lines[0])
  m = int(lines[1])
  w = [int(l) for l in lines[2].strip().split(', ')]
  v = [int(l) for l in lines[3].strip().split(', ')]
  c = [int(l) for l in lines[4].strip().split(', ')]

  best_value = 0
  best_sol = None
  for _ in range(test_num):
    gen = Genetic(W, m, w, v, c)
    trace = []
    sol = gen.solve(trace)
    if int(sol[0]) > best_value:
      best_value = int(sol[0])
      best_sol = sol
    plt.plot(trace)
  # plt.show()
  write_result(test_seq, *best_sol)
plt.show()
  # print(W)
  # print(m)
  # print(w)
  # print(v)
  # print(c)