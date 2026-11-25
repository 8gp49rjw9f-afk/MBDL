from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QComboBox
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
            type_ligne
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
            str(nom)
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

        sauvegarder.setDefault(
            True
        )

        sauvegarder.setAutoDefault(
            True
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
