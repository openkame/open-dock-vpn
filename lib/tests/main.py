from PySide6.QtWidgets import QApplication, QWidget
import sys
from kappcontroller import KAppController


if __name__ == "__main__":
    app = QApplication([])
    controller = KAppController()
    sys.exit(app.exec())


