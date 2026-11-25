from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QMessageBox,
    QFrame
)


# (cle, libelle, cote)
CATEGORIES = [
    ("sorties", "Sorties", "gauche"),
    ("taxes_provinciales", "Taxes provinciales", "gauche"),
    ("taxes_federales", "Taxes fédérales", "gauche"),
    ("impots", "Impôts", "gauche"),
    ("prets", "Prêts", "gauche"),
    ("hypotheques", "Hypothèque", "gauche"),
    ("entrees", "Entrées", "droite"),
    ("placements", "Placements", "droite"),
    ("patrimoine", "Patrimoine", "droite"),
]

INDEX_MAP = {
    "entrees": 2, "sorties": 3, "taxes_provinciales": 4,
    "taxes_federales": 5, "impots": 6, "prets": 7,
    "hypotheques": 8, "placements": 9, "reer": 10, "celi": 11,
    "patrimoine": 12
}


class CumulatifConfigDialog(QDialog):

    def __init__(self, nom="", cumulatif=None, parent=None):

        super().__init__(parent)

        self.cumulatif = cumulatif
        self.mode_edition = cumulatif is not None

        if self.mode_edition:
            self.setWindowTitle("Modifier un cumulatif")
        else:
            self.setWindowTitle("Ajouter un cumulatif")

        self.resize(600, 480 if self.mode_edition else 240)

        layout = QVBoxLayout()

        titre = QLabel(
            "Modifier le cumulatif" if self.mode_edition else "Ajouter un cumulatif"
        )
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        # Nom
        layout.addWidget(QLabel("Nom du cumulatif"))
        self.nom = QLineEdit()
        self.nom.setText(str(nom or ""))
        self.nom.setPlaceholderText("Ex: Bilan complet, Projet maison...")
        layout.addWidget(self.nom)

        self.cases = {}

        # Cases a cocher : seulement en mode edition
        if self.mode_edition:

            info = QLabel("Éléments à inclure dans ce cumulatif :")
            info.setStyleSheet("font-size:14px;font-weight:bold;")
            layout.addWidget(info)

            colonnes = QHBoxLayout()
            colonnes.setSpacing(30)

            # Colonne gauche
            gauche = QVBoxLayout()
            titre_g = QLabel("Sorties")
            titre_g.setStyleSheet(
                "font-size:15px;font-weight:bold;background:#e8e8e8;padding:6px;"
            )
            gauche.addWidget(titre_g)

            for cle, libelle, cote in CATEGORIES:
                if cote != "gauche":
                    continue
                case = QCheckBox(libelle)
                self.cases[cle] = case
                gauche.addWidget(case)

            gauche.addStretch()
            colonnes.addLayout(gauche)

            # Colonne droite
            droite = QVBoxLayout()
            titre_d = QLabel("Entrées")
            titre_d.setStyleSheet(
                "font-size:15px;font-weight:bold;background:#e8e8e8;padding:6px;"
            )
            droite.addWidget(titre_d)

            for cle, libelle, cote in CATEGORIES:
                if cote != "droite":
                    continue
                case = QCheckBox(libelle)
                self.cases[cle] = case
                droite.addWidget(case)

            droite.addStretch()
            colonnes.addLayout(droite)

            layout.addLayout(colonnes)

            # Pre-remplir avec les valeurs enregistrees
            for cle, case in self.cases.items():
                index = INDEX_MAP.get(cle)
                if index is not None and index < len(cumulatif):
                    case.setChecked(bool(cumulatif[index]))

        else:

            info = QLabel(
                "Le cumulatif enregistrera les éléments\n"
                "actuellement cochés dans la page Cumulatif."
            )
            info.setStyleSheet("font-size:13px;color:#666;")
            layout.addWidget(info)

        # Boutons
        boutons = QHBoxLayout()
        annuler = QPushButton("Annuler")
        sauvegarder = QPushButton("Sauvegarder")
        sauvegarder.setDefault(
            True
        )
        sauvegarder.setAutoDefault(
            True
        )
        sauvegarder.setDefault(
            True
        )
        sauvegarder.setAutoDefault(
            True
        )
        boutons.addStretch()
        boutons.addWidget(annuler)
        boutons.addWidget(sauvegarder)
        layout.addLayout(boutons)

        annuler.clicked.connect(self.reject)
        sauvegarder.clicked.connect(self.sauvegarder)

        self.setLayout(layout)


    def sauvegarder(self):

        if not self.nom.text().strip():
            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez donner un nom au cumulatif."
            )
            return

        self.accept()


    def valeurs_cochees(self):

        valeurs = {cle: (1 if case.isChecked() else 0) for cle, case in self.cases.items()}

        # REER et CELI sont inclus dans Placements
        valeurs["reer"] = 0
        valeurs["celi"] = 0

        for cle in ["entrees", "sorties", "taxes_provinciales",
                    "taxes_federales", "impots", "prets",
                    "hypotheques", "placements", "patrimoine"]:
            valeurs.setdefault(cle, 0)

        return valeurs
