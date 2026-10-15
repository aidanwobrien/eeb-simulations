from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser
from PySide6.QtCore import Qt
from settings import HAWK_DOVE_TEXT

class DescriptionWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Title label
        self.label = QLabel("Description")
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold;")

        # Static text
        self.static_text = QLabel(HAWK_DOVE_TEXT)
        self.static_text.setWordWrap(True)
        self.static_text.setAlignment(Qt.AlignJustify)
        self.static_text.setTextFormat(Qt.RichText)
        self.static_text.setStyleSheet("font-size: 14px; line-height: 1.5;")

        # QTextBrowser for links
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setStyleSheet("font-size: 14px; line-height: 1.5;")

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.static_text)
        layout.addWidget(self.text_browser)

    def set_text(self, label, static_text, html_text):
        self.label.setText(label)
        self.static_text.setText(static_text)
        if html_text:
            self.text_browser.setHtml(html_text)

    def load_url(self, url: str):
        self.text_browser.setSource(url)
