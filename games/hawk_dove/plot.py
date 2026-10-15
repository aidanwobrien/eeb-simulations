import matplotlib.pyplot as plt

class Plot:
    def __init__(self, world, rows, cols):
        self.rows = rows
        self.cols = cols
        self.axis_limit = self.rows * self.cols
        self.world = world
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.line_hawk, = self.ax.plot([], [], color='red', label='Hawks')
        self.line_dove, = self.ax.plot([], [], color='blue', label='Doves')

        self.hawk_history = []
        self.dove_history = []
        self.hawks = 0
        self.doves = 0

        self.ax.set_xlim(0, self.axis_limit)
        self.ax.set_ylim(0, self.axis_limit)
        self.ax.set_xlabel("Generation")
        self.ax.set_ylabel("Population")
        self.ax.legend()
        self.ax.set_title("Hawk-Dove Simulation")
        self.fig.canvas.manager.set_window_title("Hawk-Dove Simulation")


    def update(self):

        self.hawks = sum(1 for ind in self.world.individuals if ind.phenotype == "hawk")
        self.doves = sum(1 for ind in self.world.individuals if ind.phenotype == "dove")

        self.hawk_history.append(self.hawks)
        self.dove_history.append(self.doves)

        self.line_hawk.set_data(range(len(self.hawk_history)), self.hawk_history)
        self.line_dove.set_data(range(len(self.dove_history)), self.dove_history)

        x_len = len(self.hawk_history)

        xmin, xmax = self.ax.get_xlim()
        if x_len >= xmax:
            self.ax.set_xlim(0, xmax * 2)



