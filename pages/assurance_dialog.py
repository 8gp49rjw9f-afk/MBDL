from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout
)



class AssuranceDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Ajouter une assurance"
        )


        self.resize(
            420,
            400
        )


        layout = QVBoxLayout()


        titre = QLabel(
            "Ajouter une assurance"
        )

        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(
            titre
        )


        layout.addWidget(
            QLabel(
                "Compagnie"
            )
        )


        self.compagnie = QLineEdit()

        self.compagnie.setPlaceholderText(
            "Ex: Desjardins"
        )

        layout.addWidget(
            self.compagnie
        )


        layout.addWidget(
            QLabel(
                "Nom de la police"
            )
        )


        self.nom = QLineEdit()

        self.nom.setPlaceholderText(
            "Ex: Police 12345"
        )

        layout.addWidget(
            self.nom
        )


        layout.addWidget(
            QLabel(
                "Type d'assurance"
            )
        )


        self.type_assurance = QLineEdit()

        self.type_assurance.setPlaceholderText(
            "Ex: Auto, Habitation, Voyage..."
        )

        layout.addWidget(
            self.type_assurance
        )


        layout.addWidget(
            QLabel(
                "Prime mensuelle"
            )
        )

        self.prime = QLineEdit()

        self.prime.setPlaceholderText(
            "0.00"
        )

        layout.addWidget(
            self.prime
        )


        boutons = QHBoxLayout()

        annuler = QPushButton("Annuler")

        sauvegarder = QPushButton("Sauvegarder")

        sauvegarder.setDefault(
            True
        )

        sauvegarder.setAutoDefault(
            True
        )

        boutons.addWidget(annuler)

        boutons.addWidget(sauvegarder)

        layout.addLayout(boutons)

        annuler.clicked.connect(self.reject)

        sauvegarder.clicked.connect(self.accept)

        self.setLayout(layout)



class AssuranceEditDialog(QDialog):

    def __init__(
        self,
        assurance,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Modifier une assurance"
        )


        self.resize(
            420,
            400
        )


        layout = QVBoxLayout()


        titre = QLabel(
            "Modifier l'assurance"
        )

        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(
            titre
        )


        layout.addWidget(
            QLabel(
                "Compagnie"
            )
        )


        self.compagnie = QLineEdit()

        self.compagnie.setText(
            str(assurance[1] or "")
        )

        layout.addWidget(
            self.compagnie
        )


        layout.addWidget(
            QLabel(
                "Nom de la police"
            )
        )


        self.nom = QLineEdit()

        self.nom.setText(
            str(assurance[2] or "")
        )

        layout.addWidget(
            self.nom
        )


        layout.addWidget(
            QLabel(
                "Type d'assurance"
            )
        )


        self.type_assurance = QLineEdit()

        self.type_assurance.setText(
            str(assurance[3] or "")
        )

        layout.addWidget(
            self.type_assurance
        )


        layout.addWidget(
            QLabel(
                "Prime mensuelle"
            )
        )

        self.prime = QLineEdit()

        self.prime.setText(
            str(assurance[4] or "")
        )

        layout.addWidget(
            self.prime
        )


        boutons = QHBoxLayout()

        annuler = QPushButton("Annuler")

        sauvegarder = QPushButton("Sauvegarder")

        boutons.addWidget(annuler)

        boutons.addWidget(sauvegarder)

        layout.addLayout(boutons)

        annuler.clicked.connect(self.reject)

        sauvegarder.clicked.connect(self.accept)

        self.setLayout(layout)
