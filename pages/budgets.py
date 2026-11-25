from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QAbstractItemView
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from database import get_connection

from pages.budget_dialog import (
    BudgetDialog,
    BudgetEditDialog
)

from pages.budget_lignes_view_dialog import BudgetLignesViewDialog
from pages.separateur_dialog import SeparateurDialog



class BudgetsPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        titre = QLabel("Budgets prévisionnels")
        titre.setStyleSheet("font-size:28px;font-weight:bold;")
        layout.addWidget(titre)

        # =========================
        # TABLEAU
        # =========================

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            [
                "Nom de l'événement",
                "Budget actuel",
                "Détails",
                "Actions",
                ""
            ]
        )

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        layout.addWidget(self.table)

        # =========================
        # BOUTONS AJOUT
        # =========================

        boutons_ajout = QHBoxLayout()

        bouton = QPushButton("+ Ajouter un budget")
        bouton.clicked.connect(self.ouvrir_dialog)

        bouton_separateur = QPushButton("+ Ajouter un séparateur")
        bouton_separateur.clicked.connect(self.ouvrir_dialog_separateur)

        boutons_ajout.addWidget(bouton)
        boutons_ajout.addWidget(bouton_separateur)
        layout.addLayout(boutons_ajout)

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

        dialog = BudgetDialog()

        if dialog.exec():

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM budgets")
            position = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO budgets

                (
                nom,
                position
                )

                VALUES (?, ?)
                """,
                (
                    dialog.nom.text(),
                    position
                )
            )

            conn.commit()
            conn.close()

            self.charger()



    def ouvrir_dialog_separateur(self):

        dialog = SeparateurDialog()

        if dialog.exec():

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM budgets")
            position = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO budgets

                (
                nom,
                position,
                est_separateur
                )

                VALUES (?, ?, 1)
                """,
                (
                    dialog.nom.text(),
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
            est_separateur

            FROM budgets

            ORDER BY position
            """
        )

        resultats = cursor.fetchall()
        conn.close()

        self.table.clearSpans()
        self.table.setRowCount(0)

        for identifiant, nom, est_separateur in resultats:

            row = self.table.rowCount()
            self.table.insertRow(row)

            if est_separateur:

                self.table.setSpan(row, 0, 1, 4)

                item = QTableWidgetItem(nom)
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QColor(210, 210, 210))
                police = QFont()
                police.setBold(True)
                item.setFont(police)
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(row, 0, item)

                self.creer_actions(row, identifiant)
                self.table.setRowHeight(row, 22)

                continue

            # Calculer le budget actuel (somme des lignes)
            conn2 = get_connection()
            cursor2 = conn2.cursor()
            cursor2.execute(
                "SELECT SUM(prix) FROM budget_lignes WHERE budget_id = ?",
                (identifiant,)
            )
            total = cursor2.fetchone()[0] or 0
            conn2.close()

            valeurs = [
                nom or "",
                self.formater_montant(total)
            ]

            for colonne, valeur in enumerate(valeurs):
                item = QTableWidgetItem(valeur)
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(row, colonne, item)

            self.creer_actions(row, identifiant)



    def creer_actions(self, row, identifiant, est_separateur=False):

        if not est_separateur:

            bouton_voir = QPushButton("Voir")
            bouton_voir.setFixedWidth(50)
            bouton_voir.clicked.connect(
                lambda checked=False:
                self.voir(identifiant)
            )

            self.table.setCellWidget(row, 2, bouton_voir)

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



    def voir(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT

            id,
            nom,
            est_separateur

            FROM budgets

            WHERE id = ?
            """,
            (identifiant,)
        )

        resultat = cursor.fetchone()
        conn.close()

        if resultat is None or resultat[2]:
            return

        dialog = BudgetLignesViewDialog(resultat, self)
        dialog.exec()

        # Recharger pour mettre a jour le budget actuel
        self.charger()



    def monter(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT position FROM budgets WHERE id = ?",
            (identifiant,)
        )

        actuel = cursor.fetchone()

        if actuel is None or actuel[0] <= 0:
            conn.close()
            return

        position = actuel[0]

        cursor.execute(
            "UPDATE budgets SET position = position + 1 WHERE position = ?",
            (position - 1,)
        )

        cursor.execute(
            "UPDATE budgets SET position = ? WHERE id = ?",
            (position - 1, identifiant)
        )

        conn.commit()
        conn.close()

        self.charger()



    def descendre(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT position FROM budgets WHERE id = ?",
            (identifiant,)
        )

        actuel = cursor.fetchone()

        if actuel is None:
            conn.close()
            return

        position = actuel[0]

        cursor.execute("SELECT COUNT(*) FROM budgets")
        total = cursor.fetchone()[0]

        if position >= total - 1:
            conn.close()
            return

        cursor.execute(
            "UPDATE budgets SET position = position - 1 WHERE position = ?",
            (position + 1,)
        )

        cursor.execute(
            "UPDATE budgets SET position = ? WHERE id = ?",
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
            nom,
            est_separateur

            FROM budgets

            WHERE id = ?
            """,
            (identifiant,)
        )

        budget = cursor.fetchone()
        conn.close()

        if budget is None:
            return

        if budget[2]:

            dialog = SeparateurDialog(budget[1])

            if dialog.exec():

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    "UPDATE budgets SET nom = ? WHERE id = ?",
                    (dialog.nom.text(), identifiant)
                )

                conn.commit()
                conn.close()

                self.charger()

            return

        dialog = BudgetEditDialog(budget, self)

        if dialog.exec():

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE budgets SET nom = ? WHERE id = ?",
                (dialog.nom.text(), identifiant)
            )

            conn.commit()
            conn.close()

            self.charger()



    def supprimer(self, identifiant):

        confirmation = QMessageBox.question(
            self,
            "Suppression",
            "Supprimer ce budget et toutes ses lignes ?"
        )

        if confirmation == QMessageBox.Yes:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM budget_lignes WHERE budget_id = ?",
                (identifiant,)
            )

            cursor.execute(
                "DELETE FROM budgets WHERE id = ?",
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
            "SELECT id FROM budgets ORDER BY position"
        )

        lignes = cursor.fetchall()

        for index, ligne in enumerate(lignes):

            cursor.execute(
                "UPDATE budgets SET position = ? WHERE id = ?",
                (index, ligne[0])
            )

        conn.commit()
        conn.close()
