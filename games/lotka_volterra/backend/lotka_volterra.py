# import matplotlib.pyplot as plt
# import random
# import numpy as np


# # params
# alpha = 0.1         # prey birth rate
# beta = 0.02            # predation rate
# gamma = 0.3           # predator death rate
# theta = 0.01        # predator fitness gain through predation

# # initial populations
# x0 = 30      # prey
# y0 = 9    # predators

# # simulations settings
# t_max = 200
# dt = 0.1
# steps = int(t_max / dt)

# # init empty array
# x = np.zeros(steps)
# y = np.zeros(steps)
# t = np.linspace(0, t_max, steps)

# # assign first time step
# x[0] = x0
# y[0] = y0


# x_eq = gamma / theta
# y_eq = alpha / beta
# print(x_eq, y_eq)


# lotka volterra formula
def lotka_volterra(x,           # prey per capita population density
                   y,           # predator per capita population density      

                   alpha,       # effect of the presence of predators on the preys death rate
                   beta,        # preys per capita death rate

                   gamma,       # predators per capita death rate
                   theta        # effect of the prescence of prey on the predators growth rate
                   ):

    dx = (alpha * x) - (beta * x * y)
    dy = -(gamma * y) + (theta * x * y)

    return dx, dy



# # running the simulation for each time step
# for i in range(1, steps):
#     dx, dy = lotka_volterra(
#         x[i-1],
#         y[i-1],
#         alpha,
#         beta,
#         gamma,
#         theta
#         )
    
#     x[i] = x[i-1] + dx * dt
#     y[i] = y[i-1] + dy * dt



# # Plot results
# plt.figure(figsize=(10,5))
# plt.plot(t, x, label='Prey')
# plt.plot(t, y, label='Predator')
# plt.xlabel('Time')
# plt.ylabel('Population')
# plt.title('Lotka-Volterra Predator-Prey Model')
# plt.legend()
# plt.show()