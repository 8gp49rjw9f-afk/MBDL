from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QFrame
)

from PySide6.QtCore import Qt


TAUX_TPS = 0.05
TAUX_TVQ = 0.09975
TAUX_TOTAL = 1 + TAUX_TPS + TAUX_TVQ


STYLE_TITRE = "font-size:20px;font-weight:bold;color:#333333;"
STYLE_INSTRUCTION = "color:#555555;font-size:14px;"
STYLE_MONTANT = "font-size:22px;font-weight:bold;color:#333333;"
STYLE_LIGNE = "color:#444444;font-size:15px;"


def convertir(valeur):

    try:

        return float(
            str(valeur)
            .replace(" ", "")
            .replace("\u00a0", "")
            .replace(",", ".")
            .replace("$", "")
        )

    except Exception:

        return 0.0


def formater_montant(valeur):

    try:

        return (
            f"{float(valeur):,.2f}"
            .replace(",", " ")
            .replace(".", ",")
            + " $"
        )

    except Exception:

        return "0,00 $"


class TpsTvqPage(QWidget):

    """
    Calcul des taxes dans les deux sens, cote a cote :
    a gauche, un montant avant taxes ;
    a droite, un montant taxes incluses.
    """

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        layout.setContentsMargins(24, 20, 24, 20)

        layout.setSpacing(14)

        titre = QLabel("TPS/TVQ")

        titre.setStyleSheet("font-size:28px;font-weight:bold;")

        layout.addWidget(titre)

        layout.addSpacing(4)

        colonnes = QHBoxLayout()

        colonnes.setSpacing(0)

        colonnes.addLayout(self.colonne_normale(), 1)

        colonnes.addWidget(self.separateur_vertical())

        colonnes.addLayout(self.colonne_inversee(), 1)

        layout.addLayout(colonnes)

        layout.addStretch()

        self.setLayout(layout)

        self.calculer()

    # =========================
    # SÉPARATEUR
    # =========================

    def separateur_vertical(self):

        ligne = QFrame()

        ligne.setFrameShape(QFrame.VLine)

        ligne.setFrameShadow(QFrame.Sunken)

        ligne.setStyleSheet("color:#cccccc;")

        return ligne

    # =========================
    # COLONNE DE GAUCHE — CALCUL NORMAL
    # =========================

    def colonne_normale(self):

        colonne = QVBoxLayout()

        colonne.setSpacing(8)

        colonne.setContentsMargins(0, 0, 24, 0)

        titre = QLabel("Avant taxes")

        titre.setStyleSheet(STYLE_TITRE)

        colonne.addWidget(titre)

        instruction = QLabel("Entrez un montant avant taxes")

        instruction.setStyleSheet(STYLE_INSTRUCTION)

        colonne.addWidget(instruction)

        colonne.addSpacing(4)

        self.montant = QLineEdit()

        self.montant.setPlaceholderText("0,00")

        self.montant.setAlignment(Qt.AlignRight)

        self.montant.textChanged.connect(self.calculer)

        colonne.addWidget(self.montant)

        colonne.addSpacing(10)

        self.tps = QLabel("TPS : 0,00 $")

        self.tps.setStyleSheet(STYLE_LIGNE)

        colonne.addWidget(self.tps)

        self.tvq = QLabel("TVQ : 0,00 $")

        self.tvq.setStyleSheet(STYLE_LIGNE)

        colonne.addWidget(self.tvq)

        colonne.addSpacing(8)

        self.total = QLabel("Total avec taxes : 0,00 $")

        self.total.setStyleSheet(STYLE_MONTANT)

        colonne.addWidget(self.total)

        colonne.addStretch()

        return colonne

    # =========================
    # COLONNE DE DROITE — CALCUL INVERSÉ
    # =========================

    def colonne_inversee(self):

        colonne = QVBoxLayout()

        colonne.setSpacing(8)

        colonne.setContentsMargins(24, 0, 0, 0)

        titre = QLabel("Avec taxe ( inversé )")

        titre.setStyleSheet(STYLE_TITRE)

        colonne.addWidget(titre)

        instruction = QLabel("Entrez un montant avec taxes incluses")

        instruction.setStyleSheet(STYLE_INSTRUCTION)

        colonne.addWidget(instruction)

        colonne.addSpacing(4)

        self.montant_inverse = QLineEdit()

        self.montant_inverse.setPlaceholderText("0,00")

        self.montant_inverse.setAlignment(Qt.AlignRight)

        self.montant_inverse.textChanged.connect(self.calculer)

        colonne.addWidget(self.montant_inverse)

        colonne.addSpacing(10)

        self.tps_inverse = QLabel("TPS incluse : 0,00 $")

        self.tps_inverse.setStyleSheet(STYLE_LIGNE)

        colonne.addWidget(self.tps_inverse)

        self.tvq_inverse = QLabel("TVQ incluse : 0,00 $")

        self.tvq_inverse.setStyleSheet(STYLE_LIGNE)

        colonne.addWidget(self.tvq_inverse)

        colonne.addSpacing(8)

        self.sans_taxes = QLabel("Montant sans taxes : 0,00 $")

        self.sans_taxes.setStyleSheet(STYLE_MONTANT)

        colonne.addWidget(self.sans_taxes)

        colonne.addStretch()

        return colonne

    # =========================
    # CALCUL
    # =========================

    def calculer(self):

        # --- Cote normal : avant taxes vers avec taxes ---

        montant = convertir(self.montant.text())

        tps = montant * TAUX_TPS
        tvq = montant * TAUX_TVQ

        self.tps.setText(f"TPS : {formater_montant(tps)}")

        self.tvq.setText(f"TVQ : {formater_montant(tvq)}")

        self.total.setText(
            "Total avec taxes : "
            + formater_montant(montant + tps + tvq)
        )

        # --- Cote inverse : avec taxes vers avant taxes ---

        montant_total = convertir(self.montant_inverse.text())

        sans_taxes = montant_total / TAUX_TOTAL if TAUX_TOTAL else 0.0

        self.tps_inverse.setText(
            "TPS incluse : " + formater_montant(sans_taxes * TAUX_TPS)
        )

        self.tvq_inverse.setText(
            "TVQ incluse : " + formater_montant(sans_taxes * TAUX_TVQ)
        )

        self.sans_taxes.setText(
            "Montant sans taxes : " + formater_montant(sans_taxes)
        )
