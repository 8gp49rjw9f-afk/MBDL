from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QHBoxLayout
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from database import get_connection
from pages.patrimoine_dialog import PatrimoineDialog, PatrimoineEditDialog
from pages.separateur_dialog import SeparateurDialog


class PatrimoinePage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        titre = QLabel("Patrimoine")
        titre.setStyleSheet("font-size:28px;font-weight:bold;")
        layout.addWidget(titre)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nom", "Valeur", "Actions"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        layout.addWidget(self.table)

        boutons_ajout = QHBoxLayout()

        bouton = QPushButton("+ Ajouter un actif")
        bouton.clicked.connect(self.ouvrir_dialog)

        bouton_separateur = QPushButton("+ Ajouter un séparateur")
        bouton_separateur.clicked.connect(self.ouvrir_dialog_separateur)

        boutons_ajout.addWidget(bouton)
        boutons_ajout.addWidget(bouton_separateur)
        layout.addLayout(boutons_ajout)

        self.total = QLabel("Total : 0,00 $")
        self.total.setStyleSheet("font-size:18px;font-weight:bold;")
        layout.addWidget(self.total)

        self.setLayout(layout)

        self.charger()



    def formater_montant(self, valeur):
        try:
            texte = f"{float(valeur):,.2f}".replace(",", " ").replace(".", ",")
            return texte + " $"
        except:
            return "0,00 $"



    def convertir(self, valeur):
        try:
            return float(str(valeur).replace(" ", "").replace(",", ".").replace("$", ""))
        except:
            return 0



    def ouvrir_dialog(self):

        dialog = PatrimoineDialog()

        if dialog.exec():

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM patrimoine")
            position = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO patrimoine

                (nom, montant, position)

                VALUES (?, ?, ?)
                """,
                (
                    dialog.nom.text(),
                    self.convertir(dialog.montant.text()),
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

            cursor.execute("SELECT COUNT(*) FROM patrimoine")
            position = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO patrimoine

                (nom, montant, position, est_separateur)

                VALUES (?, 0, ?, 1)
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
            SELECT id, nom, montant, est_separateur

            FROM patrimoine

            ORDER BY position
            """
        )
        resultats = cursor.fetchall()
        conn.close()

        self.table.clearSpans()
        self.table.setRowCount(0)

        total = 0

        for identifiant, nom, montant, est_separateur in resultats:

            row = self.table.rowCount()
            self.table.insertRow(row)

            if est_separateur:

                self.table.setSpan(row, 0, 1, 2)

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

            montant = montant or 0
            total += montant

            item_nom = QTableWidgetItem(nom)
            item_nom.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(row, 0, item_nom)

            item_montant = QTableWidgetItem(self.formater_montant(montant))
            item_montant.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(row, 1, item_montant)

            self.creer_actions(row, identifiant)

        self.total.setText("Total : " + self.formater_montant(total))



    def creer_actions(self, row, identifiant):

        actions = QWidget()
        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(0, 0, 0, 0)

        monter = QPushButton("↑")
        monter.setFixedWidth(30)
        monter.clicked.connect(lambda: self.monter(identifiant))

        descendre = QPushButton("↓")
        descendre.setFixedWidth(30)
        descendre.clicked.connect(lambda: self.descendre(identifiant))

        modifier = QPushButton("Edit")
        modifier.setFixedWidth(45)
        modifier.clicked.connect(lambda: self.modifier(identifiant))

        supprimer = QPushButton("X")
        supprimer.setFixedWidth(30)
        supprimer.clicked.connect(lambda: self.supprimer(identifiant))

        actions_layout.addWidget(monter)
        actions_layout.addWidget(descendre)
        actions_layout.addWidget(modifier)
        actions_layout.addWidget(supprimer)

        actions.setLayout(actions_layout)
        self.table.setCellWidget(row, 2, actions)



    def monter(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT position FROM patrimoine WHERE id = ?", (identifiant,))
        actuel = cursor.fetchone()

        if actuel is None or actuel[0] <= 0:
            conn.close()
            return

        position = actuel[0]
        cursor.execute("UPDATE patrimoine SET position = position + 1 WHERE position = ?", (position - 1,))
        cursor.execute("UPDATE patrimoine SET position = ? WHERE id = ?", (position - 1, identifiant))
        conn.commit()
        conn.close()
        self.charger()



    def descendre(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT position FROM patrimoine WHERE id = ?", (identifiant,))
        actuel = cursor.fetchone()

        if actuel is None:
            conn.close()
            return

        position = actuel[0]
        cursor.execute("SELECT COUNT(*) FROM patrimoine")
        total = cursor.fetchone()[0]

        if position >= total - 1:
            conn.close()
            return

        cursor.execute("UPDATE patrimoine SET position = position - 1 WHERE position = ?", (position + 1,))
        cursor.execute("UPDATE patrimoine SET position = ? WHERE id = ?", (position + 1, identifiant))
        conn.commit()
        conn.close()
        self.charger()



    def modifier(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT nom, montant, est_separateur FROM patrimoine WHERE id = ?",
            (identifiant,)
        )
        resultat = cursor.fetchone()
        conn.close()

        if resultat is None:
            return

        nom, montant, est_separateur = resultat

        if est_separateur:

            dialog = SeparateurDialog(nom)

            if dialog.exec():
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE patrimoine SET nom = ? WHERE id = ?",
                    (dialog.nom.text(), identifiant)
                )
                conn.commit()
                conn.close()
                self.charger()

            return

        dialog = PatrimoineEditDialog(nom, montant)

        if dialog.exec():

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE patrimoine

                SET nom = ?, montant = ?

                WHERE id = ?
                """,
                (
                    dialog.nom.text(),
                    self.convertir(dialog.montant.text()),
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
            cursor.execute("DELETE FROM patrimoine WHERE id = ?", (identifiant,))
            conn.commit()
            conn.close()

            self.reorganiser_positions()
            self.charger()



    def reorganiser_positions(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM patrimoine ORDER BY position")
        lignes = cursor.fetchall()

        for index, ligne in enumerate(lignes):
            cursor.execute("UPDATE patrimoine SET position = ? WHERE id = ?", (index, ligne[0]))

        conn.commit()
        conn.close()
