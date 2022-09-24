import sys
import calculator
from PyQt5.QtWidgets import QApplication

# main runner class that instances a new
# calculator class, then shows it.
def main():
    app = QApplication(sys.argv)
    calc_instance = calculator.Calculator()
    calc_instance.show()
    app.exec_()


main()
