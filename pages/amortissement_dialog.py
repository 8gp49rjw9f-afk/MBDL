from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QDateEdit
)

from PySide6.QtCore import QDate



class AmortissementDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Ajouter un tableau d'amortissement"
        )


        self.resize(
            430,
            560
        )


        layout = QVBoxLayout()


        titre = QLabel(
            "Ajouter un tableau d'amortissement"
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
            "Ex: Condo, Auto, Prêt perso..."
        )

        layout.addWidget(
            self.nom
        )


        layout.addWidget(
            QLabel(
                "Date de départ"
            )
        )

        self.date_depart = QDateEdit()

        self.date_depart.setCalendarPopup(
            True
        )

        self.date_depart.setDate(
            QDate.currentDate()
        )

        layout.addWidget(
            self.date_depart
        )


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
                "Mise de fond"
            )
        )

        self.mise_fond = QLineEdit()

        self.mise_fond.setPlaceholderText(
            "0.00"
        )

        layout.addWidget(
            self.mise_fond
        )


        layout.addWidget(
            QLabel(
                "% intérêt annuel"
            )
        )

        self.taux = QLineEdit()

        self.taux.setPlaceholderText(
            "Ex: 5.49"
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


        layout.addWidget(
            QLabel(
                "Paiement additionnel mensuel"
            )
        )

        self.paiement_additionnel = QLineEdit()

        self.paiement_additionnel.setPlaceholderText(
            "0.00"
        )

        layout.addWidget(
            self.paiement_additionnel
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



class AmortissementEditDialog(QDialog):

    def __init__(
        self,
        tableau,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Modifier un tableau d'amortissement"
        )


        self.resize(
            430,
            560
        )


        layout = QVBoxLayout()


        titre = QLabel(
            "Modifier le tableau d'amortissement"
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
            str(tableau[1] or "")
        )

        layout.addWidget(
            self.nom
        )


        layout.addWidget(
            QLabel(
                "Date de départ"
            )
        )

        self.date_depart = QDateEdit()

        self.date_depart.setCalendarPopup(
            True
        )

        date = QDate.fromString(
            str(tableau[2]),
            "yyyy-MM-dd"
        )

        if not date.isValid():

            date = QDate.currentDate()

        self.date_depart.setDate(
            date
        )

        layout.addWidget(
            self.date_depart
        )


        layout.addWidget(
            QLabel(
                "Montant initial"
            )
        )

        self.montant_initial = QLineEdit()

        self.montant_initial.setText(
            str(tableau[3] or "")
        )

        layout.addWidget(
            self.montant_initial
        )


        layout.addWidget(
            QLabel(
                "Mise de fond"
            )
        )

        self.mise_fond = QLineEdit()

        self.mise_fond.setText(
            str(tableau[4] or "")
        )

        layout.addWidget(
            self.mise_fond
        )


        layout.addWidget(
            QLabel(
                "% intérêt annuel"
            )
        )

        self.taux = QLineEdit()

        self.taux.setText(
            str(tableau[5] or "")
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
            str(tableau[6] or "")
        )

        layout.addWidget(
            self.mois
        )


        layout.addWidget(
            QLabel(
                "Paiement additionnel mensuel"
            )
        )

        self.paiement_additionnel = QLineEdit()

        self.paiement_additionnel.setText(
            str(tableau[7] or "")
        )

        layout.addWidget(
            self.paiement_additionnel
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
