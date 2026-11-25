from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout
)



class BudgetLigneDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setWindowTitle("Ajouter une ligne")
        self.resize(400, 300)

        layout = QVBoxLayout()

        titre = QLabel("Ajouter une ligne")
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        layout.addWidget(QLabel("Nom"))
        self.nom = QLineEdit()
        self.nom.setPlaceholderText("Ex: Billet d'avion, Hôtel, Restaurant...")
        layout.addWidget(self.nom)

        layout.addWidget(QLabel("Prix"))
        self.prix = QLineEdit()
        self.prix.setPlaceholderText("0.00")
        layout.addWidget(self.prix)

        layout.addWidget(QLabel("Autres informations"))
        self.autres_infos = QLineEdit()
        self.autres_infos.setPlaceholderText("Ex: Notes supplémentaires")
        layout.addWidget(self.autres_infos)

        boutons = QHBoxLayout()
        annuler = QPushButton("Annuler")
        sauvegarder = QPushButton("Sauvegarder")
        sauvegarder.setDefault(
            True
        )
        sauvegarder.setAutoDefault(
            True
        )
        boutons.addWidget(annuler)
        boutons.addWidget(sauvegarder)
        layout.addLayout(boutons)

        annuler.clicked.connect(self.reject)
        sauvegarder.clicked.connect(self.accept)

        self.setLayout(layout)



class BudgetLigneEditDialog(QDialog):

    def __init__(
        self,
        ligne,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setWindowTitle("Modifier une ligne")
        self.resize(400, 300)

        layout = QVBoxLayout()

        titre = QLabel("Modifier la ligne")
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        # ligne = (id, budget_id, nom, prix, autres_infos)

        layout.addWidget(QLabel("Nom"))
        self.nom = QLineEdit()
        self.nom.setText(str(ligne[2] or ""))
        layout.addWidget(self.nom)

        layout.addWidget(QLabel("Prix"))
        self.prix = QLineEdit()
        self.prix.setText(str(ligne[3] or ""))
        layout.addWidget(self.prix)

        layout.addWidget(QLabel("Autres informations"))
        self.autres_infos = QLineEdit()
        self.autres_infos.setText(str(ligne[4] or ""))
        layout.addWidget(self.autres_infos)

        boutons = QHBoxLayout()
        annuler = QPushButton("Annuler")
        sauvegarder = QPushButton("Sauvegarder")
        sauvegarder.setDefault(
            True
        )
        sauvegarder.setAutoDefault(
            True
        )
        boutons.addWidget(annuler)
        boutons.addWidget(sauvegarder)
        layout.addLayout(boutons)

        annuler.clicked.connect(self.reject)
        sauvegarder.clicked.connect(self.accept)

        self.setLayout(layout)
