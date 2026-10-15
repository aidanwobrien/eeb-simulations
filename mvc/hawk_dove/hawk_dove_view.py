from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFormLayout, QTabWidget, QScrollArea, QGroupBox,
    QSplitter, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
import multiprocessing
from games.hawk_dove.world import World
import pygame as pg
from games.hawk_dove.game import Game as LVGame
from games.hawk_dove.settings import GRID_X, GRID_Y, SIM_WINDOW_HEIGHT, SIM_WINDOW_WIDTH
from settings import APP_WINDOW_WIDTH, APP_WINDOW_HEIGHT
import pygame as pg
from time import perf_counter


TIMER_AMNT = 1

class HawkDoveWindow(QWidget):
    def __init__(self, start_page):
        super().__init__()
        self.start_page = start_page
        self.setWindowTitle("Hawk-Dove Window")
        self.resize(APP_WINDOW_WIDTH, APP_WINDOW_HEIGHT)

        self.sim_timer = None
        self.sim_game = None
        self.sim_running = False
        self.sim_paused = False
        self.last_update_time = perf_counter()

        main_layout = QVBoxLayout(self)

        self.label = QLabel("Welcome to the Hawk-Dove Simulation")
        main_layout.addWidget(self.label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.sim_status_label = QLabel("Simulation: Not running")

        self.time_step = QLineEdit("0.1")
        self.grid_x = QLineEdit("100")
        self.grid_y = QLineEdit("100")

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        main_layout.addWidget(self.back_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close_app)
        main_layout.addWidget(self.close_button)

    def go_back(self):
        self.hide()
        self.start_page.show()

    def run_simulation(self):
        # Placeholder for simulation logic
        self.label.setText("Running Hawk-Dove Simulation...")

    def validate_params(self):
        # Placeholder for parameter validation logic
        return True

    def update_plots(self):
        # Placeholder for plot updating logic
        pass

    def step_simulation(self):
        # Placeholder for stepping through the simulation
        pass

    def toggle_pause(self):
        # Placeholder for toggling pause state
        pass

    def stop_simulation(self):
        # Placeholder for stopping the simulation
        pass

    def close_app(self):
        if self.sim_running:
            self.stop_simulation()
            self.close()
        else:
            self.close()

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

