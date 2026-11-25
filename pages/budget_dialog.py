from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout
)



class BudgetDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setWindowTitle("Ajouter un budget")
        self.resize(400, 200)

        layout = QVBoxLayout()

        titre = QLabel("Ajouter un budget")
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        layout.addWidget(QLabel("Nom de l'événement"))
        self.nom = QLineEdit()
        self.nom.setPlaceholderText("Ex: Vacances 2026, Rénovation cuisine...")
        layout.addWidget(self.nom)

        boutons = QHBoxLayout()
        annuler = QPushButton("Annuler")
        sauvegarder = QPushButton("Sauvegarder")
        boutons.addWidget(annuler)
        boutons.addWidget(sauvegarder)
        layout.addLayout(boutons)

        annuler.clicked.connect(self.reject)
        sauvegarder.clicked.connect(self.accept)

        self.setLayout(layout)



class BudgetEditDialog(QDialog):

    def __init__(
        self,
        budget,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setWindowTitle("Modifier un budget")
        self.resize(400, 200)

        layout = QVBoxLayout()

        titre = QLabel("Modifier le budget")
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        layout.addWidget(QLabel("Nom de l'événement"))
        self.nom = QLineEdit()
        self.nom.setText(str(budget[1] or ""))
        layout.addWidget(self.nom)

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
