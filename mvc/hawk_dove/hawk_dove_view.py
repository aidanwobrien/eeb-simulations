from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFormLayout, QTabWidget, QScrollArea, QGroupBox,
    QSplitter, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
import pygame as pg
from time import perf_counter

from games.hawk_dove.world import World
from games.hawk_dove.game import Game as HDGame
from games.hawk_dove.settings import SIM_WINDOW_HEIGHT, SIM_WINDOW_WIDTH
from settings import APP_WINDOW_WIDTH, APP_WINDOW_HEIGHT

from mvc.hawk_dove.plot_tab import PlotTab
# from mvc.hawk_dove.phase_plot_tab import PhasePlotTab

TIMER_AMNT = 1


class HawkDoveWindow(QWidget):
    def __init__(self, start_page):
        super().__init__()
        pg.init()
        self.start_page = start_page
        self.setWindowTitle("Hawk-Dove Simulation")
        self.resize(APP_WINDOW_WIDTH, APP_WINDOW_HEIGHT)

        self.sim_timer = None
        self.sim_game = None
        self.sim_running = False
        self.sim_paused = False
        self.last_update_time = perf_counter()
        self.frames_per_generation_value = 60

        main_layout = QVBoxLayout(self)

        # ---------- Parameter inputs ----------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.sim_status_label = QLabel("Simulation: Not running")

        self.time_step = QLineEdit("0.1")
        self.grid_x = QLineEdit("40")
        self.grid_y = QLineEdit("40")
        self.games_per_individual = QLineEdit("10")

        self.value = QLineEdit("100")
        self.value.setToolTip(
            "Value of the resource (V).\n"
            "As the value increases, we expect more hawk phenotypes in the population, "
            "since fighting for the resource is worth more.\n"
            "At equilibrium the hawk fraction is V / C (if V ≥ C, hawks take over)."
        )

        self.costs = QLineEdit("500")
        self.costs.setToolTip(
            "Cost of injury from a fight (C).\n"
            "As the cost increases, we expect fewer hawk phenotypes in the population, "
            "since fighting is more costly.\n"
            "At equilibrium the hawk fraction is V / C."
        )

        self.frames_per_generation = QLineEdit("1")
        self.perlin_scale = QLineEdit("50")
        self.initial_hawk_pop = QLineEdit("400")
        self.initial_dove_pop = QLineEdit("400")
        self.selection_temp = QLineEdit("1000")



        world_group = QGroupBox("World Parameters")
        world_layout = QFormLayout()
        world_layout.addRow("Grid Width:", self.grid_x)
        world_layout.addRow("Grid Height:", self.grid_y)
        world_layout.addRow("Frames per generation:", self.frames_per_generation)
        world_layout.addRow("Perlin scale:", self.perlin_scale)
        world_layout.addRow("Initial hawk population:", self.initial_hawk_pop)
        world_layout.addRow("Initial dove population:", self.initial_dove_pop)
        world_layout.addRow("Randomness:", self.selection_temp)
        world_group.setLayout(world_layout)
        scroll_layout.addWidget(world_group)

        game_group = QGroupBox("Game Parameters")
        game_layout = QFormLayout()
        game_layout.addRow("Games per individual:", self.games_per_individual)
        game_layout.addRow("Resource value (V):", self.value)
        game_layout.addRow("Fight cost (C):", self.costs)
        game_group.setLayout(game_layout)
        scroll_layout.addWidget(game_group)

        scroll.setWidget(scroll_content)

        # ---------- Buttons ----------
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)

        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_simulation)

        self.pause_button = QPushButton("Pause")
        self.pause_button.setEnabled(False)
        self.pause_button.clicked.connect(self.toggle_pause)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_simulation)

        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)

        bottom_button_widget = QWidget()
        bottom_button_layout = QHBoxLayout(bottom_button_widget)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close_app)

        bottom_button_layout.addWidget(self.back_button)
        bottom_button_layout.addWidget(self.close_button)

        # ---------- World + plot tabs ----------
        # Build a world with the default values so the plot tabs have something to bind to.
        self.world = self.build_world(self.read_params())

        self.tabs = QTabWidget()
        self.time_series_tab = PlotTab(self.world, self.grid_x, self.grid_y)
        # self.phase_plot_tab = PhasePlotTab(self.world)
        self.tabs.addTab(self.time_series_tab, "Time Series")
        self.tabs.setCurrentWidget(self.time_series_tab)
        # self.tabs.addTab(self.phase_plot_tab, "Phase Plot")

        # ---------- Layout ----------
        splitter = QSplitter(Qt.Vertical)
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.addWidget(scroll)
        top_layout.addWidget(self.sim_status_label)
        top_layout.addWidget(button_widget)

        splitter.addWidget(top_widget)
        splitter.addWidget(self.tabs)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)
        main_layout.addWidget(bottom_button_widget)

        self.update_button_colors()

    # ------------------------------------------------------------------
    # Params / world construction
    # ------------------------------------------------------------------
    def read_params(self):
        """Parse every input field. Raises ValueError on bad input."""
        return {
            "TIME_STEP": float(self.time_step.text()),
            "GRID_X": int(self.grid_x.text()),
            "GRID_Y": int(self.grid_y.text()),
            "GAMES_PER_INDIVIDUAL": int(self.games_per_individual.text()),
            "VALUE": float(self.value.text()),
            "COSTS": float(self.costs.text()),
            "FRAMES_PER_GENERATION": int(self.frames_per_generation.text()),
            "PERLIN_SCALE": float(self.perlin_scale.text()),
            "INITIAL_HAWK_POP": int(self.initial_hawk_pop.text()),
            "INITIAL_DOVE_POP": int(self.initial_dove_pop.text()),
            "SELECTION_TEMP": float(self.selection_temp.text()),
        }

    def build_world(self, params):
        return World(
            None,
            SIM_WINDOW_WIDTH,
            SIM_WINDOW_HEIGHT,
            params["GRID_X"],
            params["GRID_Y"],
            params["GAMES_PER_INDIVIDUAL"],
            params["VALUE"],
            params["COSTS"],
            params["TIME_STEP"],
            params["FRAMES_PER_GENERATION"],
            params["PERLIN_SCALE"],
            params["INITIAL_HAWK_POP"],
            params["INITIAL_DOVE_POP"],
            params["SELECTION_TEMP"]
        )

    def validate_params(self, params):
        if params["GRID_X"] <= 0 or params["GRID_Y"] <= 0:
            self.show_error("Grid dimensions must be positive.")
            return False
        if params["FRAMES_PER_GENERATION"] <= 0:
            self.show_error("Frames per generation must be positive.")
            return False
        if params["GAMES_PER_INDIVIDUAL"] <= 0:
            self.show_error("Games per individual must be positive.")
            return False
        if params["COSTS"] < 0 or params["VALUE"] < 0:
            self.show_error("Value and cost cannot be negative.")
            return False
        if params["INITIAL_HAWK_POP"] < 0 or params["INITIAL_DOVE_POP"] < 0:
            self.show_error("Initial populations cannot be negative.")
            return False
        if params["INITIAL_HAWK_POP"] + params["INITIAL_DOVE_POP"] == 0:
            self.show_error("Initial population must be greater than zero.")
            return False
        if params["SELECTION_TEMP"] <= 0:
            self.show_error("Selection temperature must be positive.")
            return False
        return True

    def show_error(self, message):
        QMessageBox.warning(self, "Invalid Parameters", message)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
    def go_back(self):
        self.stop_simulation()
        self.hide()
        self.start_page.show()

    def close_app(self):
        self.stop_simulation()
        self.close()

    # ------------------------------------------------------------------
    # Simulation control
    # ------------------------------------------------------------------
    def run_simulation(self):
        if self.sim_running:
            return

        try:
            params = self.read_params()
        except ValueError:
            self.show_error("One or more parameters are not valid numbers.")
            return

        if not self.validate_params(params):
            return

        self.frames_per_generation_value = params["FRAMES_PER_GENERATION"]

        # Recreate the world with the new params and rebind the plots
        try:
            self.world = self.build_world(params)
        except ValueError as e:
            # initial populations exceed the available non-rock tiles
            self.show_error(str(e))
            return
        self.time_series_tab.set_world(self.world)
        # self.phase_plot_tab.set_world(self.world)

        self.run_button.setEnabled(False)
        self.sim_status_label.setText("Simulation: Running")

        screen = pg.display.set_mode((SIM_WINDOW_WIDTH, SIM_WINDOW_HEIGHT), pg.RESIZABLE)
        pg.display.set_caption("Hawk-Dove Simulation")

        self.sim_game = HDGame(screen, params, world=self.world)
        self.sim_game.world = self.world

        self.sim_timer = QTimer(self)
        self.sim_timer.timeout.connect(self.step_simulation)
        self.sim_timer.start(TIMER_AMNT)

        self.sim_running = True
        self.sim_paused = False
        self.last_update_time = perf_counter()

        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.pause_button.setText("Pause")
        self.update_button_colors()

    def step_simulation(self):
        if not self.sim_game:
            return

        # Time-based generation update (frames_per_generation at 60 FPS)
        now = perf_counter()
        seconds_per_gen = self.frames_per_generation_value / 60
        if now - self.last_update_time >= seconds_per_gen:
            self.world.update()
            self.last_update_time = now

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.stop_simulation()
                return

        if self.sim_game:
            self.sim_game.update([])
            self.sim_game.draw()
            self.update_plots()

    def update_plots(self):
        self.time_series_tab.refresh_plot()
        # self.phase_plot_tab.refresh_plot()

    def toggle_pause(self):
        if not self.sim_running:
            return

        if self.sim_paused:
            self.sim_timer.start(TIMER_AMNT)
            self.pause_button.setText("Pause")
            self.sim_status_label.setText("Simulation: Running")
            self.sim_paused = False
        else:
            self.sim_timer.stop()
            self.pause_button.setText("Resume")
            self.sim_status_label.setText("Simulation: Paused")
            self.sim_paused = True

        self.update_button_colors()

    def stop_simulation(self):
        # Safe to call when nothing is running (e.g. from Back / Close)
        if not self.sim_running and self.sim_timer is None:
            return

        if self.sim_timer is not None:
            self.sim_timer.stop()
            try:
                self.sim_timer.timeout.disconnect(self.step_simulation)
            except (TypeError, RuntimeError):
                pass
            self.sim_timer.deleteLater()
            self.sim_timer = None

        self.sim_game = None
        self.sim_running = False
        self.sim_paused = False
        self.sim_status_label.setText("Simulation: Not running")
        pg.display.quit()

        self.update_plots()

        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.pause_button.setText("Pause")
        self.run_button.setEnabled(True)
        self.update_button_colors()

    def closeEvent(self, event):
        self.stop_simulation()
        super().closeEvent(event)

    # ------------------------------------------------------------------
    # Styling
    # ------------------------------------------------------------------
    def update_button_colors(self):
        # Run button
        if self.sim_running:
            self.run_button.setStyleSheet("background-color: gray; color: white;")
        else:
            self.run_button.setStyleSheet("background-color: green; color: white;")

        # Pause button
        if self.sim_paused:
            self.pause_button.setStyleSheet("background-color: orange; color: white;")
        elif self.sim_running:
            self.pause_button.setStyleSheet("background-color: yellow; color: black;")
        else:
            self.pause_button.setStyleSheet("background-color: gray; color: white;")

        # Stop button
        if self.sim_running:
            self.stop_button.setStyleSheet("background-color: red; color: white;")
        else:
            self.stop_button.setStyleSheet("background-color: gray; color: white;")