
from PyQt5.QtWidgets import QSplashScreen, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, QByteArray

from svg_data import *


class Manager_Splash_Screen(QSplashScreen):
    def __init__(self):

        self.splash_pix = QPixmap(250, 300)
        self.splash_pix.fill(QColor(251, 246, 226))
        super().__init__(self.splash_pix, Qt.WindowStaysOnTopHint)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.label = QLabel()
        space = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setPixmap(self.pixmap_setup(self.svg_data()))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout_label = QHBoxLayout()
        layout_label.setContentsMargins(0, 0, 0, 0)
        layout_label.setSpacing(0)
        layout_label.addItem(space)
        layout_label.addWidget(self.label)
        layout_label.addItem(space)
        layout.addLayout(layout_label)

        self.showMessage('加载 pip 环境', Qt.AlignBottom | Qt.AlignCenter, QColor(19, 24, 66))
        self.show()

    def pixmap_setup(self, icon_code: str):
        '''
        设置pixmap

        参数:
            Icon_code: SVG 的源码(str)
        '''
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(icon_code.encode()))
        return pixmap

    def close_splash_screen(self, widget):
        self.finish(widget)

    def show_message(self, message: str):
        self.showMessage(str(message), Qt.AlignBottom | Qt.AlignCenter, QColor(19, 24, 66))
        # time.sleep(1)

    def svg_data(self):
        return MAIN_ICON
