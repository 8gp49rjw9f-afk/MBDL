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



class PlacementEditDialog(QDialog):

    def __init__(
        self,
        placement,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Modifier un placement"
        )


        self.resize(
            420,
            650
        )


        self.placement = placement


        layout = QVBoxLayout()



        titre = QLabel(
            "Modifier le placement"
        )


        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )


        layout.addWidget(
            titre
        )



        # ======================
        # DATE INSCRIPTION
        # ======================

        layout.addWidget(
            QLabel(
                "Date inscription"
            )
        )


        self.date_inscription = QDateEdit()


        self.date_inscription.setCalendarPopup(
            True
        )


        self.date_inscription.setDate(
            QDate.fromString(
                str(placement[1]),
                "yyyy-MM-dd"
            )
        )


        layout.addWidget(
            self.date_inscription
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


        if placement[2]:

            self.date_fin.setDate(
                QDate.fromString(
                    str(placement[2]),
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
            str(placement[3] or "")
        )


        layout.addWidget(
            self.institution
        )



        # ======================
        # NOM
        # ======================

        layout.addWidget(
            QLabel(
                "Nom du placement"
            )
        )


        self.nom = QLineEdit()


        self.nom.setText(
            str(placement[4] or "")
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
            str(placement[5] or "")
        )


        layout.addWidget(
            self.montant_initial
        )



        # ======================
        # VALEUR ACTUELLE
        # ======================

        layout.addWidget(
            QLabel(
                "Valeur actuelle"
            )
        )


        self.valeur_actuelle = QLineEdit()


        self.valeur_actuelle.setText(
            str(placement[6] or "")
        )


        layout.addWidget(
            self.valeur_actuelle
        )



        # ======================
        # MAXIMUM
        # ======================

        layout.addWidget(
            QLabel(
                "Plafond / Maximum"
            )
        )


        self.maximum = QLineEdit()


        if placement[7] is not None:

            self.maximum.setText(
                str(placement[7])
            )


        layout.addWidget(
            self.maximum
        )



        self.aucun_maximum = QCheckBox(
            "Aucun plafond"
        )


        if placement[7] is None:

            self.aucun_maximum.setChecked(
                True
            )

            self.maximum.setEnabled(
                False
            )


        self.aucun_maximum.stateChanged.connect(
            self.changer_maximum
        )


        layout.addWidget(
            self.aucun_maximum
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



    def changer_maximum(
        self
    ):

        if self.aucun_maximum.isChecked():

            self.maximum.clear()

            self.maximum.setEnabled(
                False
            )

        else:

            self.maximum.setEnabled(
                True
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



    def obtenir_maximum(
        self
    ):

        if self.aucun_maximum.isChecked():

            return None


        valeur = self.maximum.text()


        if valeur == "":

            return None


        try:

            return float(
                valeur
            )

        except:

            return None