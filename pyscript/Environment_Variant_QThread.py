
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess


class Environment_Variant_QThread(QThread):
    signal_finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        subprocess.run('rundll32 sysdm.cpl,EditEnvironmentVariables')
        self.signal_finished.emit()
