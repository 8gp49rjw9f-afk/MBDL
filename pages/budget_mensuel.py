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

from pages.budget_mensuel_dialog import (
    BudgetMensuelDialog,
    BudgetMensuelEditDialog
)

from pages.separateur_dialog import SeparateurDialog



class BudgetMensuelPage(QWidget):

    def __init__(self):

        super().__init__()


        layout = QVBoxLayout()


        # =========================
        # TITRE
        # =========================

        titre = QLabel(
            "Budget mensuel"
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
            4
        )


        self.table.setHorizontalHeaderLabels(
            [
                "Type",
                "Nom",
                "Montant",
                "Actions"
            ]
        )


        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )


        header = self.table.horizontalHeader()


        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
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
            "+ Ajouter au budget"
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
        # TOTAUX
        # =========================

        self.total_entrees = QLabel(
            "Total entrées : 0,00 $"
        )

        self.total_depenses = QLabel(
            "Total dépenses : 0,00 $"
        )

        self.solde = QLabel(
            "Solde mensuel : 0,00 $"
        )


        self.total_entrees.setStyleSheet(
            "font-size:16px;"
        )

        self.total_depenses.setStyleSheet(
            "font-size:16px;"
        )

        self.solde.setStyleSheet(
            "font-size:20px;font-weight:bold;"
        )


        layout.addWidget(
            self.total_entrees
        )

        layout.addWidget(
            self.total_depenses
        )

        layout.addWidget(
            self.solde
        )


        self.setLayout(
            layout
        )


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

        dialog = BudgetMensuelDialog()


        if dialog.exec():


            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT COUNT(*)

                FROM budget_mensuel
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO budget_mensuel

                (
                type_ligne,
                nom,
                montant,
                position
                )

                VALUES (?, ?, ?, ?)
                """,

                (
                    dialog.type_ligne.currentText(),

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

                FROM budget_mensuel
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO budget_mensuel

                (
                type_ligne,
                nom,
                montant,
                position,
                est_separateur
                )

                VALUES ('', ?, 0, ?, 1)
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
            type_ligne,
            nom,
            montant,
            est_separateur

            FROM budget_mensuel

            ORDER BY position
            """
        )


        resultats = cursor.fetchall()


        conn.close()


        self.table.setRowCount(
            0
        )


        total_entrees = 0

        total_depenses = 0


        for identifiant, type_ligne, nom, montant, est_separateur in resultats:


            row = self.table.rowCount()


            self.table.insertRow(
                row
            )


            if est_separateur:


                self.table.setSpan(
                    row,
                    0,
                    1,
                    3
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


            if type_ligne == "Entrée":

                total_entrees += montant

            elif type_ligne == "Dépense":

                total_depenses += montant


            for colonne, valeur in enumerate(
                [
                    type_ligne,
                    nom,
                    self.formater_montant(
                        montant
                    )
                ]
            ):

                item = QTableWidgetItem(
                    valeur
                )

                item.setFlags(
                    Qt.ItemIsEnabled
                )

                self.table.setItem(
                    row,
                    colonne,
                    item
                )


            self.creer_actions(
                row,
                identifiant
            )


        solde = total_entrees - total_depenses


        self.total_entrees.setText(
            f"Total entrées : {self.formater_montant(total_entrees)}"
        )


        self.total_depenses.setText(
            f"Total dépenses : {self.formater_montant(total_depenses)}"
        )


        self.solde.setText(
            f"Solde mensuel : {self.formater_montant(solde)}"
        )



    # =========================
    # ACTIONS
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
            25
        )

        monter.clicked.connect(
            lambda checked=False:
            self.monter(
                identifiant
            )
        )


        descendre = QPushButton(
            "↓"
        )

        descendre.setFixedWidth(
            25
        )

        descendre.clicked.connect(
            lambda checked=False:
            self.descendre(
                identifiant
            )
        )


        modifier = QPushButton(
            "Edit"
        )

        modifier.setFixedWidth(
            45
        )

        modifier.clicked.connect(
            lambda checked=False:
            self.modifier(
                identifiant
            )
        )


        supprimer = QPushButton(
            "X"
        )

        supprimer.setFixedWidth(
            25
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
            3,
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

            FROM budget_mensuel

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
            UPDATE budget_mensuel

            SET position = position + 1

            WHERE position = ?
            """,
            (
                position - 1,
            )
        )


        cursor.execute(
            """
            UPDATE budget_mensuel

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

            FROM budget_mensuel

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

            FROM budget_mensuel
            """
        )


        total = cursor.fetchone()[0]


        if position >= total - 1:

            conn.close()

            return


        cursor.execute(
            """
            UPDATE budget_mensuel

            SET position = position - 1

            WHERE position = ?
            """,
            (
                position + 1,
            )
        )


        cursor.execute(
            """
            UPDATE budget_mensuel

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

            type_ligne,
            nom,
            montant,
            est_separateur

            FROM budget_mensuel

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


        type_ligne, nom, montant, est_separateur = resultat


        if est_separateur:


            dialog = SeparateurDialog(
                nom
            )


            if dialog.exec():


                conn = get_connection()

                cursor = conn.cursor()


                cursor.execute(
                    """
                    UPDATE budget_mensuel

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


        dialog = BudgetMensuelEditDialog(
            type_ligne,
            nom,
            montant,
            self
        )


        if dialog.exec():


            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                UPDATE budget_mensuel

                SET

                type_ligne = ?,

                nom = ?,

                montant = ?

                WHERE id = ?
                """,
                (
                    dialog.type_ligne.currentText(),

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
                DELETE FROM budget_mensuel

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

            FROM budget_mensuel

            ORDER BY position
            """
        )


        lignes = cursor.fetchall()


        for index, ligne in enumerate(lignes):

            cursor.execute(
                """
                UPDATE budget_mensuel

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
