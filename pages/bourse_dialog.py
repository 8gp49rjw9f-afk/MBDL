from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QComboBox,
    QDateEdit,
    QCheckBox
)

from PySide6.QtCore import QDate

from pages.bourse_recherche_dialog import BourseRechercheDialog


TYPES = [
    "Bourse",
    "Crypto"
]



class BourseDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Ajouter une position")
        self.resize(420, 620)

        layout = QVBoxLayout()

        titre = QLabel("Ajouter une position")
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        # Bouton recherche en haut
        bouton_rechercher = QPushButton("🔍 Rechercher le prix en ligne")
        bouton_rechercher.setStyleSheet("font-size:14px;font-weight:bold;padding:8px;")
        bouton_rechercher.clicked.connect(self.rechercher_prix)
        layout.addWidget(bouton_rechercher)

        # Type
        layout.addWidget(QLabel("Type"))
        self.type_ligne = QComboBox()
        for valeur in TYPES:
            self.type_ligne.addItem(valeur)
        layout.addWidget(self.type_ligne)

        # Date d'achat
        layout.addWidget(QLabel("Date d'achat"))
        self.date_achat = QDateEdit()
        self.date_achat.setCalendarPopup(True)
        self.date_achat.setDate(QDate.currentDate())
        layout.addWidget(self.date_achat)

        # Institution
        layout.addWidget(QLabel("Institution"))
        self.institution = QLineEdit()
        self.institution.setPlaceholderText("Ex: Wealthsimple, Binance...")
        layout.addWidget(self.institution)

        # Nom
        layout.addWidget(QLabel("Nom"))
        self.nom = QLineEdit()
        self.nom.setPlaceholderText("Ex: Apple, XEQT, Bitcoin...")
        layout.addWidget(self.nom)

        # Symbole
        layout.addWidget(QLabel("Symbole"))
        self.symbole = QLineEdit()
        self.symbole.setPlaceholderText("Ex: AAPL, BTC...")
        layout.addWidget(self.symbole)

        # Nombre d'actions
        layout.addWidget(QLabel("Nombre d'actions / unités"))
        self.nombre_actions = QLineEdit()
        self.nombre_actions.setPlaceholderText("Ex: 25")
        layout.addWidget(self.nombre_actions)

        # Prix d'achat par action + checkbox prix actuel
        layout.addWidget(QLabel("Prix d'achat par action"))
        prix_achat_layout = QHBoxLayout()
        self.prix_achat = QLineEdit()
        self.prix_achat.setPlaceholderText("0.00")
        prix_achat_layout.addWidget(self.prix_achat)

        self.checkbox_prix_actuel = QCheckBox("= Prix actuel")
        self.checkbox_prix_actuel.setChecked(True)
        self.checkbox_prix_actuel.stateChanged.connect(self.sync_prix_achat)
        prix_achat_layout.addWidget(self.checkbox_prix_actuel)
        layout.addLayout(prix_achat_layout)

        # Prix actuel par action
        layout.addWidget(QLabel("Prix actuel par action"))
        self.prix_actuel = QLineEdit()
        self.prix_actuel.setPlaceholderText("0.00")
        layout.addWidget(self.prix_actuel)

        # Boutons
        boutons = QHBoxLayout()
        annuler = QPushButton("Annuler")
        sauvegarder = QPushButton("Sauvegarder")
        boutons.addWidget(annuler)
        boutons.addWidget(sauvegarder)
        layout.addLayout(boutons)

        annuler.clicked.connect(self.reject)
        sauvegarder.clicked.connect(self.accept)

        self.setLayout(layout)


    def sync_prix_achat(self):

        if self.checkbox_prix_actuel.isChecked():
            self.prix_achat.setText(self.prix_actuel.text())
            self.prix_achat.setEnabled(False)
        else:
            self.prix_achat.setEnabled(True)


    def rechercher_prix(self):

        type_ligne = self.type_ligne.currentText()
        nom = self.nom.text().strip()

        dialog = BourseRechercheDialog(
            type_ligne=type_ligne,
            nom_recherche=nom,
            parent=self
        )

        if dialog.exec_() and dialog.prix_selectionne is not None:
            self.prix_actuel.setText(str(dialog.prix_selectionne))
            if dialog.nom_selectionne:
                self.nom.setText(dialog.nom_selectionne)
            if dialog.symbole_selectionne:
                self.symbole.setText(dialog.symbole_selectionne)
            if self.checkbox_prix_actuel.isChecked():
                self.prix_achat.setText(str(dialog.prix_selectionne))



class BourseEditDialog(QDialog):

    def __init__(self, action, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Modifier une position")
        self.resize(420, 620)

        layout = QVBoxLayout()

        titre = QLabel("Modifier la position")
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        # Bouton recherche en haut
        bouton_rechercher = QPushButton("🔍 Rechercher le prix en ligne")
        bouton_rechercher.setStyleSheet("font-size:14px;font-weight:bold;padding:8px;")
        bouton_rechercher.clicked.connect(self.rechercher_prix)
        layout.addWidget(bouton_rechercher)

        # Type
        layout.addWidget(QLabel("Type"))
        self.type_ligne = QComboBox()
        for valeur in TYPES:
            self.type_ligne.addItem(valeur)
        self.type_ligne.setCurrentText(str(action[8] or "Bourse"))
        layout.addWidget(self.type_ligne)

        # Date d'achat
        layout.addWidget(QLabel("Date d'achat"))
        self.date_achat = QDateEdit()
        self.date_achat.setCalendarPopup(True)
        date = QDate.fromString(str(action[1]), "yyyy-MM-dd")
        if not date.isValid():
            date = QDate.currentDate()
        self.date_achat.setDate(date)
        layout.addWidget(self.date_achat)

        # Institution
        layout.addWidget(QLabel("Institution"))
        self.institution = QLineEdit()
        self.institution.setText(str(action[2] or ""))
        layout.addWidget(self.institution)

        # Nom
        layout.addWidget(QLabel("Nom de l'action"))
        self.nom = QLineEdit()
        self.nom.setText(str(action[3] or ""))
        layout.addWidget(self.nom)

        # Symbole
        layout.addWidget(QLabel("Symbole"))
        self.symbole = QLineEdit()
        self.symbole.setText(str(action[4] or ""))
        layout.addWidget(self.symbole)

        # Nombre d'actions
        layout.addWidget(QLabel("Nombre d'actions"))
        self.nombre_actions = QLineEdit()
        self.nombre_actions.setText(str(action[5] or ""))
        layout.addWidget(self.nombre_actions)

        # Prix d'achat par action + checkbox
        layout.addWidget(QLabel("Prix d'achat par action"))
        prix_achat_layout = QHBoxLayout()
        self.prix_achat = QLineEdit()
        self.prix_achat.setText(str(action[6] or ""))
        prix_achat_layout.addWidget(self.prix_achat)

        self.checkbox_prix_actuel = QCheckBox("= Prix actuel")
        self.checkbox_prix_actuel.setChecked(True)
        self.checkbox_prix_actuel.stateChanged.connect(self.sync_prix_achat)
        prix_achat_layout.addWidget(self.checkbox_prix_actuel)
        layout.addLayout(prix_achat_layout)

        # Prix actuel par action
        layout.addWidget(QLabel("Prix actuel par action"))
        self.prix_actuel = QLineEdit()
        self.prix_actuel.setText(str(action[7] or ""))
        layout.addWidget(self.prix_actuel)

        # Boutons
        boutons = QHBoxLayout()
        annuler = QPushButton("Annuler")
        sauvegarder = QPushButton("Sauvegarder")
        boutons.addWidget(annuler)
        boutons.addWidget(sauvegarder)
        layout.addLayout(boutons)

        annuler.clicked.connect(self.reject)
        sauvegarder.clicked.connect(self.accept)

        self.setLayout(layout)


    def sync_prix_achat(self):

        if self.checkbox_prix_actuel.isChecked():
            self.prix_achat.setText(self.prix_actuel.text())
            self.prix_achat.setEnabled(False)
        else:
            self.prix_achat.setEnabled(True)


    def rechercher_prix(self):

        type_ligne = self.type_ligne.currentText()
        nom = self.nom.text().strip()

        dialog = BourseRechercheDialog(
            type_ligne=type_ligne,
            nom_recherche=nom,
            parent=self
        )

        if dialog.exec_() and dialog.prix_selectionne is not None:
            self.prix_actuel.setText(str(dialog.prix_selectionne))
            if dialog.nom_selectionne:
                self.nom.setText(dialog.nom_selectionne)
            if dialog.symbole_selectionne:
                self.symbole.setText(dialog.symbole_selectionne)
            if self.checkbox_prix_actuel.isChecked():
                self.prix_achat.setText(str(dialog.prix_selectionne))
