from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QCheckBox
)



class TaxeDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Ajouter un contrat"
        )


        self.resize(
            400,
            470
        )


        layout = QVBoxLayout()



        titre = QLabel(
            "Ajouter un contrat"
        )

        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )


        layout.addWidget(
            titre
        )



        # =====================
        # ANNEE
        # =====================

        layout.addWidget(
            QLabel(
                "Année"
            )
        )


        self.annee = QLineEdit()


        self.annee.setPlaceholderText(
            "Ex: 2026"
        )


        layout.addWidget(
            self.annee
        )



        # =====================
        # CONTRAT
        # =====================

        layout.addWidget(
            QLabel(
                "Contrat"
            )
        )


        self.contrat = QLineEdit()


        self.contrat.setPlaceholderText(
            "Ex: Client ABC"
        )


        layout.addWidget(
            self.contrat
        )



        # =====================
        # MONTANT FACTURE
        # =====================

        layout.addWidget(
            QLabel(
                "Montant facturé"
            )
        )


        self.montant_facture = QLineEdit()


        self.montant_facture.setPlaceholderText(
            "0.00"
        )


        layout.addWidget(
            self.montant_facture
        )



        # =====================
        # SANS TPS / TVQ
        # =====================

        self.sans_tps = QCheckBox(
            "TPS non applicable"
        )


        layout.addWidget(
            self.sans_tps
        )


        self.sans_tvq = QCheckBox(
            "TVQ non applicable"
        )


        layout.addWidget(
            self.sans_tvq
        )



        # =====================
        # SANS IMPOT
        # =====================

        self.sans_impot = QCheckBox(
            "Sans impôt applicable"
        )


        layout.addWidget(
            self.sans_impot
        )


        self.sans_impot.stateChanged.connect(
            self.changer_impot
        )



        # =====================
        # POURCENTAGE IMPOT
        # =====================

        layout.addWidget(
            QLabel(
                "Impôt à payer (%)"
            )
        )


        self.pourcentage_impot = QLineEdit()


        self.pourcentage_impot.setText(
            "33"
        )


        layout.addWidget(
            self.pourcentage_impot
        )



        # =====================
        # BOUTONS
        # =====================

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



    def changer_impot(
        self
    ):

        if self.sans_impot.isChecked():

            self.pourcentage_impot.setEnabled(
                False
            )

        else:

            self.pourcentage_impot.setEnabled(
                True
            )
