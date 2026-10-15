import sys
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSplitter, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from mvc.start.description_widget import DescriptionWidget
from mvc.start.games_widget import GamesWidget
from settings import (
    HAWK_DOVE_LABEL, HAWK_DOVE_TEXT, HAWK_DOVE_WIKI,
    LOTKA_VOLTERRA_LABEL, LOTKA_VOLTERRA_TEXT, LOTKA_VOLTERRA_WIKI
    )
from mvc.hawk_dove.hawk_dove_view import HawkDoveWindow
from mvc.lotka_volterra.lotka_volterra_view import LotkaVolterraWindow

class StartPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Evolutionary Games")
        self.resize(800, 600)

        self.games_widget = GamesWidget()
        self.description_widget = DescriptionWidget()

        # SPLITTER
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.games_widget)
        splitter.addWidget(self.description_widget)
        splitter.setSizes([250, 550])

        # MAIN LAYOUT
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(splitter)

        # CONNECTIONS
        self.games_widget.list_widget.currentTextChanged.connect(self.on_item_selected)
        self.games_widget.select_button.pressed.connect(self.on_item_launched)

    def on_item_selected(self):
        item = self.games_widget.list_widget.currentItem()
        if not item:
            return

        text = item.text()

        if text == "Hawk-Dove":
            self.description_widget.set_text(
                label=HAWK_DOVE_LABEL,
                static_text=HAWK_DOVE_TEXT,
                html_text=HAWK_DOVE_WIKI
                )

        elif text == "Lotka-Volterra":
            self.description_widget.set_text(
                label=LOTKA_VOLTERRA_LABEL,
                static_text=LOTKA_VOLTERRA_TEXT,
                html_text=LOTKA_VOLTERRA_WIKI
                )


    
    def on_item_launched(self):
        item = self.games_widget.list_widget.currentItem()

        if not item:
            return
        
        text = item.text()

        if text == "Hawk-Dove":
            self.open_hawk_dove_window()
        elif text == "Lotka-Volterra":
            self.open_lotka_volterra_window()


            
    def open_hawk_dove_window(self):
        self.hawk_dove_window = HawkDoveWindow(self)
        self.hawk_dove_window.show()
        self.close()

    def open_lotka_volterra_window(self):
        self.lotka_volterra_window = LotkaVolterraWindow(self)
        self.lotka_volterra_window.show()
        self.close()
