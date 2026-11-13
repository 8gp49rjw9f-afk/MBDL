from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont


# Categories dans l'ordre d'affichage
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


def formater_montant(valeur):

    try:
        texte = (
            f"{float(valeur):,.2f}"
            .replace(",", " ")
            .replace(".", ",")
        )
        return texte + " $"
    except:
        return "0,00 $"


def calculer_montants(cumulatif, annee):

    # Retourne un dict: cle -> montant (depuis les pages existantes)
    from database import get_connection

    conn = get_connection()
    cursor = conn.cursor()

    montants = {}

    def valeur_unique(requete, parametres=()):
        try:
            cursor.execute(requete, parametres)
            resultat = cursor.fetchone()
            if resultat is None:
                return 0
            return resultat[0] or 0
        except:
            return 0

    annee_texte = f"{annee}%"

    # Sorties
    montants["sorties"] = valeur_unique(
        "SELECT SUM(montant) FROM sorties_argent WHERE est_separateur = 0"
    )

    # Entrees
    montants["entrees"] = valeur_unique(
        "SELECT SUM(montant) FROM entrees_argent WHERE est_separateur = 0"
    )

    # Pretes (capital restant)
    montants["prets"] = valeur_unique(
        "SELECT SUM(solde_actuel) FROM prets WHERE est_separateur = 0"
    )

    # Hypotheques (restant a payer)
    total_hypo = valeur_unique(
        "SELECT SUM(montant_initial) FROM hypotheques WHERE est_separateur = 0"
    )
    paye_hypo = valeur_unique(
        "SELECT SUM(montant_paye) FROM hypotheques WHERE est_separateur = 0"
    )
    restant_hypo = total_hypo - paye_hypo
    if restant_hypo < 0:
        restant_hypo = 0
    montants["hypotheques"] = restant_hypo

    # Placements (valeur actuelle)
    montants["placements"] = valeur_unique(
        "SELECT SUM(valeur_actuelle) FROM placements WHERE est_separateur = 0"
    )

    # REER / CELI (cotisations de l'annee courante)
    montants["reer"] = valeur_unique(
        """
        SELECT SUM(montant_initial) FROM placements
        WHERE est_separateur = 0 AND type_ligne = 'REER'
        AND date_inscription LIKE ?
        """,
        (annee_texte,)
    )

    montants["celi"] = valeur_unique(
        """
        SELECT SUM(montant_initial) FROM placements
        WHERE est_separateur = 0 AND type_ligne = 'CELI'
        AND date_inscription LIKE ?
        """,
        (annee_texte,)
    )

    # Taxes provinciales / federales / impots (depuis travail_autonome)
    # TPS = taxe federale, TVQ = taxe provinciale au Quebec
    facture_tps = valeur_unique(
        """
        SELECT SUM(montant_facture) FROM travail_autonome
        WHERE sans_tps = 0
        """
    )

    facture_tvq = valeur_unique(
        """
        SELECT SUM(montant_facture) FROM travail_autonome
        WHERE sans_tvq = 0
        """
    )

    montants["taxes_federales"] = facture_tps * 0.05
    montants["taxes_provinciales"] = facture_tvq * 0.09975

    # Patrimoine (somme des actifs)
    montants["patrimoine"] = valeur_unique(
        "SELECT SUM(montant) FROM patrimoine WHERE est_separateur = 0"
    )

    # Impots : tous les contrats (comme la page Taxes), sans filtre d'annee
    impot_brut = valeur_unique(
        """
        SELECT SUM(montant_facture * pourcentage_impot / 100)
        FROM travail_autonome
        WHERE sans_impot = 0
        """
    )

    provincial_paye = valeur_unique(
        "SELECT provincial_paye FROM acomptes WHERE id = 1"
    )
    federal_paye = valeur_unique(
        "SELECT federal_paye FROM acomptes WHERE id = 1"
    )

    # Le total peut etre negatif (trop d'acomptes verses)
    montants["impots"] = impot_brut - (provincial_paye + federal_paye)

    conn.close()

    return montants


class CumulatifViewDialog(QDialog):

    def __init__(self, cumulatif, parent=None):

        super().__init__(parent)

        from datetime import datetime
        annee = datetime.now().year

        self.cumulatif = cumulatif

        self.setWindowTitle(f"Cumulatif - {cumulatif[1]}")
        self.resize(600, 620)

        layout = QVBoxLayout()

        titre = QLabel(str(cumulatif[1] or ""))
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        # Calculer les montants
        montants = calculer_montants(cumulatif, annee)

        # Tableau a 2 colonnes
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Détail", "Montant"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.setColumnWidth(1, 180)

        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)

        layout.addWidget(self.table)

        # Total
        self.label_total = QLabel()
        self.label_total.setStyleSheet(
            "font-size:22px;font-weight:bold;padding:10px;"
        )
        layout.addWidget(self.label_total)

        self.setLayout(layout)

        # Remplir
        total = 0

        # Section sorties / dettes
        # Les impots sont traites a part : leur signe decide s'ils
        # reduisent (impot du) ou augmentent (remboursement) le total
        a_du_contenu = False
        for cle, libelle, cote in CATEGORIES:
            if cote != "gauche":
                continue
            if cle == "impots":
                continue
            if not cumulatif[INDEX_MAP[cle]]:
                continue
            a_du_contenu = True
            montant = montants.get(cle, 0)
            total -= montant
            self.ajouter_ligne(libelle, -montant)

        # Impots : signe libre
        if cumulatif[INDEX_MAP["impots"]]:
            a_du_contenu = True
            montant_impots = montants.get("impots", 0)
            if montant_impots > 0:
                # Remboursement : augmente le total
                total += montant_impots
                self.ajouter_ligne("Impôts (remboursement)", montant_impots)
            elif montant_impots < 0:
                # Impot a payer : diminue le total
                total += montant_impots
                self.ajouter_ligne("Impôts", montant_impots)
            else:
                self.ajouter_ligne("Impôts", 0)

        if a_du_contenu:
            self.ajouter_separateur()

        # Section entrees / avoirs
        for cle, libelle, cote in CATEGORIES:
            if cote != "droite":
                continue
            if not cumulatif[INDEX_MAP[cle]]:
                continue
            montant = montants.get(cle, 0)
            total += montant
            self.ajouter_ligne(libelle, montant)

        # Total en bas
        if total >= 0:
            texte_total = f"Total : +{formater_montant(total)}"
            couleur = "#1b7f2e"
        else:
            texte_total = f"Total : -{formater_montant(abs(total))}"
            couleur = "#c02020"

        self.label_total.setText(texte_total)
        self.label_total.setStyleSheet(
            f"font-size:22px;font-weight:bold;padding:10px;color:{couleur};"
        )


    def ajouter_ligne(self, libelle, montant):

        row = self.table.rowCount()
        self.table.insertRow(row)

        item_libelle = QTableWidgetItem(libelle)
        item_libelle.setFlags(Qt.ItemIsEnabled)

        if montant < 0:
            texte = f"-{formater_montant(abs(montant))}"
            couleur_texte = QColor(192, 32, 32)
        else:
            texte = f"+{formater_montant(montant)}"
            couleur_texte = QColor(27, 127, 46)

        item_montant = QTableWidgetItem(texte)
        item_montant.setFlags(Qt.ItemIsEnabled)
        item_montant.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        item_montant.setForeground(couleur_texte)
        item_montant.setBackground(QColor(245, 245, 245))

        self.table.setItem(row, 0, item_libelle)
        self.table.setItem(row, 1, item_montant)


    def ajouter_separateur(self):

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setSpan(row, 0, 1, 2)

        item = QTableWidgetItem("")
        item.setBackground(QColor(230, 230, 230))
        item.setFlags(Qt.ItemIsEnabled)
        self.table.setItem(row, 0, item)
        self.table.setRowHeight(row, 6)
