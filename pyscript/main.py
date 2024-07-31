

from pip_manager_function import *


class Manager_Main(Manager_Function):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exe = Manager_Main()
    exe.show()
    sys.exit(app.exec_())
