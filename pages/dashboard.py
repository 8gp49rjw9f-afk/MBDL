from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titre = QLabel(
            "Tableau de bord"
        )

        titre.setStyleSheet(
            "font-size: 28px;"
        )

        layout.addWidget(titre)

        texte = QLabel(
            "Bienvenue dans Mon Financier"
        )

        layout.addWidget(texte)

        self.setLayout(layout)