import os
import httpx
from dotenv import load_dotenv
from json import dump, load
from pathlib import Path
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QPushButton, QScrollArea, QLabel

CACHE_FILE = Path(__file__).resolve().parent/"cache.json"
cache = {}
try:
    with open(CACHE_FILE, "r") as f:
        cache = load(f)
except FileNotFoundError:
    print("No cached file. Making one now.")

class NewsEntry(QWidget):
    def __init__(self, author: str | None = None, title: str | None = None, description: str | None = None, link: str | None = None):
        super().__init__()

        layout = QVBoxLayout(self)

        self.author = QLabel(f"Author: {author}" or "No Author")
        self.title = QLabel(f"Title: {title}" or "No Title")
        self.description = QLabel(f"Description: {description}" or "No Description")
        self.link = QLabel(f"Link: {link}" or "No Link")

        layout.addWidget(self.author)
        layout.addWidget(self.title)
        layout.addWidget(self.description)
        layout.addWidget(self.link)

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("News App")

        centralLayout = QVBoxLayout()
        centralPanel = QWidget()
        centralPanel.setLayout(centralLayout)

        topLayout = QHBoxLayout()
        topPanel = QWidget()
        topPanel.setLayout(topLayout)
        centralLayout.addWidget(topPanel)

        bottomLayout = QVBoxLayout()
        bottomPanel = QWidget()
        bottomPanel.setLayout(bottomLayout)
        centralLayout.addWidget(bottomPanel)

        self.button = QPushButton("Load sources")
        self.button.clicked.connect(self.clicked)
        topLayout.addWidget(self.button)

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        bottomLayout.addWidget(scrollArea)
        container = QWidget()
        self.newsItems = QVBoxLayout(container)
        #self.newsItems.addStretch()
        scrollArea.setWidget(container)

        # this as the method name implies, sets the window to be a fixed size meaning you cannot resize it
        # QSize is used that accepts a width and height in this case it's in pixels
        self.setFixedSize(QSize(400, 300))

        self.setCentralWidget(centralPanel)

    def clicked(self):
        data = fetch()
        for i in range(len(data)):
            self.newsItems.addWidget(NewsEntry(data[i]["author"], data[i]["title"], data[i]["description"], data[i]["url"]))

def fetch(url: str = "https://api.apilayer.net/mediastack/v1/news"):
    global cache
    params = {
            "access_key": os.getenv("API_KEY"),
            "countries": "us",
            "limit": "100",
            "offset": "0",
            }
    r = httpx.get(url, params=params)
    with open(CACHE_FILE, "w") as f:
        dump(r.json(), f, indent = 2)
    with open(CACHE_FILE, "r") as f:
        cache = load(f)
    ls = list(cache["data"])
    return ls

def main():
    load_dotenv()

    app = QApplication([])
    window = MainWindow()
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
