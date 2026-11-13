from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox
)



class BudgetMensuelDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Ajouter au budget"
        )


        self.resize(
            400,
            300
        )


        layout = QVBoxLayout()


        titre = QLabel(
            "Ajouter une ligne au budget"
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
            "Entrée"
        )

        self.type_ligne.addItem(
            "Dépense"
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
            "Ex: Loyer"
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



class BudgetMensuelEditDialog(QDialog):

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
            "Modifier le budget"
        )


        self.resize(
            400,
            300
        )


        layout = QVBoxLayout()


        titre = QLabel(
            "Modifier une ligne"
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
            "Entrée"
        )

        self.type_ligne.addItem(
            "Dépense"
        )

        self.type_ligne.setCurrentText(
            str(type_ligne or "Entrée")
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
