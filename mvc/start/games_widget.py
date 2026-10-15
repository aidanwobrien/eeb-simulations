import sys
from PySide6.QtWidgets import QVBoxLayout, QWidget, QListWidget, QLabel, QPushButton
from PySide6.QtCore import Qt

class GamesWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.label = QLabel("Select a game:")
        layout.addWidget(self.label)

        self.list_widget = QListWidget()
        self.list_widget.addItems([
            "Hawk-Dove",
            "Lotka-Volterra"
        ])

        self.select_button = QPushButton("Select")

        layout.addWidget(self.list_widget)
        layout.addWidget(self.select_button)

        self.setLayout(layout)
