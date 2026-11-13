from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QComboBox
)



class ReerCeliDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Ajouter une cotisation"
        )


        self.resize(
            400,
            300
        )


        layout = QVBoxLayout()


        titre = QLabel(
            "Ajouter une cotisation"
        )

        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(
            titre
        )


        layout.addWidget(
            QLabel(
                "Type"
            )
        )


        self.type_ligne = QComboBox()

        self.type_ligne.addItem(
            "REER"
        )

        self.type_ligne.addItem(
            "CELI"
        )

        layout.addWidget(
            self.type_ligne
        )


        layout.addWidget(
            QLabel(
                "Nom"
            )
        )


        self.nom = QLineEdit()

        self.nom.setPlaceholderText(
            "Ex: Cotisation janvier"
        )

        layout.addWidget(
            self.nom
        )


        layout.addWidget(
            QLabel(
                "Montant"
            )
        )


        self.montant = QLineEdit()

        self.montant.setPlaceholderText(
            "0.00"
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


        annuler.clicked.connect(
            self.reject
        )

        sauvegarder.clicked.connect(
            self.accept
        )


        self.setLayout(
            layout
        )



class ReerCeliEditDialog(QDialog):

    def __init__(
        self,
        type_ligne,
        nom,
        montant,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Modifier la cotisation"
        )


        self.resize(
            400,
            300
        )


        layout = QVBoxLayout()


        titre = QLabel(
            "Modifier la cotisation"
        )

        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(
            titre
        )


        layout.addWidget(
            QLabel(
                "Type"
            )
        )


        self.type_ligne = QComboBox()

        self.type_ligne.addItem(
            "REER"
        )

        self.type_ligne.addItem(
            "CELI"
        )

        self.type_ligne.setCurrentText(
            str(type_ligne or "REER")
        )

        layout.addWidget(
            self.type_ligne
        )


        layout.addWidget(
            QLabel(
                "Nom"
            )
        )


        self.nom = QLineEdit()

        self.nom.setText(
            str(nom or "")
        )

        layout.addWidget(
            self.nom
        )


        layout.addWidget(
            QLabel(
                "Montant"
            )
        )


        self.montant = QLineEdit()

        self.montant.setText(
            str(montant or "")
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


        annuler.clicked.connect(
            self.reject
        )

        sauvegarder.clicked.connect(
            self.accept
        )


        self.setLayout(
            layout
        )
