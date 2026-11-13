from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton,
    QFrame,
    QMessageBox
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from database import get_connection

from pages.cumulatif_view_dialog import (
    formater_montant,
    calculer_montants
)

from pages.cumulatifs_liste_dialog import CumulatifsListeDialog


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


class CumulatifPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        titre = QLabel("Cumulatif")
        titre.setStyleSheet("font-size:28px;font-weight:bold;")
        layout.addWidget(titre)

        # =========================
        # DEUX PANNEAUX
        # =========================

        panneaux = QHBoxLayout()
        panneaux.setSpacing(30)

        self.cases = {}

        # ---- Panneau gauche (Sorties / Dettes) ----
        gauche = QVBoxLayout()

        titre_gauche = QLabel("Sorties")
        titre_gauche.setStyleSheet(
            "font-size:18px;font-weight:bold;background:#e8e8e8;padding:8px;"
        )
        titre_gauche.setAlignment(Qt.AlignCenter)
        gauche.addWidget(titre_gauche)

        for cle, libelle, cote in CATEGORIES:
            if cote != "gauche":
                continue
            case = QCheckBox(libelle)
            case.stateChanged.connect(self.recalculer)
            self.cases[cle] = case
            gauche.addWidget(case)

        gauche.addStretch()

        self.total_gauche = QLabel()
        self.total_gauche.setStyleSheet("font-size:20px;font-weight:bold;")
        gauche.addWidget(self.total_gauche)

        ligne_g = QFrame()
        ligne_g.setFrameShape(QFrame.HLine)
        gauche.addWidget(ligne_g)

        panneaux.addLayout(gauche)

        # ---- Panneau droit (Entrées / Avoirs) ----
        droite = QVBoxLayout()

        titre_droite = QLabel("Entrées")
        titre_droite.setStyleSheet(
            "font-size:18px;font-weight:bold;background:#e8e8e8;padding:8px;"
        )
        titre_droite.setAlignment(Qt.AlignCenter)
        droite.addWidget(titre_droite)

        for cle, libelle, cote in CATEGORIES:
            if cote != "droite":
                continue
            case = QCheckBox(libelle)
            case.stateChanged.connect(self.recalculer)
            self.cases[cle] = case
            droite.addWidget(case)

        droite.addStretch()

        self.total_droite = QLabel()
        self.total_droite.setStyleSheet("font-size:20px;font-weight:bold;")
        droite.addWidget(self.total_droite)

        ligne_d = QFrame()
        ligne_d.setFrameShape(QFrame.HLine)
        droite.addWidget(ligne_d)

        panneaux.addLayout(droite)

        layout.addLayout(panneaux)

        layout.addStretch()

        # =========================
        # BOUTONS
        # =========================

        bouton_creer = QPushButton("Ajouter un cumulatif")
        bouton_creer.setStyleSheet("font-size:16px;font-weight:bold;padding:12px;")
        bouton_creer.clicked.connect(self.creer_cumulatif)
        layout.addWidget(bouton_creer)

        bouton_voir = QPushButton("Voir les cumulatifs")
        bouton_voir.setStyleSheet("font-size:16px;font-weight:bold;padding:12px;")
        bouton_voir.clicked.connect(self.voir_cumulatifs)
        layout.addWidget(bouton_voir)

        self.setLayout(layout)

        self.recalculer()



    def showEvent(self, event):
        super().showEvent(event)
        self.recalculer()



    def cases_cochees(self):

        # Retourne une liste cumulatif-like pour calculer_montants
        valeurs = [0] * 12
        for cle, case in self.cases.items():
            if case.isChecked():
                valeurs[INDEX_MAP[cle]] = 1
        return valeurs



    def recalculer(self):

        annee = datetime.now().year

        # Ordre attendu par calculer_montants et INDEX_MAP
        cumulatif_fictif = [0, ""]
        for cle in ["entrees", "sorties", "taxes_provinciales", "taxes_federales",
                    "impots", "prets", "hypotheques", "placements", "reer", "celi",
                    "patrimoine"]:
            if cle in self.cases:
                cumulatif_fictif.append(1 if self.cases[cle].isChecked() else 0)
            else:
                cumulatif_fictif.append(0)

        montants = calculer_montants(cumulatif_fictif, annee)

        # Colonne Sorties : chaque montant est une depense qui reduit l'avoir.
        # Exception : les Impots peuvent etre positifs (remboursement d'acomptes).
        total_gauche = 0
        for cle, libelle, cote in CATEGORIES:
            if cote != "gauche":
                continue
            if not self.cases[cle].isChecked():
                continue

            montant = montants.get(cle, 0)

            if cle == "impots":
                # Le montant est deja net :
                #   +1000 => je dois 1000 => -1000 dans le total
                #   -1000 => on me doit 1000 => +1000 dans le total
                total_gauche -= montant
            else:
                total_gauche -= abs(montant)

        total_droite = 0
        for cle, libelle, cote in CATEGORIES:
            if cote == "droite" and self.cases[cle].isChecked():
                total_droite += abs(montants.get(cle, 0))

        # Affichage de la colonne Sorties
        self.total_gauche.setText(
            f"Total : {formater_montant(total_gauche)}"
        )

        if total_gauche < 0:
            self.total_gauche.setStyleSheet(
                "font-size:20px;font-weight:bold;color:#c02020;"
            )
        elif total_gauche > 0:
            self.total_gauche.setStyleSheet(
                "font-size:20px;font-weight:bold;color:#1b7f2e;"
            )
        else:
            self.total_gauche.setStyleSheet("font-size:20px;font-weight:bold;")

        # Affichage de la colonne Entrées
        self.total_droite.setText(
            f"Total : {formater_montant(total_droite)}"
        )

        if total_droite > 0:
            self.total_droite.setStyleSheet(
                "font-size:20px;font-weight:bold;color:#1b7f2e;"
            )
        else:
            self.total_droite.setStyleSheet("font-size:20px;font-weight:bold;")



    def creer_cumulatif(self):

        # Popup simple: un nom seulement
        from pages.cumulatif_config_dialog import CumulatifConfigDialog

        dialog = CumulatifConfigDialog(parent=self)

        if dialog.exec():

            # Ce qui est enregistre = les cases cochees dans la page
            values = {}
            for cle, case in self.cases.items():
                values[cle] = 1 if case.isChecked() else 0

            # REER et CELI sont inclus dans Placements
            values["reer"] = 0
            values["celi"] = 0

            for cle in ["entrees", "sorties", "taxes_provinciales",
                        "taxes_federales", "impots", "prets",
                        "hypotheques", "placements", "patrimoine"]:
                values.setdefault(cle, 0)

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM cumulatifs")
            position = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO cumulatifs

                (
                nom, entrees, sorties, taxes_provinciales, taxes_federales,
                impots, prets, hypotheques, placements, reer, celi,
                patrimoine, position
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    dialog.nom.text(),
                    values.get("entrees", 0), values.get("sorties", 0),
                    values.get("taxes_provinciales", 0), values.get("taxes_federales", 0),
                    values.get("impots", 0), values.get("prets", 0),
                    values.get("hypotheques", 0), values.get("placements", 0),
                    values.get("reer", 0), values.get("celi", 0),
                    values.get("patrimoine", 0),
                    position
                )
            )

            conn.commit()
            conn.close()

            QMessageBox.information(
                self,
                "Cumulatif enregistré",
                "Le cumulatif « " + dialog.nom.text() + " » a été enregistré."
            )


    def voir_cumulatifs(self):

        dialog = CumulatifsListeDialog(self)
        dialog.exec()
