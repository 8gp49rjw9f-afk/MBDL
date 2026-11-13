from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QCheckBox,
    QDateEdit
)

from PySide6.QtCore import QDate



class PretEditDialog(QDialog):

    def __init__(
        self,
        pret,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Modifier un prêt"
        )


        self.resize(
            420,
            650
        )


        self.pret = pret


        layout = QVBoxLayout()



        titre = QLabel(
            "Modifier le prêt"
        )


        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )


        layout.addWidget(
            titre
        )



        # ======================
        # DATE DÉBUT
        # ======================

        layout.addWidget(
            QLabel(
                "Date début"
            )
        )


        self.date_debut = QDateEdit()


        self.date_debut.setCalendarPopup(
            True
        )


        self.date_debut.setDate(
            QDate.fromString(
                str(pret[1]),
                "yyyy-MM-dd"
            )
        )


        layout.addWidget(
            self.date_debut
        )



        # ======================
        # DATE FIN
        # ======================

        self.aucune_date_fin = QCheckBox(
            "Pas de date de fin"
        )


        layout.addWidget(
            self.aucune_date_fin
        )


        layout.addWidget(
            QLabel(
                "Date fin"
            )
        )


        self.date_fin = QDateEdit()


        self.date_fin.setCalendarPopup(
            True
        )


        if pret[2]:

            self.date_fin.setDate(
                QDate.fromString(
                    str(pret[2]),
                    "yyyy-MM-dd"
                )
            )

        else:

            self.aucune_date_fin.setChecked(
                True
            )

            self.date_fin.setEnabled(
                False
            )


        self.aucune_date_fin.stateChanged.connect(
            self.changer_date_fin
        )


        layout.addWidget(
            self.date_fin
        )



        # ======================
        # INSTITUTION
        # ======================

        layout.addWidget(
            QLabel(
                "Institution"
            )
        )


        self.institution = QLineEdit()


        self.institution.setText(
            str(pret[3] or "")
        )


        layout.addWidget(
            self.institution
        )



        # ======================
        # NOM
        # ======================

        layout.addWidget(
            QLabel(
                "Nom du prêt"
            )
        )


        self.nom = QLineEdit()


        self.nom.setText(
            str(pret[4] or "")
        )


        layout.addWidget(
            self.nom
        )



        # ======================
        # MONTANT INITIAL
        # ======================

        layout.addWidget(
            QLabel(
                "Montant initial"
            )
        )


        self.montant_initial = QLineEdit()


        self.montant_initial.setText(
            str(pret[5] or "")
        )


        layout.addWidget(
            self.montant_initial
        )



        # ======================
        # SOLDE ACTUEL
        # ======================

        layout.addWidget(
            QLabel(
                "Solde actuel"
            )
        )


        self.solde_actuel = QLineEdit()


        self.solde_actuel.setText(
            str(pret[6] or "")
        )


        layout.addWidget(
            self.solde_actuel
        )



        # ======================
        # TAUX
        # ======================

        layout.addWidget(
            QLabel(
                "Taux d'intérêt (%)"
            )
        )


        self.taux = QLineEdit()


        self.taux.setText(
            str(pret[7] or "")
        )


        layout.addWidget(
            self.taux
        )



        # ======================
        # PAIEMENT MENSUEL
        # ======================

        layout.addWidget(
            QLabel(
                "Paiement mensuel"
            )
        )


        self.paiement_mensuel = QLineEdit()


        self.paiement_mensuel.setText(
            str(pret[8] or "")
        )


        layout.addWidget(
            self.paiement_mensuel
        )



        # ======================
        # BOUTONS
        # ======================

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



    def changer_date_fin(
        self
    ):

        if self.aucune_date_fin.isChecked():

            self.date_fin.clear()

            self.date_fin.setEnabled(
                False
            )

        else:

            self.date_fin.setEnabled(
                True
            )
