from PyQt5.QtWidgets import QApplication
import sys
from interface.window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.showMaximized()
    sys.exit(app.exec_())