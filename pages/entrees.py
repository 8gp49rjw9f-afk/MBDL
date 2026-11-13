from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QHBoxLayout,
    QAbstractItemView
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from database import get_connection
from pages.entree_edit_dialog import EntreeEditDialog
from pages.entree_dialog import EntreeDialog
from pages.separateur_dialog import SeparateurDialog



class EntreesPage(QWidget):

    def __init__(self):

        super().__init__()


        layout = QVBoxLayout()


        # =========================
        # TITRE
        # =========================

        titre = QLabel(
            "Entrées"
        )

        titre.setStyleSheet(
            "font-size:28px;font-weight:bold;"
        )

        layout.addWidget(
            titre
        )


        # =========================
        # TABLEAU
        # =========================

        self.table = QTableWidget()

        self.table.setColumnCount(
            3
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Nom",
                "Montant ✎",
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


        layout.addWidget(
            self.table
        )


        # =========================
        # BOUTONS AJOUT
        # =========================

        boutons_ajout = QHBoxLayout()


        bouton = QPushButton(
            "+ Ajouter une entrée"
        )

        bouton.clicked.connect(
            self.ouvrir_dialog
        )


        bouton_separateur = QPushButton(
            "+ Ajouter un séparateur"
        )

        bouton_separateur.clicked.connect(
            self.ouvrir_dialog_separateur
        )


        boutons_ajout.addWidget(
            bouton
        )

        boutons_ajout.addWidget(
            bouton_separateur
        )


        layout.addLayout(
            boutons_ajout
        )


        # =========================
        # TOTAL
        # =========================

        self.total = QLabel(
            "Total : 0,00 $"
        )

        self.total.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )

        layout.addWidget(
            self.total
        )


        self.setLayout(
            layout
        )


        self.table.blockSignals(True)

        self.table.cellChanged.connect(
            self.valeur_modifiee
        )

        self.table.blockSignals(False)

        self.charger()



    def valeur_modifiee(
        self,
        row,
        column
    ):

        if column != 1:
            return

        item = self.table.item(
            row,
            column
        )

        if item is None:
            return

        nouvelle_valeur = self.convertir(
            item.text()
        )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id

            FROM entrees_argent

            ORDER BY position
            """
        )

        lignes = cursor.fetchall()

        if row < len(lignes):

            cursor.execute(
                """
                UPDATE entrees_argent

                SET montant = ?

                WHERE id = ?
                """,
                (
                    nouvelle_valeur,
                    lignes[row][0]
                )
            )

            conn.commit()

        conn.close()

        self.charger()



    # =========================
    # FORMAT MONTANT
    # =========================

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



    # =========================
    # CONVERSION
    # =========================

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



    # =========================
    # AJOUT
    # =========================

    def ouvrir_dialog(
        self
    ):

        dialog = EntreeDialog()


        if dialog.exec():

            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT COUNT(*)

                FROM entrees_argent
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO entrees_argent

                (
                nom,
                montant,
                position
                )

                VALUES (?, ?, ?)
                """,

                (
                    dialog.nom.text(),

                    self.convertir(
                        dialog.montant.text()
                    ),

                    position
                )
            )


            conn.commit()

            conn.close()


            self.charger()



    # =========================
    # AJOUT SEPARATEUR
    # =========================

    def ouvrir_dialog_separateur(
        self
    ):

        dialog = SeparateurDialog()


        if dialog.exec():

            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT COUNT(*)

                FROM entrees_argent
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO entrees_argent

                (
                nom,
                montant,
                position,
                est_separateur
                )

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



    # =========================
    # CHARGEMENT
    # =========================

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
            montant,
            est_separateur

            FROM entrees_argent

            ORDER BY position
            """
        )


        resultats = cursor.fetchall()


        conn.close()


        self.table.blockSignals(True)

        self.table.clearSpans()


        self.table.setRowCount(
            0
        )


        total = 0


        for identifiant, nom, montant, est_separateur in resultats:


            row = self.table.rowCount()


            self.table.insertRow(
                row
            )


            if est_separateur:


                self.table.setSpan(
                    row,
                    0,
                    1,
                    2
                )


                item = QTableWidgetItem(
                    nom
                )


                item.setTextAlignment(
                    Qt.AlignCenter
                )


                item.setBackground(
                    QColor(
                        210,
                        210,
                        210
                    )
                )


                police = QFont()

                police.setBold(
                    True
                )

                item.setFont(
                    police
                )


                item.setFlags(
                    Qt.ItemIsEnabled
                )


                self.table.setItem(
                    row,
                    0,
                    item
                )


                self.creer_actions(
                    row,
                    identifiant
                )


                self.table.setRowHeight(
                    row,
                    22
                )


                continue


            montant = montant or 0


            total += montant


            item_nom = QTableWidgetItem(
                nom
            )

            item_nom.setFlags(
                Qt.ItemIsEnabled
            )


            item_montant = QTableWidgetItem(
                self.formater_montant(
                    montant
                )
            )

            item_montant.setToolTip(
                "Valeur modifiable directement"
            )


            self.table.setItem(
                row,
                0,
                item_nom
            )


            self.table.setItem(
                row,
                1,
                item_montant
            )


            self.creer_actions(
                row,
                identifiant
            )


        self.table.blockSignals(False)


        self.total.setText(
            "Total : "
            +
            self.formater_montant(
                total
            )
        )



    # =========================
    # CREATION DES ACTIONS
    # =========================

    def creer_actions(
        self,
        row,
        identifiant
    ):

        actions = QWidget()


        actions_layout = QHBoxLayout()


        actions_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )


        monter = QPushButton(
            "↑"
        )

        monter.setFixedWidth(
            30
        )


        descendre = QPushButton(
            "↓"
        )

        descendre.setFixedWidth(
            30
        )


        modifier = QPushButton(
            "Edit"
        )

        modifier.setFixedWidth(
            45
        )


        supprimer = QPushButton(
            "X"
        )

        supprimer.setFixedWidth(
            30
        )


        monter.clicked.connect(
            lambda checked=False:
            self.monter(
                identifiant
            )
        )


        descendre.clicked.connect(
            lambda checked=False:
            self.descendre(
                identifiant
            )
        )


        modifier.clicked.connect(
            lambda checked=False:
            self.modifier(
                identifiant
            )
        )


        supprimer.clicked.connect(
            lambda checked=False:
            self.supprimer(
                identifiant
            )
        )


        actions_layout.addWidget(
            monter
        )

        actions_layout.addWidget(
            descendre
        )

        actions_layout.addWidget(
            modifier
        )

        actions_layout.addWidget(
            supprimer
        )


        actions.setLayout(
            actions_layout
        )


        self.table.setCellWidget(
            row,
            2,
            actions
        )



    # =========================
    # MONTER
    # =========================

    def monter(
        self,
        identifiant
    ):

        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT position

            FROM entrees_argent

            WHERE id = ?
            """,
            (
                identifiant,
            )
        )


        actuel = cursor.fetchone()


        if actuel is None:

            conn.close()

            return


        position = actuel[0]


        if position <= 0:

            conn.close()

            return


        cursor.execute(
            """
            UPDATE entrees_argent

            SET position = position + 1

            WHERE position = ?
            """,
            (
                position - 1,
            )
        )


        cursor.execute(
            """
            UPDATE entrees_argent

            SET position = ?

            WHERE id = ?
            """,
            (
                position - 1,
                identifiant
            )
        )


        conn.commit()

        conn.close()


        self.charger()



    # =========================
    # DESCENDRE
    # =========================

    def descendre(
        self,
        identifiant
    ):

        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT position

            FROM entrees_argent

            WHERE id = ?
            """,
            (
                identifiant,
            )
        )


        actuel = cursor.fetchone()


        if actuel is None:

            conn.close()

            return


        position = actuel[0]


        cursor.execute(
            """
            SELECT COUNT(*)

            FROM entrees_argent
            """
        )


        total = cursor.fetchone()[0]


        if position >= total - 1:

            conn.close()

            return


        cursor.execute(
            """
            UPDATE entrees_argent

            SET position = position - 1

            WHERE position = ?
            """,
            (
                position + 1,
            )
        )


        cursor.execute(
            """
            UPDATE entrees_argent

            SET position = ?

            WHERE id = ?
            """,
            (
                position + 1,
                identifiant
            )
        )


        conn.commit()

        conn.close()


        self.charger()



    # =========================
    # MODIFIER
    # =========================

    def modifier(
        self,
        identifiant
    ):

        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT

            nom,
            montant,
            est_separateur

            FROM entrees_argent

            WHERE id = ?
            """,
            (
                identifiant,
            )
        )


        resultat = cursor.fetchone()


        conn.close()


        if resultat is None:

            return


        nom, montant, est_separateur = resultat


        if est_separateur:


            dialog = SeparateurDialog(
                nom
            )


            if dialog.exec():


                conn = get_connection()

                cursor = conn.cursor()


                cursor.execute(
                    """
                    UPDATE entrees_argent

                    SET nom = ?

                    WHERE id = ?
                    """,
                    (
                        dialog.nom.text(),
                        identifiant
                    )
                )


                conn.commit()

                conn.close()


                self.charger()


            return


        dialog = EntreeEditDialog(
            nom,
            montant
        )


        if dialog.exec():


            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                UPDATE entrees_argent

                SET

                nom = ?,

                montant = ?

                WHERE id = ?
                """,
                (
                    dialog.nom.text(),

                    self.convertir(
                        dialog.montant.text()
                    ),

                    identifiant
                )
            )


            conn.commit()

            conn.close()


            self.charger()



    # =========================
    # SUPPRIMER
    # =========================

    def supprimer(
        self,
        identifiant
    ):

        confirmation = QMessageBox.question(
            self,
            "Suppression",
            "Supprimer cette ligne ?"
        )


        if confirmation == QMessageBox.Yes:


            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                DELETE FROM entrees_argent

                WHERE id = ?
                """,
                (
                    identifiant,
                )
            )


            conn.commit()

            conn.close()


            self.reorganiser_positions()


            self.charger()



    # =========================
    # REORGANISER POSITIONS
    # =========================

    def reorganiser_positions(
        self
    ):

        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT id

            FROM entrees_argent

            ORDER BY position
            """
        )


        lignes = cursor.fetchall()


        for index, ligne in enumerate(lignes):

            cursor.execute(
                """
                UPDATE entrees_argent

                SET position = ?

                WHERE id = ?
                """,
                (
                    index,
                    ligne[0]
                )
            )


        conn.commit()

        conn.close()
