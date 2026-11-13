from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout
)



class EntreeEditDialog(QDialog):

    def __init__(
        self,
        nom,
        montant
    ):

        super().__init__()


        self.setWindowTitle(
            "Modifier une entrée"
        )


        self.resize(
            350,
            200
        )


        layout = QVBoxLayout()



        titre = QLabel(
            "Modifier l'entrée"
        )


        titre.setStyleSheet(
            "font-size:20px;font-weight:bold;"
        )


        layout.addWidget(
            titre
        )



        self.nom = QLineEdit()


        self.nom.setText(
            str(nom)
        )


        layout.addWidget(
            self.nom
        )



        self.montant = QLineEdit()


        self.montant.setText(
            str(montant)
        )


        layout.addWidget(
            self.montant
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



        sauvegarder.clicked.connect(
            self.accept
        )


        annuler.clicked.connect(
            self.reject
        )


        self.setLayout(
            layout
        )