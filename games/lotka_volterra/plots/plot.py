import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import MaxNLocator

class Plot:
    def __init__(self, world, grid_x, grid_y):
        self.world = world

        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.line_food, = self.ax.plot([], [], color="green", label="Plants")
        self.line_prey, = self.ax.plot([], [], color='blue', label='Herbivores')
        self.line_pred, = self.ax.plot([], [], color='red', label='Carnivores')

        self.generations = 0

        self.ax.set_xlim(0, 500)
        self.ax.set_ylim(0, max(world.initial_prey_pop, world.initial_predator_pop) * 2)
        self.ax.set_xlabel("Ticks")
        self.ax.set_ylabel("Population")
        self.ax.legend()
        # self.ax.set_title("Primary and Secondary Consumer Population")
        self.fig.canvas.manager.set_window_title("Lotka-Volterra Simulation")

        self.ax.yaxis.set_major_locator(MultipleLocator(50))
        self.ax.xaxis.set_major_locator(MaxNLocator(nbins=8, integer=True))
        

    def update(self):
        food_history = list(self.world.food_history)
        prey_history = list(self.world.prey_history)
        predator_history = list(self.world.predator_history)

        if not prey_history:
            return

        self.generations = list(range(len(prey_history)))

        # Update the lines
        self.line_food.set_data(self.generations, food_history)
        self.line_prey.set_data(self.generations, prey_history)
        self.line_pred.set_data(self.generations, predator_history)

        xmax = len(prey_history)
        if xmax > self.ax.get_xlim()[1]:
            self.ax.set_xlim(0, xmax + 500)
            self.ax.xaxis.set_major_locator(
                MaxNLocator(nbins=8, integer=True)
                )

        # Dynamically expand y-axis
        ymax = max(food_history + prey_history + predator_history) * 1.1
        if ymax > self.ax.get_ylim()[1]:
            self.ax.set_ylim(0, ymax)

            

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


