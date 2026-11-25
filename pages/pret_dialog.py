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



class PretDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Ajouter un prêt"
        )


        self.resize(
            420,
            680
        )


        layout = QVBoxLayout()


        titre = QLabel(
            "Ajouter un prêt"
        )

        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(
            titre
        )


        # =====================
        # DATES
        # =====================

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
            QDate.currentDate()
        )

        layout.addWidget(
            self.date_debut
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
            "Ex: Desjardins"
        )

        layout.addWidget(
            self.institution
        )


        layout.addWidget(
            QLabel(
                "Nom du prêt"
            )
        )

        self.nom = QLineEdit()

        self.nom.setPlaceholderText(
            "Ex: Prêt auto, Marge de crédit..."
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
                "Montant avancé"
            )
        )

        self.solde_actuel = QLineEdit()

        self.solde_actuel.setPlaceholderText(
            "0.00"
        )

        layout.addWidget(
            self.solde_actuel
        )


        layout.addWidget(
            QLabel(
                "Taux d'intérêt (%)"
            )
        )

        self.taux = QLineEdit()

        self.taux.setPlaceholderText(
            "Ex: 5.5"
        )

        layout.addWidget(
            self.taux
        )


        layout.addWidget(
            QLabel(
                "Nombre de mois"
            )
        )

        self.mois = QLineEdit()

        self.mois.setPlaceholderText(
            "Ex: 60"
        )

        layout.addWidget(
            self.mois
        )


        layout.addWidget(
            QLabel(
                "Paiement mensuel"
            )
        )

        self.paiement_mensuel = QLineEdit()

        self.paiement_mensuel.setPlaceholderText(
            "0.00"
        )

        layout.addWidget(
            self.paiement_mensuel
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
            680
        )


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


        # =====================
        # DATES
        # =====================

        layout.addWidget(
            QLabel(
                "Date début"
            )
        )


        self.date_debut = QDateEdit()

        self.date_debut.setCalendarPopup(
            True
        )


        date = QDate.fromString(
            str(pret[1]),
            "yyyy-MM-dd"
        )

        if not date.isValid():

            date = QDate.currentDate()


        self.date_debut.setDate(
            date
        )

        layout.addWidget(
            self.date_debut
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


        if pret[2]:

            date_fin = QDate.fromString(
                str(pret[2]),
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
            str(pret[3] or "")
        )

        layout.addWidget(
            self.institution
        )


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
            str(pret[5] or "")
        )

        layout.addWidget(
            self.montant_initial
        )


        layout.addWidget(
            QLabel(
                "Montant avancé"
            )
        )

        self.solde_actuel = QLineEdit()

        self.solde_actuel.setText(
            str(pret[6] or "")
        )

        layout.addWidget(
            self.solde_actuel
        )


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


        layout.addWidget(
            QLabel(
                "Nombre de mois"
            )
        )

        self.mois = QLineEdit()

        self.mois.setText(
            str(pret[9] or "")
        )

        layout.addWidget(
            self.mois
        )


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
