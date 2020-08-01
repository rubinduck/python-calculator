"""
Module launching GUI
"""


from PyQt5.QtWidgets import QApplication

from gui import CalculatorMainWindow


def main():
    app = QApplication([])
    window = CalculatorMainWindow()
    window.resize(window.minimumSize())
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
