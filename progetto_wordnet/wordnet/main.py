# main.py
import sys
import os
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet
from controller_model import MainController

"""
Main function to run the application
"""
def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_teal.xml")

    controller = MainController(app)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
