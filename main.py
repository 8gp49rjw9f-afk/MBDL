import os
import sys

from database import create_database

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from login import LoginWindow
from app import MainWindow


def resource_path(
    relative_path
):

    try:

        base_path = sys._MEIPASS

    except AttributeError:

        base_path = os.path.abspath(".")


    return os.path.join(
        base_path,
        relative_path
    )



fenetre_principale = None

def ouvrir_application():

    global fenetre_principale

    fenetre_principale = MainWindow()

    fenetre_principale.show()



create_database()


app = QApplication(sys.argv)


app.setApplicationName(
    "Mon bas de laine v1.41"
)


app.setWindowIcon(
    QIcon(
        resource_path("assets/Logo.png")
    )
)


login = LoginWindow(
    ouvrir_application
)


login.show()


sys.exit(
    app.exec()
)
