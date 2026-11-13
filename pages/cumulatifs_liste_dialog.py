from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QAbstractItemView,
    QWidget
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from database import get_connection

from pages.cumulatif_config_dialog import CumulatifConfigDialog
from pages.cumulatif_view_dialog import (
    CumulatifViewDialog,
    calculer_montants,
    formater_montant,
    INDEX_MAP,
    CATEGORIES
)


class CumulatifsListeDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Mes cumulatifs")
        self.resize(750, 500)

        layout = QVBoxLayout()

        titre = QLabel("Mes cumulatifs")
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        # Tableau: Nom, Montant, Ouvrir, Actions
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Nom", "Montant", "Ouvrir", "Actions", ""]
        )

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        layout.addWidget(self.table)

        # Bouton fermer
        bouton_fermer = QPushButton("Fermer")
        bouton_fermer.clicked.connect(self.accept)
        layout.addWidget(bouton_fermer)

        self.setLayout(layout)

        self.charger()


    def creer(self):

        dialog = CumulatifConfigDialog(parent=self)

        if dialog.exec():

            # Reprendre les cases cochees de la page Cumulatif
            parent = self.parent()

            values = {}
            if parent is not None and hasattr(parent, "cases"):
                for cle, case in parent.cases.items():
                    values[cle] = 1 if case.isChecked() else 0

            for cle in ["entrees", "sorties", "taxes_provinciales",
                        "taxes_federales", "impots", "prets",
                        "hypotheques", "placements", "patrimoine"]:
                values.setdefault(cle, 0)

            values["reer"] = 0
            values["celi"] = 0

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

            self.charger()


    def charger(self):

        from datetime import datetime
        annee = datetime.now().year

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, nom, entrees, sorties, taxes_provinciales, taxes_federales,
                   impots, prets, hypotheques, placements, reer, celi,
                   patrimoine, position

            FROM cumulatifs

            ORDER BY position, id
            """
        )
        resultats = cursor.fetchall()
        conn.close()

        self.table.clearSpans()
        self.table.setRowCount(0)

        for ligne in resultats:

            row = self.table.rowCount()
            self.table.insertRow(row)

            identifiant = ligne[0]

            # Calculer le montant total
            montants = calculer_montants(ligne, annee)

            total = 0
            for cle, libelle, cote in CATEGORIES:
                if not ligne[INDEX_MAP[cle]]:
                    continue
                if cote == "gauche":
                    total -= montants.get(cle, 0)
                else:
                    total += montants.get(cle, 0)

            # Nom
            item_nom = QTableWidgetItem(str(ligne[1] or ""))
            item_nom.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(row, 0, item_nom)

            # Montant avec couleur
            if total >= 0:
                texte = f"+{formater_montant(total)}"
                item_montant = QTableWidgetItem(texte)
                item_montant.setForeground(QColor(27, 127, 46))
            else:
                texte = f"-{formater_montant(abs(total))}"
                item_montant = QTableWidgetItem(texte)
                item_montant.setForeground(QColor(192, 32, 32))

            item_montant.setFlags(Qt.ItemIsEnabled)
            item_montant.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 1, item_montant)

            # Bouton Ouvrir
            bouton_ouvrir = QPushButton("Ouvrir")
            bouton_ouvrir.setFixedWidth(70)
            bouton_ouvrir.clicked.connect(
                lambda checked=False, c=ligne:
                self.ouvrir(c)
            )
            self.table.setCellWidget(row, 2, bouton_ouvrir)

            # Actions
            self.creer_actions(row, identifiant)


    def creer_actions(self, row, identifiant):

        actions = QWidget()
        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(0, 0, 0, 0)

        monter = QPushButton("↑")
        monter.setFixedWidth(25)
        monter.clicked.connect(lambda: self.monter(identifiant))

        descendre = QPushButton("↓")
        descendre.setFixedWidth(25)
        descendre.clicked.connect(lambda: self.descendre(identifiant))

        modifier = QPushButton("Edit")
        modifier.setFixedWidth(45)
        modifier.clicked.connect(lambda: self.modifier(identifiant))

        supprimer = QPushButton("X")
        supprimer.setFixedWidth(25)
        supprimer.clicked.connect(lambda: self.supprimer(identifiant))

        actions_layout.addWidget(monter)
        actions_layout.addWidget(descendre)
        actions_layout.addWidget(modifier)
        actions_layout.addWidget(supprimer)

        actions.setLayout(actions_layout)
        self.table.setCellWidget(row, 3, actions)


    def ouvrir(self, cumulatif):

        dialog = CumulatifViewDialog(cumulatif, self)
        dialog.exec()


    def modifier(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, nom, entrees, sorties, taxes_provinciales, taxes_federales,
                   impots, prets, hypotheques, placements, reer, celi,
                   patrimoine, position

            FROM cumulatifs

            WHERE id = ?
            """,
            (identifiant,)
        )
        cumulatif = cursor.fetchone()
        conn.close()

        if cumulatif is None:
            return

        # On passe le cumulatif complet pour pre-remplir les cases a cocher
        dialog = CumulatifConfigDialog(
            nom=cumulatif[1],
            cumulatif=cumulatif,
            parent=self
        )

        if dialog.exec():

            values = dialog.valeurs_cochees()

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE cumulatifs

                SET nom = ?, entrees = ?, sorties = ?, taxes_provinciales = ?,
                    taxes_federales = ?, impots = ?, prets = ?, hypotheques = ?,
                    placements = ?, reer = ?, celi = ?, patrimoine = ?

                WHERE id = ?
                """,
                (
                    dialog.nom.text(),
                    values.get("entrees", 0), values.get("sorties", 0),
                    values.get("taxes_provinciales", 0), values.get("taxes_federales", 0),
                    values.get("impots", 0), values.get("prets", 0),
                    values.get("hypotheques", 0), values.get("placements", 0),
                    values.get("reer", 0), values.get("celi", 0),
                    values.get("patrimoine", 0),
                    identifiant
                )
            )
            conn.commit()
            conn.close()

            self.charger()


    def supprimer(self, identifiant):

        confirmation = QMessageBox.question(
            self,
            "Suppression",
            "Supprimer ce cumulatif ?"
        )

        if confirmation == QMessageBox.Yes:

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cumulatifs WHERE id = ?", (identifiant,))
            conn.commit()
            conn.close()

            self.reorganiser_positions()
            self.charger()


    def monter(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT position FROM cumulatifs WHERE id = ?", (identifiant,))
        actuel = cursor.fetchone()

        if actuel is None or actuel[0] <= 0:
            conn.close()
            return

        position = actuel[0]
        cursor.execute("UPDATE cumulatifs SET position = position + 1 WHERE position = ?", (position - 1,))
        cursor.execute("UPDATE cumulatifs SET position = ? WHERE id = ?", (position - 1, identifiant))
        conn.commit()
        conn.close()
        self.charger()


    def descendre(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT position FROM cumulatifs WHERE id = ?", (identifiant,))
        actuel = cursor.fetchone()

        if actuel is None:
            conn.close()
            return

        position = actuel[0]
        cursor.execute("SELECT COUNT(*) FROM cumulatifs")
        total = cursor.fetchone()[0]

        if position >= total - 1:
            conn.close()
            return

        cursor.execute("UPDATE cumulatifs SET position = position - 1 WHERE position = ?", (position + 1,))
        cursor.execute("UPDATE cumulatifs SET position = ? WHERE id = ?", (position + 1, identifiant))
        conn.commit()
        conn.close()
        self.charger()


    def reorganiser_positions(self):

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM cumulatifs ORDER BY position")
        lignes = cursor.fetchall()

        for index, ligne in enumerate(lignes):
            cursor.execute("UPDATE cumulatifs SET position = ? WHERE id = ?", (index, ligne[0]))

        conn.commit()
        conn.close()
