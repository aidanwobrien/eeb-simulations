from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator, MaxNLocator

class PlotTab(QWidget):
    def __init__(self, world, grid_x, grid_y):
        super().__init__()
        self.world = world

        layout = QVBoxLayout(self)
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.ax = self.fig.add_subplot(111)
        self.line_food, = self.ax.plot([], [], color="green", label="Plants")
        self.line_prey, = self.ax.plot([], [], color="blue", label="Herbivores")
        self.line_pred, = self.ax.plot([], [], color="red", label="Carnivores")

        self.ax.set_xlim(0, 500)
        self.ax.set_ylim(0, max(world.initial_prey_pop, world.initial_predator_pop) * 2)
        self.ax.set_xlabel("Ticks")
        self.ax.set_ylabel("Population")
        self.ax.legend()
        self.ax.yaxis.set_major_locator(MaxNLocator(nbins=8, integer=True))
        self.ax.xaxis.set_major_locator(MaxNLocator(nbins=8, integer=True))

        self.generations = 0

    def refresh_plot(self):
        food_history = list(self.world.food_history)
        prey_history = list(self.world.prey_history)
        predator_history = list(self.world.predator_history)

        if not prey_history:
            return

        generations = list(range(len(prey_history)))

        # Update lines
        self.line_food.set_data(generations, food_history)
        self.line_prey.set_data(generations, prey_history)
        self.line_pred.set_data(generations, predator_history)

        # Update x-axis dynamically
        self.ax.set_xlim(0, len(generations))
        self.ax.xaxis.set_major_locator(MaxNLocator(nbins=8, integer=True))

        # Update y-axis dynamically with 10% padding
        all_values = food_history + prey_history + predator_history
        ymax = max(all_values) * 1.1 if all_values else 1
        self.ax.set_ylim(0, ymax)

        # Redraw canvas
        self.canvas.draw_idle()

    def set_world(self, world):
        self.world = world
        self.refresh_plot()
