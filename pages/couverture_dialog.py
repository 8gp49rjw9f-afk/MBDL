from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QComboBox
)



class CouvertureDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setWindowTitle("Ajouter une couverture")
        self.resize(400, 400)

        layout = QVBoxLayout()

        titre = QLabel("Ajouter une couverture")
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        # Nom
        layout.addWidget(QLabel("Nom"))
        self.nom = QLineEdit()
        self.nom.setPlaceholderText("Ex: Responsabilité civile")
        layout.addWidget(self.nom)

        # Montant assuré avec type
        layout.addWidget(QLabel("Montant assuré"))
        self.type_montant = QComboBox()
        self.type_montant.addItem("Prix ($)")
        self.type_montant.addItem("Pourcentage (%)")
        layout.addWidget(self.type_montant)
        self.montant_assure = QLineEdit()
        self.montant_assure.setPlaceholderText("0.00")
        layout.addWidget(self.montant_assure)

        # Franchise
        layout.addWidget(QLabel("Franchise"))
        self.franchise = QLineEdit()
        self.franchise.setPlaceholderText("0.00")
        layout.addWidget(self.franchise)

        # Autres informations
        layout.addWidget(QLabel("Autres informations"))
        self.autres_infos = QLineEdit()
        self.autres_infos.setPlaceholderText("Ex: Notes supplémentaires")
        layout.addWidget(self.autres_infos)

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



class CouvertureEditDialog(QDialog):

    def __init__(
        self,
        couverture,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setWindowTitle("Modifier une couverture")
        self.resize(400, 400)

        layout = QVBoxLayout()

        titre = QLabel("Modifier la couverture")
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        # couverture = (id, assurance_id, nom, type_montant, montant_assure, franchise, autres_infos)

        # Nom
        layout.addWidget(QLabel("Nom"))
        self.nom = QLineEdit()
        self.nom.setText(str(couverture[2] or ""))
        layout.addWidget(self.nom)

        # Montant assuré avec type
        layout.addWidget(QLabel("Montant assuré"))
        self.type_montant = QComboBox()
        self.type_montant.addItem("Prix ($)")
        self.type_montant.addItem("Pourcentage (%)")
        self.type_montant.setCurrentText(str(couverture[3] or "Prix ($)"))
        layout.addWidget(self.type_montant)
        self.montant_assure = QLineEdit()
        self.montant_assure.setText(str(couverture[4] or ""))
        layout.addWidget(self.montant_assure)

        # Franchise
        layout.addWidget(QLabel("Franchise"))
        self.franchise = QLineEdit()
        self.franchise.setText(str(couverture[5] or ""))
        layout.addWidget(self.franchise)

        # Autres informations
        layout.addWidget(QLabel("Autres informations"))
        self.autres_infos = QLineEdit()
        self.autres_infos.setText(str(couverture[6] or ""))
        layout.addWidget(self.autres_infos)

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