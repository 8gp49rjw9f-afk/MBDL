from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
)



class SeparateurDialog(QDialog):

    def __init__(
        self,
        nom="",
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Séparateur"
        )


        self.resize(
            350,
            160
        )


        layout = QVBoxLayout()



        titre = QLabel(
            "Nom du séparateur"
        )

        titre.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )


        layout.addWidget(
            titre
        )



        self.nom = QLineEdit()


        self.nom.setText(
            str(nom)
        )


        self.nom.setPlaceholderText(
            "Ex: Revenus 2026"
        )


        layout.addWidget(
            self.nom
        )



        boutons = QHBoxLayout()


        annuler = QPushButton(
            "Annuler"
        )


        sauvegarder = QPushButton(
            "Sauvegarder"
        )


        boutons.addWidget(
            annuler
        )

        boutons.addWidget(
            sauvegarder
        )


        layout.addLayout(
            boutons
        )


        annuler.clicked.connect(
            self.reject
        )

        sauvegarder.clicked.connect(
            self.accept
        )


        self.setLayout(
            layout
        )
