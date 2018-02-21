# Misc
import time
import hashlib
import sys

# PIL
from PIL import Image, ImageQt

# Pygame
import pygame
import pygame.camera

# Pyqt5
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMainWindow, QLabel
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage, QFont

# My imports
from graph import DotGraph, LineGraph


# Statics
CAM_SIZE = (1920, 1080)  # Urlab cam
SCREEN_RESOLUTION = (1920, 1080)
CAMERA_INTERVAL = 5  # How often image will be read from cam (milliseconds)


def crunch_image(image):
    # More magic to be inserted here at a later date
    hasher = hashlib.sha256()
    hasher.update(image.tobytes())

    return hasher.hexdigest()


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_UI()
        self.show()

    def init_UI(self):
        self.setWindowTitle("PDS CAMERA")
        self.dot_graph_shown = True

        # Information showers
        self.camera_feed = LiveSteamLabel(self)
        self.number_dispay = NumberLabel(self)
        self.image_still = CapturedPhotoLabel(self)
        self.line_graph = LineGraph(self)
        self.dot_graph = DotGraph(self)

        # Buttons
        self.capture_button = QPushButton("Capture current image", self)
        self.capture_button.clicked.connect(self._update_labels)
        self.toggle_button = QPushButton("Toggle other graph", self)
        self.toggle_button.clicked.connect(self._switch_graphs)

        self._create_layout()

    def _switch_graphs(self):
        if self.dot_graph_shown:
            self.dot_graph_shown = False
            self.dot_graph.hide()
            self.line_graph.show()
        else:
            self.dot_graph_shown = True
            self.line_graph.hide()
            self.dot_graph.show()

    def _update_labels(self):
        # try:
        img = self.camera_feed.get_current_image()
        new_string = crunch_image(img)

        self.image_still.update(img)
        self.number_dispay.update(new_string)
        self.line_graph.addvalue(int(new_string, 16) % 100)
        self.dot_graph.addvalue(int(new_string, 16) % 100)
        # finally:
        #     QtCore.QTimer.singleShot(5, self._update_labels)

    def _create_layout(self):
        self.setGeometry(0, 0, *SCREEN_RESOLUTION)

        main_grid = QGridLayout()
        self.setLayout(main_grid)

        main_grid.setGeometry(QtCore.QRect(0, 0, *SCREEN_RESOLUTION))
        main_grid.setSpacing(10)

        main_grid.addWidget(self.camera_feed, 1, 1)
        main_grid.addWidget(self.line_graph, 1, 2)
        main_grid.addWidget(self.dot_graph, 1, 2)
        main_grid.addWidget(self.image_still, 3, 1)
        main_grid.addWidget(self.number_dispay, 3, 2)

        self.line_graph.hide()
        self._create_button_grid(main_grid)

    def _create_button_grid(self, main_grid):
        button_grid = QGridLayout()
        main_grid.addLayout(button_grid, 2, 2)

        button_grid.addWidget(self.capture_button, 1, 1)
        button_grid.addWidget(self.toggle_button, 1, 2)


class NumberLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFont(QFont("Comic Sans", 20, QFont.Bold))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText("Random number:\n4")  # https://xkcd.com/221/

    def update(self, new_string):
        self.setText("Random number:\n"+new_string)


class CapturedPhotoLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(*LIVESTREAM_LABEL_SIZE)
        self.update(Image.open("placeholder.jpg").convert(mode="RGBA"))

    def update(self, image):
        self.current_image = image
        img = self.current_image.copy()
        img = img.resize(LIVESTREAM_LABEL_SIZE)
        qt_image = ImageQt.ImageQt(img)
        self.setPixmap(QPixmap.fromImage(qt_image))


class LiveSteamLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.update_it()
        self.setFixedSize(*LIVESTREAM_LABEL_SIZE)
        self.show()

    def get_new_pixmap(self):
        camera_image = camera.get_image()

        pil_string_image = pygame.image.tostring(camera_image, "RGBA", False)
        pil_image = Image.frombytes("RGBA", CAM_SIZE, pil_string_image)
        self.current_image = pil_image.copy()

        pil_image = pil_image.resize(LIVESTREAM_LABEL_SIZE)
        qt_image = ImageQt.ImageQt(pil_image)

        return QPixmap.fromImage(qt_image)

    def get_current_image(self):
        return self.current_image

    def update_it(self):
        try:
            self.setPixmap(self.get_new_pixmap())
        finally:
            QtCore.QTimer.singleShot(CAMERA_INTERVAL, self.update_it)


if __name__ == '__main__':
    # Pygame magic setup
    pygame.init()
    pygame.camera.init()

    all_cams = pygame.camera.list_cameras()
    camera = pygame.camera.Camera(all_cams[-1], CAM_SIZE)
    camera.start()

    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    LIVESTREAM_LABEL_SIZE = (width // 2 - 50, height // 2 - 50)

    main_window = MainWindow()
    sys.exit(app.exec_())
