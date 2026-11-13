from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QComboBox,
    QDateEdit
)

from PySide6.QtCore import QDate


TYPES = [
    "REER",
    "CELI",
    "Autre"
]



class PlacementDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Ajouter un placement"
        )


        self.resize(
            420,
            700
        )


        layout = QVBoxLayout()


        titre = QLabel(
            "Ajouter un placement"
        )

        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(
            titre
        )


        # =====================
        # TYPE
        # =====================

        layout.addWidget(
            QLabel(
                "Type"
            )
        )


        self.type_ligne = QComboBox()

        for valeur in TYPES:

            self.type_ligne.addItem(
                valeur
            )

        layout.addWidget(
            self.type_ligne
        )


        # =====================
        # DATES
        # =====================

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
            QDate.currentDate()
        )

        layout.addWidget(
            self.date_inscription
        )


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

        self.date_fin.setDate(
            QDate.currentDate()
        )

        layout.addWidget(
            self.date_fin
        )


        self.aucune_date_fin.stateChanged.connect(
            self.changer_date_fin
        )


        # =====================
        # INFORMATIONS
        # =====================

        layout.addWidget(
            QLabel(
                "Institution"
            )
        )


        self.institution = QLineEdit()

        self.institution.setPlaceholderText(
            "Ex: Banque Nationale"
        )

        layout.addWidget(
            self.institution
        )


        layout.addWidget(
            QLabel(
                "Nom du placement"
            )
        )


        self.nom = QLineEdit()

        self.nom.setPlaceholderText(
            "Ex: CELI actions, REER 2026..."
        )

        layout.addWidget(
            self.nom
        )


        # =====================
        # VALEURS
        # =====================

        layout.addWidget(
            QLabel(
                "Montant initial"
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
                "Valeur actuelle"
            )
        )


        self.valeur_actuelle = QLineEdit()

        self.valeur_actuelle.setPlaceholderText(
            "0.00"
        )

        layout.addWidget(
            self.valeur_actuelle
        )


        layout.addWidget(
            QLabel(
                "Plafond / Maximum"
            )
        )


        self.maximum = QLineEdit()

        self.maximum.setPlaceholderText(
            "Optionnel"
        )

        layout.addWidget(
            self.maximum
        )


        self.aucun_maximum = QCheckBox(
            "Aucun plafond"
        )

        layout.addWidget(
            self.aucun_maximum
        )


        self.aucun_maximum.stateChanged.connect(
            self.changer_maximum
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

            return 0


        try:

            return float(
                self.maximum.text()
                .replace(" ", "")
                .replace(",", ".")
                .replace("$", "")
            )

        except:

            return 0



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
            700
        )


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


        # =====================
        # TYPE
        # =====================

        layout.addWidget(
            QLabel(
                "Type"
            )
        )


        self.type_ligne = QComboBox()

        for valeur in TYPES:

            self.type_ligne.addItem(
                valeur
            )


        self.type_ligne.setCurrentText(
            str(placement[1] or "Autre")
        )

        layout.addWidget(
            self.type_ligne
        )


        # =====================
        # DATES
        # =====================

        layout.addWidget(
            QLabel(
                "Date inscription"
            )
        )


        self.date_inscription = QDateEdit()

        self.date_inscription.setCalendarPopup(
            True
        )


        date = QDate.fromString(
            str(placement[2]),
            "yyyy-MM-dd"
        )

        if not date.isValid():

            date = QDate.currentDate()


        self.date_inscription.setDate(
            date
        )

        layout.addWidget(
            self.date_inscription
        )


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


        if placement[3]:

            date_fin = QDate.fromString(
                str(placement[3]),
                "yyyy-MM-dd"
            )

            if not date_fin.isValid():

                date_fin = QDate.currentDate()

            self.date_fin.setDate(
                date_fin
            )

        else:

            self.date_fin.setDate(
                QDate.currentDate()
            )

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


        # =====================
        # INFORMATIONS
        # =====================

        layout.addWidget(
            QLabel(
                "Institution"
            )
        )


        self.institution = QLineEdit()

        self.institution.setText(
            str(placement[4] or "")
        )

        layout.addWidget(
            self.institution
        )


        layout.addWidget(
            QLabel(
                "Nom du placement"
            )
        )


        self.nom = QLineEdit()

        self.nom.setText(
            str(placement[5] or "")
        )

        layout.addWidget(
            self.nom
        )


        # =====================
        # VALEURS
        # =====================

        layout.addWidget(
            QLabel(
                "Montant initial"
            )
        )


        self.montant_initial = QLineEdit()

        self.montant_initial.setText(
            str(placement[6] or "")
        )

        layout.addWidget(
            self.montant_initial
        )


        layout.addWidget(
            QLabel(
                "Valeur actuelle"
            )
        )


        self.valeur_actuelle = QLineEdit()

        self.valeur_actuelle.setText(
            str(placement[7] or "")
        )

        layout.addWidget(
            self.valeur_actuelle
        )


        layout.addWidget(
            QLabel(
                "Plafond / Maximum"
            )
        )


        self.maximum = QLineEdit()

        self.maximum.setText(
            str(placement[8] or "")
        )

        layout.addWidget(
            self.maximum
        )


        self.aucun_maximum = QCheckBox(
            "Aucun plafond"
        )

        layout.addWidget(
            self.aucun_maximum
        )


        if not placement[8]:

            self.aucun_maximum.setChecked(
                True
            )

            self.maximum.setEnabled(
                False
            )


        self.aucun_maximum.stateChanged.connect(
            self.changer_maximum
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

            return 0


        try:

            return float(
                self.maximum.text()
                .replace(" ", "")
                .replace(",", ".")
                .replace("$", "")
            )

        except:

            return 0
