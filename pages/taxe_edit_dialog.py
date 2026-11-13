from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QCheckBox
)



class TaxeEditDialog(QDialog):

    def __init__(
        self,
        contrat,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Modifier un contrat"
        )


        self.resize(
            400,
            470
        )


        self.contrat_data = contrat


        layout = QVBoxLayout()



        titre = QLabel(
            "Modifier le contrat"
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


        self.annee.setText(
            str(contrat[1] or "")
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


        self.contrat.setText(
            str(contrat[2] or "")
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


        self.montant_facture.setText(
            str(contrat[3] or "")
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


        self.sans_tps.setChecked(
            bool(
                contrat[4]
            )
        )


        layout.addWidget(
            self.sans_tps
        )


        self.sans_tvq = QCheckBox(
            "TVQ non applicable"
        )


        self.sans_tvq.setChecked(
            bool(
                contrat[5]
            )
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


        self.sans_impot.setChecked(
            bool(
                contrat[6]
            )
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
            str(
                contrat[7]
                if contrat[7] is not None
                else 33
            )
        )


        if self.sans_impot.isChecked():

            self.pourcentage_impot.setEnabled(
                False
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
