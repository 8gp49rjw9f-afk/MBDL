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

from pages.couverture_dialog import (
    CouvertureDialog,
    CouvertureEditDialog
)



class CouverturesViewDialog(QDialog):

    def __init__(
        self,
        assurance,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.assurance = assurance


        self.setWindowTitle(
            "Couvertures"
        )


        self.resize(
            875,
            500
        )


        layout = QVBoxLayout()


        # =========================
        # EN-TETE
        # =========================

        titre = QLabel(
            f"{assurance[1]} - {assurance[3]}"
        )

        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(
            titre
        )


        sous_titre = QLabel(
            f"Police : {assurance[2]}"
        )

        sous_titre.setStyleSheet(
            "font-size:16px;"
        )

        layout.addWidget(
            sous_titre
        )


        # =========================
        # TABLEAU
        # =========================

        self.table = QTableWidget()


        self.table.setColumnCount(
            5
        )


        self.table.setHorizontalHeaderLabels(
            [
                "Nom",
                "Montant assuré",
                "Franchise",
                "Autres informations",
                "Actions"
            ]
        )


        header = self.table.horizontalHeader()


        header.setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeToContents
        )


        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )


        layout.addWidget(
            self.table
        )


        # =========================
        # BOUTON AJOUT
        # =========================

        bouton = QPushButton(
            "+ Ajouter une couverture"
        )

        bouton.clicked.connect(
            self.ouvrir_dialog
        )

        layout.addWidget(
            bouton
        )


        self.setLayout(
            layout
        )


        self.charger()



    def formater_montant(
        self,
        valeur
    ):

        try:

            texte = (
                f"{float(valeur):,.2f}"
                .replace(",", " ")
                .replace(".", ",")
            )

            return texte + " $"

        except:

            return "0,00 $"



    def convertir(
        self,
        valeur
    ):

        try:

            return float(
                str(valeur)
                .replace(" ", "")
                .replace(",", ".")
                .replace("$", "")
            )

        except:

            return 0



    def ouvrir_dialog(
        self
    ):

        dialog = CouvertureDialog(
            self
        )


        if dialog.exec():

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)

                FROM couvertures

                WHERE assurance_id = ?
                """,
                (
                    self.assurance[0],
                )
            )

            position = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO couvertures

                (
                assurance_id,
                nom,
                type_montant,
                montant_assure,
                franchise,
                autres_infos,
                position
                )

                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.assurance[0],
                    dialog.nom.text(),
                    dialog.type_montant.currentText(),
                    self.convertir(dialog.montant_assure.text()),
                    self.convertir(dialog.franchise.text()),
                    dialog.autres_infos.text(),
                    position
                )
            )

            conn.commit()
            conn.close()

            self.charger()



    def charger(
        self
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT

            id,
            nom,
            type_montant,
            montant_assure,
            franchise,
            autres_infos

            FROM couvertures

            WHERE assurance_id = ?

            ORDER BY position
            """,
            (
                self.assurance[0],
            )
        )

        resultats = cursor.fetchall()
        conn.close()

        self.table.setRowCount(0)

        for identifiant, nom, type_montant, montant_assure, franchise, autres_infos in resultats:

            row = self.table.rowCount()
            self.table.insertRow(row)

            # Si pourcentage, afficher avec % sinon en $
            if type_montant and "Pourcentage" in type_montant:
                texte_montant = f"{montant_assure or 0:.2f} %"
            else:
                texte_montant = self.formater_montant(montant_assure or 0)

            valeurs = [
                nom or "",
                texte_montant,
                self.formater_montant(franchise or 0),
                autres_infos or ""
            ]

            for colonne, valeur in enumerate(valeurs):

                item = QTableWidgetItem(valeur)
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(row, colonne, item)

            self.creer_actions(row, identifiant)



    def creer_actions(
        self,
        row,
        identifiant
    ):

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

        self.table.setCellWidget(row, 4, actions)



    def monter(
        self,
        identifiant
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT position FROM couvertures WHERE id = ?",
            (identifiant,)
        )

        actuel = cursor.fetchone()

        if actuel is None or actuel[0] <= 0:
            conn.close()
            return

        position = actuel[0]

        cursor.execute(
            "UPDATE couvertures SET position = position + 1 WHERE position = ? AND assurance_id = ?",
            (position - 1, self.assurance[0])
        )

        cursor.execute(
            "UPDATE couvertures SET position = ? WHERE id = ?",
            (position - 1, identifiant)
        )

        conn.commit()
        conn.close()

        self.charger()



    def descendre(
        self,
        identifiant
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT position FROM couvertures WHERE id = ?",
            (identifiant,)
        )

        actuel = cursor.fetchone()

        if actuel is None:
            conn.close()
            return

        position = actuel[0]

        cursor.execute(
            "SELECT COUNT(*) FROM couvertures WHERE assurance_id = ?",
            (self.assurance[0],)
        )

        total = cursor.fetchone()[0]

        if position >= total - 1:
            conn.close()
            return

        cursor.execute(
            "UPDATE couvertures SET position = position - 1 WHERE position = ? AND assurance_id = ?",
            (position + 1, self.assurance[0])
        )

        cursor.execute(
            "UPDATE couvertures SET position = ? WHERE id = ?",
            (position + 1, identifiant)
        )

        conn.commit()
        conn.close()

        self.charger()



    def modifier(
        self,
        identifiant
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT

            id,
            assurance_id,
            nom,
            type_montant,
            montant_assure,
            franchise,
            autres_infos

            FROM couvertures

            WHERE id = ?
            """,
            (identifiant,)
        )

        couverture = cursor.fetchone()
        conn.close()

        if couverture is None:
            return

        dialog = CouvertureEditDialog(couverture, self)

        if dialog.exec():

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE couvertures

                SET

                nom = ?,

                type_montant = ?,

                montant_assure = ?,

                franchise = ?,

                autres_infos = ?

                WHERE id = ?
                """,
                (
                    dialog.nom.text(),
                    dialog.type_montant.currentText(),
                    self.convertir(dialog.montant_assure.text()),
                    self.convertir(dialog.franchise.text()),
                    dialog.autres_infos.text(),
                    identifiant
                )
            )

            conn.commit()
            conn.close()

            self.charger()



    def supprimer(
        self,
        identifiant
    ):

        confirmation = QMessageBox.question(
            self,
            "Suppression",
            "Supprimer cette couverture ?"
        )

        if confirmation == QMessageBox.Yes:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM couvertures WHERE id = ?",
                (identifiant,)
            )

            conn.commit()
            conn.close()

            self.reorganiser_positions()
            self.charger()



    def reorganiser_positions(
        self
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM couvertures WHERE assurance_id = ? ORDER BY position",
            (self.assurance[0],)
        )

        lignes = cursor.fetchall()

        for index, ligne in enumerate(lignes):

            cursor.execute(
                "UPDATE couvertures SET position = ? WHERE id = ?",
                (index, ligne[0])
            )

        conn.commit()
        conn.close()