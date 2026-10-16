from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFormLayout, QTabWidget, QScrollArea, QGroupBox,
    QSplitter, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
import multiprocessing
# from mvc.start.pg_runner import run_lotka_volterra
from mvc.lotka_volterra.plot_tab import PlotTab
from mvc.lotka_volterra.phase_plot_tab import PhasePlotTab
from games.lotka_volterra.world import World
import pygame as pg
from games.lotka_volterra.game import Game as LVGame
from games.lotka_volterra.settings import GRID_X, GRID_Y, SIM_WINDOW_HEIGHT, SIM_WINDOW_WIDTH
from settings import APP_WINDOW_WIDTH, APP_WINDOW_HEIGHT
import pygame as pg
from time import perf_counter

TIMER_AMNT = 1

class LotkaVolterraWindow(QWidget):
    def __init__(self, start_page):
        super().__init__()
        pg.init()
        self.start_page = start_page
        self.setWindowTitle("Lotka Volterra Game")
        self.resize(APP_WINDOW_WIDTH, APP_WINDOW_HEIGHT)

        self.sim_timer = None
        self.sim_game = None
        self.sim_running = False
        self.sim_paused = False
        self.last_update_time = perf_counter()

        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.sim_status_label = QLabel("Simulation: Not running")

        self.time_step = QLineEdit("0.1")
        self.grid_x = QLineEdit("100")
        self.grid_y = QLineEdit("100")
        self.initial_prey_pop = QLineEdit("200")
        self.initial_predator_pop = QLineEdit("20")
        self.frames_per_generation = QLineEdit("1")
        self.perlin_scale = QLineEdit("18")
        self.perlin_noise_scale = QLineEdit("9")

        self.h_init = QLineEdit("10")
        self.h_move_cost = QLineEdit("0.1")
        self.h_basal_cost = QLineEdit("1")
        self.h_food_gain = QLineEdit("5")
        self.h_food_wait = QLineEdit("1")
        self.h_repro_th = QLineEdit("20")
        self.h_repro_cost = QLineEdit("7")
        self.prey_birth_rate = QLineEdit("0.4")

        self.p_init = QLineEdit("30")
        self.p_move_cost = QLineEdit("2")
        self.p_basal_cost = QLineEdit("1")
        self.p_food_gain = QLineEdit("8")
        self.p_food_wait = QLineEdit("2")
        self.p_repro_th = QLineEdit("70")
        self.p_repro_cost = QLineEdit("10")
        self.predation_rate = QLineEdit("0.01")
        self.predator_mortality_rate = QLineEdit("0.1")
        self.predator_fitness_gain_rate = QLineEdit("0.2")

        food_group = QGroupBox("World / Food Parameters")
        food_layout = QFormLayout()
        self.initial_food_pop_rate = QLineEdit("0.5")
        self.food_regrow = QLineEdit("20")
        # food_layout.addRow("Time step:", self.time_step)
        food_layout.addRow("Initial prey population:", self.initial_prey_pop)
        food_layout.addRow("Initial predator population:", self.initial_predator_pop)
        food_layout.addRow("Grid Width:", self.grid_x)
        food_layout.addRow("Grid Height:", self.grid_y)
        food_layout.addRow("Frames per generation:", self.frames_per_generation)
        food_layout.addRow("Perlin scale:", self.perlin_scale)
        food_layout.addRow("Perlin noise scale:", self.perlin_noise_scale)
        food_layout.addRow("Initial food population rate (% / 100):", self.initial_food_pop_rate)
        food_layout.addRow("Food regrow rate (frames):", self.food_regrow)
        food_group.setLayout(food_layout)
        scroll_layout.addWidget(food_group)

        h_group = QGroupBox("Herbivore Parameters")
        h_layout = QFormLayout()

        h_layout.addRow("Initial herbivore energy:", self.h_init)
        h_layout.addRow("Move cost:", self.h_move_cost)
        h_layout.addRow("Basal cost:", self.h_basal_cost)
        h_layout.addRow("Food gain:", self.h_food_gain)
        h_layout.addRow("Food wait:", self.h_food_wait)
        h_layout.addRow("Reproduction threshold:", self.h_repro_th)
        h_layout.addRow("Reproduction cost:", self.h_repro_cost)
        h_layout.addRow("Prey birth rate:", self.prey_birth_rate)
        h_group.setLayout(h_layout)
        scroll_layout.addWidget(h_group)

        p_group = QGroupBox("Predator Parameters")
        p_layout = QFormLayout()

        p_layout.addRow("Initial predator energy:", self.p_init)
        p_layout.addRow("Move cost:", self.p_move_cost)
        p_layout.addRow("Basal cost:", self.p_basal_cost)
        p_layout.addRow("Food gain:", self.p_food_gain)
        p_layout.addRow("Food wait:", self.p_food_wait)
        p_layout.addRow("Reproduction threshold:", self.p_repro_th)
        p_layout.addRow("Reproduction cost:", self.p_repro_cost)
        p_layout.addRow("Predation rate:", self.predation_rate)
        p_layout.addRow("Predator mortality rate:", self.predator_mortality_rate)
        p_layout.addRow("Predator fitness gain rate:", self.predator_fitness_gain_rate)

        p_group.setLayout(p_layout)
        scroll_layout.addWidget(p_group)

        # sim_group = QGroupBox("Population & Simulation Parameters")
        # sim_layout = QFormLayout()
        # sim_group.setLayout(sim_layout)
        # scroll_layout.addWidget(sim_group)

        self.grid_x_value = int(self.grid_x.text())
        self.grid_y_value = int(self.grid_y.text())
        self.initial_food_pop_rate_value = float(self.initial_food_pop_rate.text())
        self.food_regrow_value = float(self.food_regrow.text())

        self.h_init_value = float(self.h_init.text())
        self.h_move_cost_value = float(self.h_move_cost.text())
        self.h_basal_cost_value = float(self.h_basal_cost.text())
        self.h_food_gain_value = float(self.h_food_gain.text())
        self.h_food_wait_value = float(self.h_food_wait.text())
        self.h_repro_th_value = float(self.h_repro_th.text())
        self.h_repro_cost_value = float(self.h_repro_cost.text())

        self.p_init_value = float(self.p_init.text())
        self.p_move_cost_value = float(self.p_move_cost.text())
        self.p_basal_cost_value = float(self.p_basal_cost.text())
        self.p_food_gain_value = float(self.p_food_gain.text())
        self.p_food_wait_value = float(self.p_food_wait.text())
        self.p_repro_th_value = float(self.p_repro_th.text())
        self.p_repro_cost_value = float(self.p_repro_cost.text())

        self.prey_birth_rate_value = float(self.prey_birth_rate.text())
        self.predation_rate_value = float(self.predation_rate.text())
        self.predator_mortality_rate_value = float(self.predator_mortality_rate.text())
        self.predator_fitness_gain_rate_value = float(self.predator_fitness_gain_rate.text())
        self.initial_prey_pop_value = int(self.initial_prey_pop.text())
        self.initial_predator_pop_value = int(self.initial_predator_pop.text())
        self.time_step_value = float(self.time_step.text())
        self.frames_per_generation_value = int(self.frames_per_generation.text())
        self.perlin_scale_value = float(self.perlin_scale.text())
        self.perlin_noise_scale_value = float(self.perlin_noise_scale.text())



        scroll.setWidget(scroll_content)

        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)

        bottom_button_widget = QWidget()
        bottom_button_layout = QHBoxLayout(bottom_button_widget)

        self.pause_button = QPushButton("Pause")
        self.pause_button.setEnabled(False)
        self.pause_button.clicked.connect(self.toggle_pause)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_simulation)

        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_simulation)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close_app)

        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)

        self.tabs = QTabWidget()
        # self.pygame_tab = QLabel("Pygame simulation will appear here")
        # self.pygame_tab.setAlignment(Qt.AlignCenter)
        # self.pygame_tab.setStyleSheet("border: 1px solid gray; color: gray; font-size: 14px;")
        # self.tabs.addTab(self.pygame_tab, "Simulation")

        # Create a "world" instance but do not start Pygame yet
        self.world = World(None, SIM_WINDOW_WIDTH, SIM_WINDOW_HEIGHT,
                        self.grid_x_value,
                        self.grid_y_value,
                        self.initial_food_pop_rate_value,
                        self.food_regrow_value,
                        self.h_init_value,
                        self.h_move_cost_value,
                        self.h_basal_cost_value,
                        self.h_food_gain_value,
                        self.h_food_wait_value,
                        self.h_repro_th_value,
                        self.h_repro_cost_value,
                        self.p_init_value,
                        self.p_move_cost_value,
                        self.p_basal_cost_value,
                        self.p_food_gain_value,
                        self.p_food_wait_value,
                        self.p_repro_th_value,
                        self.p_repro_cost_value,
                        self.prey_birth_rate_value,
                        self.predation_rate_value,
                        self.predator_mortality_rate_value,
                        self.predator_fitness_gain_rate_value,
                        self.initial_prey_pop_value,
                        self.initial_predator_pop_value,
                        self.time_step_value,
                        self.frames_per_generation_value,
                        self.perlin_scale_value,
                        self.perlin_noise_scale_value
                        )

        # Embed the actual plot widgets
        self.time_series_tab = PlotTab(self.world, GRID_X, GRID_Y)
        self.phase_plot_tab = PhasePlotTab(self.world, GRID_X, GRID_Y)

        self.tabs.addTab(self.time_series_tab, "Time Series")
        self.tabs.addTab(self.phase_plot_tab, "Phase Plot")
        self.tabs.setCurrentWidget(self.time_series_tab)

        bottom_button_layout.addWidget(self.back_button)
        bottom_button_layout.addWidget(self.close_button)


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

    def go_back(self):
        self.stop_simulation()
        self.hide()
        self.start_page.show()

    def run_simulation(self):
        params = {
            "INITIAL_FOOD_POP_RATE": float(self.initial_food_pop_rate.text()),
            "FOOD_REGROW": float(self.food_regrow.text()),
            "GRID_X": int(self.grid_x.text()),
            "GRID_Y": int(self.grid_y.text()),
            "H_INIT": float(self.h_init.text()),
            "H_MOVE_COST": float(self.h_move_cost.text()),
            "H_BASAL_COST": float(self.h_basal_cost.text()),
            "H_FOOD_GAIN": float(self.h_food_gain.text()),
            "H_FOOD_WAIT": float(self.h_food_wait.text()),
            "H_REPRO_TH": float(self.h_repro_th.text()),
            "H_REPRO_COST": float(self.h_repro_cost.text()),
            "P_INIT": float(self.p_init.text()),
            "P_MOVE_COST": float(self.p_move_cost.text()),
            "P_BASAL_COST": float(self.p_basal_cost.text()),
            "P_FOOD_GAIN": float(self.p_food_gain.text()),
            "P_FOOD_WAIT": float(self.p_food_wait.text()),
            "P_REPRO_TH": float(self.p_repro_th.text()),
            "P_REPRO_COST": float(self.p_repro_cost.text()),
            "PREY_BIRTH_RATE": float(self.prey_birth_rate.text()),
            "PREDATION_RATE": float(self.predation_rate.text()),
            "PREDATOR_MORTALITY_RATE": float(self.predator_mortality_rate.text()),
            "PREDATOR_FITNESS_GAIN_RATE": float(self.predator_fitness_gain_rate.text()),
            "INITIAL_PREY_POP": int(self.initial_prey_pop.text()),
            "INITIAL_PREDATOR_POP": int(self.initial_predator_pop.text()),
            "TIME_STEP": float(self.time_step.text()),
            "FRAMES_PER_GENERATION": int(self.frames_per_generation.text()),
            "PERLIN_SCALE": float(self.perlin_scale.text()),
            "PERLIN_NOISE_SCALE": float(self.perlin_noise_scale.text())
        }

        # Recreate the world with the new params
        self.world = World(None, SIM_WINDOW_WIDTH, SIM_WINDOW_HEIGHT,
                        params["GRID_X"],
                        params["GRID_Y"],
                        params["INITIAL_FOOD_POP_RATE"],
                        params["FOOD_REGROW"],
                        params["H_INIT"],
                        params["H_MOVE_COST"],
                        params["H_BASAL_COST"],
                        params["H_FOOD_GAIN"],
                        params["H_FOOD_WAIT"],
                        params["H_REPRO_TH"],
                        params["H_REPRO_COST"],
                        params["P_INIT"],
                        params["P_MOVE_COST"],
                        params["P_BASAL_COST"],
                        params["P_FOOD_GAIN"],
                        params["P_FOOD_WAIT"],
                        params["P_REPRO_TH"],
                        params["P_REPRO_COST"],
                        params["PREY_BIRTH_RATE"],
                        params["PREDATION_RATE"],
                        params["PREDATOR_MORTALITY_RATE"],
                        params["PREDATOR_FITNESS_GAIN_RATE"],
                        params["INITIAL_PREY_POP"],
                        params["INITIAL_PREDATOR_POP"],
                        params["TIME_STEP"],
                        params["FRAMES_PER_GENERATION"],
                        params["PERLIN_SCALE"],
                        params["PERLIN_NOISE_SCALE"])

        # Update plot tabs
        self.time_series_tab.set_world(self.world)
        self.phase_plot_tab.set_world(self.world)

        self.run_lotka_volterra(params)



    def run_lotka_volterra(self, params):

        if self.validate_params():

            if self.sim_running:
                return  # already running

            self.run_button.setEnabled(False)

            self.sim_status_label.setText("Simulation: Running")
            screen = pg.display.set_mode((SIM_WINDOW_WIDTH, SIM_WINDOW_HEIGHT), pg.RESIZABLE)
            pg.display.set_caption("Lotka–Volterra Simulation")

            self.sim_game = LVGame(screen, params)
            self.sim_game.world = self.world

            self.sim_timer = QTimer(self)
            self.sim_timer.timeout.connect(self.step_simulation)
            self.sim_timer.start(TIMER_AMNT)

            self.sim_running = True
            self.sim_paused = False
            self.update_button_colors()

            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            self.pause_button.setText("Pause")
            self.last_update_time = perf_counter()
        else:
            return
            # self.show_error_dialog("Initial populations exceed the world size!")

    def validate_params(self):
        """Check if initial prey and predator populations fit on non-rock tiles."""
        try:
            current_prey = int(self.initial_prey_pop.text())
            current_predator = int(self.initial_predator_pop.text())
            grid_x = int(self.grid_x.text())
            grid_y = int(self.grid_y.text())
        except ValueError:
            return False  # invalid input in the QLineEdits

        # Count how many non-rock tiles exist
        non_rock_tiles = sum(
            1
            for row in range(self.world.rows)
            for col in range(self.world.cols)
            if (row, col) not in getattr(self.world, "rocks", set())
        )

        total_requested = current_prey + current_predator

        if total_requested > non_rock_tiles:
            # Optionally, show a message to the user
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(
                self,
                "Too many agents",
                f"Initial prey + predator population ({total_requested}) "
                f"exceeds the number of available non-rock tiles ({non_rock_tiles})."
            )
            return False

        return True


    def update_plots(self):
        self.time_series_tab.refresh_plot()
        self.phase_plot_tab.refresh_plot()


    def step_simulation(self):
        if not self.sim_game:
            return

        # --- 1) Time-based generation update ---
        now = perf_counter()
        seconds_per_gen = self.frames_per_generation_value / 60  # user input in frames at 60 FPS
        if now - self.last_update_time >= seconds_per_gen:
            self.world.update()  # advance one generation
            self.last_update_time = now

        # --- 2) Handle pygame events (prevent closing if desired) ---
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.stop_simulation()
                return


        if self.sim_game: 
            self.sim_game.update([])
            self.sim_game.draw()
            self.update_plots()

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
        if self.sim_timer is None:
            return
        self.sim_timer.stop()
        self.sim_status_label.setText("Simulation: Not Running")
        try:
            self.sim_timer.timeout.disconnect(self.step_simulation)
        except TypeError:
            pass  # already disconnected
        self.sim_timer.deleteLater()
        self.sim_timer = None

        self.sim_game = None
        self.sim_running = False
        self.sim_paused = False
        self.update_button_colors()
        pg.display.quit()

        self.time_series_tab.refresh_plot()
        self.phase_plot_tab.refresh_plot()

        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.pause_button.setText("Pause")
        self.run_button.setEnabled(True)

    def close_app(self):
        if self.sim_running:
            self.stop_simulation()
            self.close()
        else:
            self.close()

    # def show_error_dialog(self, message):
    #     msg_box = QMessageBox(self)
    #     msg_box.setIcon(QMessageBox.Warning)
    #     msg_box.setWindowTitle("Invalid Parameters")
    #     msg_box.setText(message)
    #     msg_box.setStandardButtons(QMessageBox.Ok)
    #     msg_box.exec()

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
