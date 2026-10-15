from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.pyplot as plt

class PhasePlotTab(QWidget):
    def __init__(self, world, grid_x, grid_y):
        super().__init__()
        self.world = world

        self.layout = QVBoxLayout(self)

        # Create matplotlib figure and axis
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.layout.addWidget(self.canvas)

        # Trajectory line
        self.phase_line, = self.ax.plot(
            [], [],
            color="purple",
            lw=2,
            label="System trajectory"
        )

        # Current state marker
        self.phase_point, = self.ax.plot(
            [], [],
            'o',
            color="black",
            markersize=6,
            label="Current state"
        )

        self.ax.set_xlabel("Herbivores")
        self.ax.set_ylabel("Carnivores")
        self.ax.set_title("Lotka–Volterra Phase Portrait")
        self.ax.legend()
        self.ax.grid(True, alpha=0.3)

    def refresh_plot(self):
        prey_history = list(self.world.prey_history)
        predator_history = list(self.world.predator_history)

        if not prey_history or not predator_history:
            return

        # Update trajectory
        self.phase_line.set_data(prey_history, predator_history)

        # Update current point
        self.phase_point.set_data(
            [prey_history[-1]],
            [predator_history[-1]]
        )
        
        self.ax.relim()
        self.ax.autoscale_view() 

        # # Dynamic limits
        # x_max = max(prey_history) * 1.1
        # y_max = max(predator_history) * 1.1
        # self.ax.set_xlim(0, x_max)
        # self.ax.set_ylim(0, y_max)

        # Redraw canvas
        self.canvas.draw_idle()

    def set_world(self, world):
        self.world = world
        self.refresh_plot()

