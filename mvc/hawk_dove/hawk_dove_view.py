from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class HawkDoveWindow(QWidget):
    def __init__(self, start_page):
        super().__init__()
        self.start_page = start_page
        self.setWindowTitle("Hawk-Dove Window")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        self.label = QLabel("Welcome to the Hawk-Dove Simulation")
        layout.addWidget(self.label)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)



    def go_back(self):
        self.hide()
        self.start_page.show()
