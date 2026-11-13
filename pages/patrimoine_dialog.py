from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
)


class PatrimoineDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Ajouter un actif")
        self.resize(400, 300)

        layout = QVBoxLayout()

        titre = QLabel("Ajouter un actif")
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        layout.addWidget(QLabel("Nom"))
        self.nom = QLineEdit()
        self.nom.setPlaceholderText("Ex: Condo, Auto, Terrain, Bijoux...")
        layout.addWidget(self.nom)

        layout.addWidget(QLabel("Valeur"))
        self.montant = QLineEdit()
        self.montant.setPlaceholderText("0.00")
        layout.addWidget(self.montant)

        boutons = QHBoxLayout()
        annuler = QPushButton("Annuler")
        sauvegarder = QPushButton("Sauvegarder")
        boutons.addWidget(annuler)
        boutons.addWidget(sauvegarder)
        layout.addLayout(boutons)

        annuler.clicked.connect(self.reject)
        sauvegarder.clicked.connect(self.accept)

        self.setLayout(layout)


class PatrimoineEditDialog(QDialog):

    def __init__(self, nom, montant, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Modifier un actif")
        self.resize(400, 300)

        layout = QVBoxLayout()

        titre = QLabel("Modifier l'actif")
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        layout.addWidget(QLabel("Nom"))
        self.nom = QLineEdit()
        self.nom.setText(str(nom or ""))
        layout.addWidget(self.nom)

        layout.addWidget(QLabel("Valeur"))
        self.montant = QLineEdit()
        self.montant.setText(str(montant or ""))
        layout.addWidget(self.montant)

        boutons = QHBoxLayout()
        annuler = QPushButton("Annuler")
        sauvegarder = QPushButton("Sauvegarder")
        boutons.addWidget(annuler)
        boutons.addWidget(sauvegarder)
        layout.addLayout(boutons)

        annuler.clicked.connect(self.reject)
        sauvegarder.clicked.connect(self.accept)

        self.setLayout(layout)
