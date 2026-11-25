from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QDateEdit
)

from PySide6.QtCore import QDate



class BourseEditDialog(QDialog):

    def __init__(
        self,
        action,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Modifier une action"
        )


        self.resize(
            420,
            520
        )


        layout = QVBoxLayout()


        titre = QLabel(
            "Modifier l'action"
        )

        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )


        layout.addWidget(
            titre
        )


        layout.addWidget(
            QLabel(
                "Date d'achat"
            )
        )


        self.date_achat = QDateEdit()

        self.date_achat.setCalendarPopup(
            True
        )

        self.date_achat.setDate(
            QDate.fromString(
                str(action[1]),
                "yyyy-MM-dd"
            )
        )

        layout.addWidget(
            self.date_achat
        )


        layout.addWidget(
            QLabel(
                "Institution"
            )
        )


        self.institution = QLineEdit()

        self.institution.setText(
            str(action[2] or "")
        )

        layout.addWidget(
            self.institution
        )


        layout.addWidget(
            QLabel(
                "Nom de l'action"
            )
        )


        self.nom = QLineEdit()

        self.nom.setText(
            str(action[3] or "")
        )

        layout.addWidget(
            self.nom
        )


        layout.addWidget(
            QLabel(
                "Prix d'achat"
            )
        )


        self.prix_achat = QLineEdit()

        self.prix_achat.setText(
            str(action[4] or "")
        )

        layout.addWidget(
            self.prix_achat
        )


        layout.addWidget(
            QLabel(
                "Valeur actuelle"
            )
        )


        self.valeur_actuelle = QLineEdit()

        self.valeur_actuelle.setText(
            str(action[5] or "")
        )

        layout.addWidget(
            self.valeur_actuelle
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
