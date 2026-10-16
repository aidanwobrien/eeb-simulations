
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