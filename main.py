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
from PyQt5.QtGui import QPixmap, QImage


# Statics
CAM_SIZE = (1920, 1080) # Urlab cam
CAMERA_INTERVAL = 5 # How often image will be read from cam (milliseconds)
LIVESTREAM_LABEL_SIZE = (1200, 720)


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_UI()
        self.show()

    def init_UI(self):
        self.setWindowTitle("PDS CAMERA")

        self.camera_feed = LiveSteamLabel(self)
        self.image_still = CapturedPhotoLabel(self.camera_feed, self)

        self._create_layout()

    def _create_layout(self):
        self.setGeometry(0, 0, 1920, 1080)

        main_grid = QGridLayout()
        self.setLayout(main_grid)
        main_grid.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        main_grid.setSpacing(10)

        main_grid.addWidget(self.camera_feed, 1, 1)
        main_grid.addWidget(self.image_stil, 2, 1)


    def _create_button_grid(self):
        return


class CapturedPhotoLabel(QLabel):
    def __init__(self, livestream, parent=None):
        super().__init__(parent)
        self.livestream = livestream


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
    main_window = MainWindow()
    sys.exit(app.exec_())