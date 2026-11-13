from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
)



class HypothequeDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Ajouter une hypothèque"
        )


        self.resize(
            420,
            520
        )


        layout = QVBoxLayout()


        titre = QLabel(
            "Ajouter une hypothèque"
        )

        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(
            titre
        )


        layout.addWidget(
            QLabel(
                "Nom"
            )
        )

        self.nom = QLineEdit()

        self.nom.setPlaceholderText(
            "Ex: Condo Montréal"
        )

        layout.addWidget(
            self.nom
        )


        layout.addWidget(
            QLabel(
                "Institution"
            )
        )

        self.institution = QLineEdit()

        self.institution.setPlaceholderText(
            "Ex: Desjardins"
        )

        layout.addWidget(
            self.institution
        )


        layout.addWidget(
            QLabel(
                "Valeur de la propriété"
            )
        )

        self.valeur_propriete = QLineEdit()

        self.valeur_propriete.setPlaceholderText(
            "0.00"
        )

        layout.addWidget(
            self.valeur_propriete
        )


        layout.addWidget(
            QLabel(
                "Montant du prêt total"
            )
        )

        self.montant_initial = QLineEdit()

        self.montant_initial.setPlaceholderText(
            "0.00"
        )

        layout.addWidget(
            self.montant_initial
        )


        layout.addWidget(
            QLabel(
                "Montant déjà payé"
            )
        )

        self.montant_paye = QLineEdit()

        self.montant_paye.setPlaceholderText(
            "0.00"
        )

        layout.addWidget(
            self.montant_paye
        )


        layout.addWidget(
            QLabel(
                "% intérêt annuel"
            )
        )

        self.taux = QLineEdit()

        self.taux.setPlaceholderText(
            "Ex: 4.79"
        )

        layout.addWidget(
            self.taux
        )


        layout.addWidget(
            QLabel(
                "Mois d'amortissement"
            )
        )

        self.mois = QLineEdit()

        self.mois.setPlaceholderText(
            "Ex: 300"
        )

        layout.addWidget(
            self.mois
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



class HypothequeEditDialog(QDialog):

    def __init__(
        self,
        hypotheque,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Modifier une hypothèque"
        )


        self.resize(
            420,
            520
        )


        layout = QVBoxLayout()


        titre = QLabel(
            "Modifier l'hypothèque"
        )

        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(
            titre
        )


        layout.addWidget(
            QLabel(
                "Nom"
            )
        )

        self.nom = QLineEdit()

        self.nom.setText(
            str(hypotheque[1] or "")
        )

        layout.addWidget(
            self.nom
        )


        layout.addWidget(
            QLabel(
                "Institution"
            )
        )

        self.institution = QLineEdit()

        self.institution.setText(
            str(hypotheque[2] or "")
        )

        layout.addWidget(
            self.institution
        )


        layout.addWidget(
            QLabel(
                "Valeur de la propriété"
            )
        )

        self.valeur_propriete = QLineEdit()

        self.valeur_propriete.setText(
            str(hypotheque[3] or "")
        )

        layout.addWidget(
            self.valeur_propriete
        )


        layout.addWidget(
            QLabel(
                "Montant du prêt total"
            )
        )

        self.montant_initial = QLineEdit()

        self.montant_initial.setText(
            str(hypotheque[4] or "")
        )

        layout.addWidget(
            self.montant_initial
        )


        layout.addWidget(
            QLabel(
                "Montant déjà payé"
            )
        )

        self.montant_paye = QLineEdit()

        self.montant_paye.setText(
            str(hypotheque[5] or "")
        )

        layout.addWidget(
            self.montant_paye
        )


        layout.addWidget(
            QLabel(
                "% intérêt annuel"
            )
        )

        self.taux = QLineEdit()

        self.taux.setText(
            str(hypotheque[6] or "")
        )

        layout.addWidget(
            self.taux
        )


        layout.addWidget(
            QLabel(
                "Mois d'amortissement"
            )
        )

        self.mois = QLineEdit()

        self.mois.setText(
            str(hypotheque[7] or "")
        )

        layout.addWidget(
            self.mois
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
