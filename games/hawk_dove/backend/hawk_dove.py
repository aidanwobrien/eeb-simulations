import matplotlib.pyplot as plt
import random


# # cost > value
# value = 50
# cost = 1000

# population_size = 2000
# generations = 200
# games_per_individual = 10

# population = []


# for i in range(population_size):
#     phenotype = random.choice(["hawk", "dove"])
#     population.append(phenotype)


# hawk_history = []
# dove_history = []


# for gen in range(generations):

#     scores = [0] * population_size
#     fitness = []

#     for i in range(population_size):
#         for _ in range(games_per_individual):
#             j = random.randrange(population_size)
#             if i != j:
#                 scores[i] += hawk_dove_payoff(population[i], population[j], value, cost)

#     average_scores = []
#     for s in scores:
#         avg = s / games_per_individual
#         average_scores.append(avg)

#     min_score = min(average_scores)
#     fitness = []
#     for s in average_scores:
#         fit = s - min_score + 1e-6
#         fitness.append(fit)

#     population = random.choices(population, weights=fitness, k=population_size)


#     hawks = population.count("hawk")
#     doves = population.count("dove")

#     hawk_history.append(hawks)
#     dove_history.append(doves)

# plt.figure(figsize=(8,5))
# plt.plot(hawk_history, label="Hawks", color="red")
# plt.plot(dove_history, label="Doves", color="blue")
# plt.xlabel("Generation")
# plt.ylabel("Population")
# plt.title("Hawk-Dove Evolutionary Dynamics")
# plt.legend()
# plt.grid(True)
# plt.show()


def hawk_dove_payoff(a, b, value, cost):
    if a == "hawk" and b == "hawk":
        return (value - cost) / 2
    if a == "hawk" and b == "dove":
        return value
    if a == "dove" and b == "hawk":
        return 0
    if a == "dove" and b == "dove":
        return value / 2
    
