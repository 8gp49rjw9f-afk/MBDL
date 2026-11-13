from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QFrame,
    QAbstractItemView
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from database import get_connection

from pages.placement_dialog import (
    PlacementDialog,
    PlacementEditDialog
)

from pages.separateur_dialog import SeparateurDialog



class PlacementsPage(QWidget):

    def __init__(self):

        super().__init__()


        layout = QVBoxLayout()


        # =========================
        # TITRE
        # =========================

        titre = QLabel(
            "Placements"
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
            11
        )


        self.table.setHorizontalHeaderLabels(
            [
                "Type",
                "Date début",
                "Date fin",
                "Institution",
                "Nom",
                "Initial",
                "Valeur actuelle ✎",
                "Maximum",
                "% accompli",
                "% Profit",
                "Actions"
            ]
        )



        header = self.table.horizontalHeader()


        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
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
            QHeaderView.Stretch
        )


        for i in range(5, 11):

            header.setSectionResizeMode(
                i,
                QHeaderView.ResizeToContents
            )


        self.table.setAlternatingRowColors(
            False
        )


        layout.addWidget(
            self.table
        )


        # =========================
        # BOUTONS AJOUT
        # =========================

        boutons_ajout = QHBoxLayout()


        bouton = QPushButton(
            "+ Ajouter un placement"
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

        self.total_initial = QLabel()
        self.total_initial.setStyleSheet("font-size:16px;")

        self.total = QLabel()
        self.total.setStyleSheet("font-size:20px;font-weight:bold;")

        layout.addWidget(self.total_initial)
        layout.addWidget(self.total)


        self.setLayout(
            layout
        )


        self.table.blockSignals(True)
        self.table.cellChanged.connect(self.valeur_modifiee)
        self.table.blockSignals(False)
        self.charger()



    def valeur_modifiee(
        self,
        row,
        column
    ):

        if column != 6:
            return

        item = self.table.item(row, column)
        if item is None:
            return

        nouvelle_valeur = self.convertir(item.text())

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM placements ORDER BY position, id")
        lignes = cursor.fetchall()

        if row < len(lignes):
            cursor.execute(
                "UPDATE placements SET valeur_actuelle = ? WHERE id = ?",
                (nouvelle_valeur, lignes[row][0])
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
                .replace("%", "")
            )

        except:

            return 0



    # =========================
    # AJOUT
    # =========================

    def ouvrir_dialog(
        self
    ):

        dialog = PlacementDialog()


        if dialog.exec():


            conn = get_connection()

            cursor = conn.cursor()


            if dialog.aucune_date_fin.isChecked():

                date_fin = None

            else:

                date_fin = dialog.date_fin.date().toString(
                    "yyyy-MM-dd"
                )


            cursor.execute(
                """
                SELECT COUNT(*)

                FROM placements
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO placements

                (
                type_ligne,
                date_inscription,
                date_fin,
                institution,
                nom,
                montant_initial,
                valeur_actuelle,
                maximum,
                position
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,

                (
                    dialog.type_ligne.currentText(),

                    dialog.date_inscription.date().toString(
                        "yyyy-MM-dd"
                    ),

                    date_fin,

                    dialog.institution.text(),

                    dialog.nom.text(),

                    self.convertir(
                        dialog.montant_initial.text()
                    ),

                    self.convertir(
                        dialog.valeur_actuelle.text()
                    ),

                    dialog.obtenir_maximum(),

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

                FROM placements
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO placements

                (
                type_ligne,
                nom,
                position,
                est_separateur
                )

                VALUES ('', ?, ?, 1)
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

        self.table.blockSignals(
            True
        )


        annee = str(
            datetime.now().year
        )


        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT

            id,
            type_ligne,
            date_inscription,
            date_fin,
            institution,
            nom,
            montant_initial,
            valeur_actuelle,
            maximum,
            est_separateur

            FROM placements

            ORDER BY position, id
            """
        )


        placements = cursor.fetchall()


        conn.close()


        self.table.blockSignals(True)

        self.table.clearSpans()


        self.table.setRowCount(
            0
        )


        total = 0

        total_initial = 0

        self.total_reer_annee = 0

        self.total_celi_annee = 0

        self.total_annee = 0


        for placement in placements:


            row = self.table.rowCount()


            self.table.insertRow(
                row
            )


            (
                identifiant,
                type_ligne,
                date1,
                date2,
                institution,
                nom,
                initial,
                actuel,
                maximum,
                est_separateur

            ) = placement


            if est_separateur:


                self.table.setSpan(
                    row,
                    0,
                    1,
                    10
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


            initial = initial or 0

            actuel = actuel or 0

            maximum = maximum or 0

            type_ligne = type_ligne or "Autre"


            total += actuel

            total_initial += initial


            if str(date1 or "").startswith(annee):


                self.total_annee += initial


                if type_ligne == "REER":

                    self.total_reer_annee += initial


                elif type_ligne == "CELI":

                    self.total_celi_annee += initial


            profit = 0


            if initial > 0:

                profit = (
                    actuel - initial
                ) / initial * 100


            progression = 0


            if maximum > initial:

                progression = (
                    (actuel - initial) / (maximum - initial)
                ) * 100


                if progression < 0:

                    progression = 0


                if progression > 100:

                    progression = 100


            if date2:

                texte_date_fin = date2

            else:

                texte_date_fin = "aucune"


            if maximum > 0:

                texte_maximum = self.formater_montant(
                    maximum
                )

            else:

                texte_maximum = "aucun"


            valeurs = [

                type_ligne,

                date1 or "",

                texte_date_fin,

                institution,

                nom,

                self.formater_montant(
                    initial
                ),

                self.formater_montant(
                    actuel
                ),

                texte_maximum,

                f"{progression:.2f} %",

                f"{profit:.2f} %"

            ]


            for colonne, valeur in enumerate(valeurs):


                item = QTableWidgetItem(
                    valeur
                )


                if colonne != 6:

                    item.setFlags(
                        Qt.ItemIsEnabled
                    )

                else:

                    item.setFlags(
                        Qt.ItemIsEnabled | Qt.ItemIsEditable
                    )

                    item.setToolTip(
                        "Valeur modifiable directement"
                    )


                if colonne == 2 and not date2:

                    item.setBackground(
                        QColor(
                            235,
                            235,
                            235
                        )
                    )


                if colonne == 7 and maximum <= 0:

                    item.setBackground(
                        QColor(
                            235,
                            235,
                            235
                        )
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


        self.table.blockSignals(False)


        self.total_initial.setText(
            f"Total des montants initiaux : {self.formater_montant(total_initial)}"
        )


        self.total.setText(
            f"Total des montants actuels : {self.formater_montant(total)}"
        )


        self.table.blockSignals(
            False
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
            10,
            actions
        )




    def sauvegarder_plafonds(
        self
    ):

        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute(
            """
            UPDATE plafonds

            SET reer_possible = ?,
            celi_possible = ?

            WHERE id = 1
            """,

            (
                self.convertir(
                    self.reer_maximum.champ.text()
                ),

                self.convertir(
                    self.celi_maximum.champ.text()
                )
            )
        )


        conn.commit()

        conn.close()



    def afficher_totaux(
        self
    ):

        reer_maximum = self.convertir(
            self.reer_maximum.champ.text()
        )


        celi_maximum = self.convertir(
            self.celi_maximum.champ.text()
        )


        vert = "font-size:16px;font-weight:bold;color:#1b7f2e;"

        rouge = "font-size:16px;font-weight:bold;color:#c02020;"


        self.reer_annee.setText(
            f"REER Total durant l'année courante : {self.formater_montant(self.total_reer_annee)}"
        )


        if self.total_reer_annee > reer_maximum:

            self.reer_annee.setStyleSheet(
                rouge
            )

        else:

            self.reer_annee.setStyleSheet(
                vert
            )


        self.celi_annee.setText(
            f"CELI Total durant l'année courante : {self.formater_montant(self.total_celi_annee)}"
        )


        if self.total_celi_annee > celi_maximum:

            self.celi_annee.setStyleSheet(
                rouge
            )

        else:

            self.celi_annee.setStyleSheet(
                vert
            )


        self.placements_annee.setText(
            f"Placements totaux durant l'année courante : {self.formater_montant(self.total_annee)}"
        )



    # =========================
    # MODIFICATION VALEUR ACTUELLE
    # =========================

    def valeur_modifiee(
        self,
        row,
        column
    ):

        if column != 6:

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

            FROM placements

            ORDER BY position, id
            """
        )


        lignes = cursor.fetchall()


        if row < len(lignes):


            cursor.execute(
                """
                UPDATE placements

                SET valeur_actuelle = ?

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

            FROM placements

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
            UPDATE placements

            SET position = position + 1

            WHERE position = ?
            """,
            (
                position - 1,
            )
        )


        cursor.execute(
            """
            UPDATE placements

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

            FROM placements

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

            FROM placements
            """
        )


        nombre = cursor.fetchone()[0]


        if position >= nombre - 1:

            conn.close()

            return


        cursor.execute(
            """
            UPDATE placements

            SET position = position - 1

            WHERE position = ?
            """,
            (
                position + 1,
            )
        )


        cursor.execute(
            """
            UPDATE placements

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

            id,
            type_ligne,
            date_inscription,
            date_fin,
            institution,
            nom,
            montant_initial,
            valeur_actuelle,
            maximum,
            est_separateur

            FROM placements

            WHERE id = ?
            """,
            (
                identifiant,
            )
        )


        placement = cursor.fetchone()


        conn.close()


        if placement is None:

            return


        if placement[9]:


            dialog = SeparateurDialog(
                placement[5]
            )


            if dialog.exec():


                conn = get_connection()

                cursor = conn.cursor()


                cursor.execute(
                    """
                    UPDATE placements

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


        dialog = PlacementEditDialog(
            placement,
            self
        )


        if dialog.exec():


            conn = get_connection()

            cursor = conn.cursor()


            if dialog.aucune_date_fin.isChecked():

                date_fin = None

            else:

                date_fin = dialog.date_fin.date().toString(
                    "yyyy-MM-dd"
                )


            cursor.execute(
                """
                UPDATE placements

                SET

                type_ligne = ?,

                date_inscription = ?,

                date_fin = ?,

                institution = ?,

                nom = ?,

                montant_initial = ?,

                valeur_actuelle = ?,

                maximum = ?

                WHERE id = ?
                """,

                (
                    dialog.type_ligne.currentText(),

                    dialog.date_inscription.date().toString(
                        "yyyy-MM-dd"
                    ),

                    date_fin,

                    dialog.institution.text(),

                    dialog.nom.text(),

                    self.convertir(
                        dialog.montant_initial.text()
                    ),

                    self.convertir(
                        dialog.valeur_actuelle.text()
                    ),

                    dialog.obtenir_maximum(),

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
                DELETE FROM placements

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

            FROM placements

            ORDER BY position
            """
        )


        lignes = cursor.fetchall()


        for index, ligne in enumerate(lignes):

            cursor.execute(
                """
                UPDATE placements

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
