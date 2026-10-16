import sys

from PyQt6.QtWidgets import QApplication

from core.app import HarshOSApp


def main():
    qt_app = QApplication(sys.argv)

    app = HarshOSApp()
    app.start()

    sys.exit(qt_app.exec())


if __name__ == "__main__":
    main()