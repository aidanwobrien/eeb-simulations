import matplotlib.pyplot as plt

class PhasePlot:
    def __init__(self, world):
        self.world = world

        plt.ion()
        self.fig, self.ax = plt.subplots()

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

        self.fig.canvas.manager.set_window_title("Phase Portrait Plot")

    def update(self):
        prey_history = list(self.world.prey_history)
        predator_history = list(self.world.predator_history)

        if not prey_history:
            return

        # Update trajectory
        self.phase_line.set_data(prey_history, predator_history)

        # Update current point
        self.phase_point.set_data(
            [prey_history[-1]],
            [predator_history[-1]]
        )

        # Dynamic limits
        x_max = max(prey_history) * 1.1
        y_max = max(predator_history) * 1.1

        self.ax.set_xlim(0, x_max)
        self.ax.set_ylim(0, y_max)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
