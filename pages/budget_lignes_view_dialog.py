from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from database import get_connection

from pages.budget_ligne_dialog import (
    BudgetLigneDialog,
    BudgetLigneEditDialog
)



class BudgetLignesViewDialog(QDialog):

    def __init__(
        self,
        budget,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.budget = budget

        self.setWindowTitle("Détails du budget")
        self.resize(800, 500)

        layout = QVBoxLayout()

        # En-tete
        titre = QLabel(str(budget[1] or ""))
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        self.total_label = QLabel()
        self.total_label.setStyleSheet("font-size:16px;font-weight:bold;")
        layout.addWidget(self.total_label)

        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            [
                "Nom",
                "Prix",
                "Autres informations",
                "Actions"
            ]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(self.table)

        # Bouton ajout
        bouton = QPushButton("+ Ajouter une ligne")
        bouton.clicked.connect(self.ouvrir_dialog)
        layout.addWidget(bouton)

        self.setLayout(layout)
        self.charger()



    def formater_montant(self, valeur):

        try:
            texte = (
                f"{float(valeur):,.2f}"
                .replace(",", " ")
                .replace(".", ",")
            )
            return texte + " $"
        except:
            return "0,00 $"



    def convertir(self, valeur):

        try:
            return float(
                str(valeur)
                .replace(" ", "")
                .replace(",", ".")
                .replace("$", "")
            )
        except:
            return 0



    def ouvrir_dialog(self):

        dialog = BudgetLigneDialog(self)

        if dialog.exec():

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT COUNT(*) FROM budget_lignes WHERE budget_id = ?",
                (self.budget[0],)
            )

            position = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO budget_lignes

                (
                budget_id,
                nom,
                prix,
                autres_infos,
                position
                )

                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    self.budget[0],
                    dialog.nom.text(),
                    self.convertir(dialog.prix.text()),
                    dialog.autres_infos.text(),
                    position
                )
            )

            conn.commit()
            conn.close()

            self.charger()



    def charger(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT

            id,
            nom,
            prix,
            autres_infos

            FROM budget_lignes

            WHERE budget_id = ?

            ORDER BY position
            """,
            (self.budget[0],)
        )

        resultats = cursor.fetchall()
        conn.close()

        self.table.setRowCount(0)

        total = 0

        for identifiant, nom, prix, autres_infos in resultats:

            row = self.table.rowCount()
            self.table.insertRow(row)

            prix = prix or 0
            total += prix

            valeurs = [
                nom or "",
                self.formater_montant(prix),
                autres_infos or ""
            ]

            for colonne, valeur in enumerate(valeurs):

                item = QTableWidgetItem(valeur)
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(row, colonne, item)

            self.creer_actions(row, identifiant)

        self.total_label.setText(
            f"Budget actuel : {self.formater_montant(total)}"
        )



    def creer_actions(self, row, identifiant):

        actions = QWidget()
        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(0, 0, 0, 0)

        monter = QPushButton("↑")
        monter.setFixedWidth(25)
        monter.clicked.connect(
            lambda checked=False:
            self.monter(identifiant)
        )

        descendre = QPushButton("↓")
        descendre.setFixedWidth(25)
        descendre.clicked.connect(
            lambda checked=False:
            self.descendre(identifiant)
        )

        modifier = QPushButton("Edit")
        modifier.setFixedWidth(45)
        modifier.clicked.connect(
            lambda checked=False:
            self.modifier(identifiant)
        )

        supprimer = QPushButton("X")
        supprimer.setFixedWidth(25)
        supprimer.clicked.connect(
            lambda checked=False:
            self.supprimer(identifiant)
        )

        actions_layout.addWidget(monter)
        actions_layout.addWidget(descendre)
        actions_layout.addWidget(modifier)
        actions_layout.addWidget(supprimer)

        actions.setLayout(actions_layout)

        self.table.setCellWidget(row, 3, actions)



    def monter(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT position FROM budget_lignes WHERE id = ?",
            (identifiant,)
        )

        actuel = cursor.fetchone()

        if actuel is None or actuel[0] <= 0:
            conn.close()
            return

        position = actuel[0]

        cursor.execute(
            "UPDATE budget_lignes SET position = position + 1 WHERE position = ? AND budget_id = ?",
            (position - 1, self.budget[0])
        )

        cursor.execute(
            "UPDATE budget_lignes SET position = ? WHERE id = ?",
            (position - 1, identifiant)
        )

        conn.commit()
        conn.close()

        self.charger()



    def descendre(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT position FROM budget_lignes WHERE id = ?",
            (identifiant,)
        )

        actuel = cursor.fetchone()

        if actuel is None:
            conn.close()
            return

        position = actuel[0]

        cursor.execute(
            "SELECT COUNT(*) FROM budget_lignes WHERE budget_id = ?",
            (self.budget[0],)
        )

        total = cursor.fetchone()[0]

        if position >= total - 1:
            conn.close()
            return

        cursor.execute(
            "UPDATE budget_lignes SET position = position - 1 WHERE position = ? AND budget_id = ?",
            (position + 1, self.budget[0])
        )

        cursor.execute(
            "UPDATE budget_lignes SET position = ? WHERE id = ?",
            (position + 1, identifiant)
        )

        conn.commit()
        conn.close()

        self.charger()



    def modifier(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT

            id,
            budget_id,
            nom,
            prix,
            autres_infos

            FROM budget_lignes

            WHERE id = ?
            """,
            (identifiant,)
        )

        ligne = cursor.fetchone()
        conn.close()

        if ligne is None:
            return

        dialog = BudgetLigneEditDialog(ligne, self)

        if dialog.exec():

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE budget_lignes

                SET

                nom = ?,

                prix = ?,

                autres_infos = ?

                WHERE id = ?
                """,
                (
                    dialog.nom.text(),
                    self.convertir(dialog.prix.text()),
                    dialog.autres_infos.text(),
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
            "Supprimer cette ligne ?"
        )

        if confirmation == QMessageBox.Yes:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM budget_lignes WHERE id = ?",
                (identifiant,)
            )

            conn.commit()
            conn.close()

            self.reorganiser_positions()
            self.charger()



    def reorganiser_positions(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM budget_lignes WHERE budget_id = ? ORDER BY position",
            (self.budget[0],)
        )

        lignes = cursor.fetchall()

        for index, ligne in enumerate(lignes):

            cursor.execute(
                "UPDATE budget_lignes SET position = ? WHERE id = ?",
                (index, ligne[0])
            )

        conn.commit()
        conn.close()
