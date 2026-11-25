from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
)



class EntreeDialog(QDialog):

    def __init__(
        self
    ):

        super().__init__()


        self.setWindowTitle(
            "Ajouter une entrée"
        )


        self.resize(
            400,
            250
        )



        layout = QVBoxLayout()



        # =====================
        # NOM
        # =====================

        label_nom = QLabel(
            "Nom"
        )


        self.nom = QLineEdit()


        self.nom.setPlaceholderText(
            "Ex: Salaire"
        )



        layout.addWidget(
            label_nom
        )


        layout.addWidget(
            self.nom
        )



        # =====================
        # MONTANT
        # =====================

        label_montant = QLabel(
            "Montant"
        )


        self.montant = QLineEdit()


        self.montant.setPlaceholderText(
            "Ex: 3500"
        )



        layout.addWidget(
            label_montant
        )


        layout.addWidget(
            self.montant
        )



        # =====================
        # BOUTONS
        # =====================

        boutons = QHBoxLayout()


        sauvegarder = QPushButton(
            "Sauvegarder"
        )

        sauvegarder.setDefault(
            True
        )

        sauvegarder.setAutoDefault(
            True
        )

        annuler = QPushButton(
            "Annuler"
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



        self.setLayout(
            layout
        )



        sauvegarder.clicked.connect(
            self.accept
        )


        annuler.clicked.connect(
            self.reject
        )