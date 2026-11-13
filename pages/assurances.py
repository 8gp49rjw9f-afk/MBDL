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

from pages.assurance_dialog import (
    AssuranceDialog,
    AssuranceEditDialog
)

from pages.couvertures_view_dialog import CouverturesViewDialog
from pages.separateur_dialog import SeparateurDialog



class AssurancesPage(QWidget):

    def __init__(self):

        super().__init__()


        layout = QVBoxLayout()


        titre = QLabel(
            "Assurances"
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
            7
        )


        self.table.setHorizontalHeaderLabels(
            [
                "Compagnie",
                "Nom de la police",
                "Type d'assurance",
                "Prime mensuelle",
                "Couvertures",
                "Actions",
                ""
            ]
        )


        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )


        header = self.table.horizontalHeader()


        header.setSectionResizeMode(
            0,
            QHeaderView.Stretch
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

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            5,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            6,
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
            "+ Ajouter une assurance"
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

    def ouvrir_dialog(
        self
    ):

        dialog = AssuranceDialog()


        if dialog.exec():

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)

                FROM assurances
                """
            )

            position = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO assurances

                (
                compagnie,
                nom,
                type_assurance,
                prime,
                position
                )

                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    dialog.compagnie.text(),
                    dialog.nom.text(),
                    dialog.type_assurance.text(),
                    self.convertir(dialog.prime.text()),
                    position
                )
            )

            conn.commit()
            conn.close()

            self.charger()



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

                FROM assurances
                """
            )

            position = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO assurances

                (
                compagnie,
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



    def charger(
        self
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT

            id,
            compagnie,
            nom,
            type_assurance,
            prime,
            est_separateur

            FROM assurances

            ORDER BY position
            """
        )

        resultats = cursor.fetchall()

        conn.close()

        self.table.clearSpans()

        self.table.setRowCount(0)

        for identifiant, compagnie, nom, type_assurance, prime, est_separateur in resultats:

            row = self.table.rowCount()
            self.table.insertRow(row)

            if est_separateur:

                self.table.setSpan(row, 0, 1, 6)

                item = QTableWidgetItem(nom)
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QColor(210, 210, 210))
                police = QFont()
                police.setBold(True)
                item.setFont(police)
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(row, 0, item)

                self.creer_actions(row, identifiant, True)
                self.table.setRowHeight(row, 22)

                continue

            valeurs = [
                compagnie,
                nom,
                type_assurance,
                self.formater_montant(prime or 0)
            ]

            for colonne, valeur in enumerate(valeurs):

                item = QTableWidgetItem(valeur)
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(row, colonne, item)

            self.creer_actions(row, identifiant)



    def creer_actions(
        self,
        row,
        identifiant,
        est_separateur=False
    ):

        if not est_separateur:

            bouton_voir = QPushButton("Voir")
            bouton_voir.setFixedWidth(50)
            bouton_voir.clicked.connect(
                lambda checked=False:
                self.voir(identifiant)
            )

            self.table.setCellWidget(row, 4, bouton_voir)

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

        self.table.setCellWidget(row, 5, actions)



    def voir(
        self,
        identifiant
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT

            id,
            compagnie,
            nom,
            type_assurance,
            prime,
            est_separateur

            FROM assurances

            WHERE id = ?
            """,
            (identifiant,)
        )

        resultat = cursor.fetchone()
        conn.close()

        if resultat is None or resultat[5]:
            return

        dialog = CouverturesViewDialog(resultat, self)
        dialog.exec()



    def monter(
        self,
        identifiant
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT position

            FROM assurances

            WHERE id = ?
            """,
            (identifiant,)
        )

        actuel = cursor.fetchone()

        if actuel is None or actuel[0] <= 0:
            conn.close()
            return

        position = actuel[0]

        cursor.execute(
            """
            UPDATE assurances

            SET position = position + 1

            WHERE position = ?
            """,
            (position - 1,)
        )

        cursor.execute(
            """
            UPDATE assurances

            SET position = ?

            WHERE id = ?
            """,
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
            """
            SELECT position

            FROM assurances

            WHERE id = ?
            """,
            (identifiant,)
        )

        actuel = cursor.fetchone()

        if actuel is None:
            conn.close()
            return

        position = actuel[0]

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM assurances
            """
        )

        total = cursor.fetchone()[0]

        if position >= total - 1:
            conn.close()
            return

        cursor.execute(
            """
            UPDATE assurances

            SET position = position - 1

            WHERE position = ?
            """,
            (position + 1,)
        )

        cursor.execute(
            """
            UPDATE assurances

            SET position = ?

            WHERE id = ?
            """,
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
            compagnie,
            nom,
            type_assurance,
            prime,
            est_separateur

            FROM assurances

            WHERE id = ?
            """,
            (identifiant,)
        )

        assurance = cursor.fetchone()
        conn.close()

        if assurance is None:
            return

        if assurance[5]:

            dialog = SeparateurDialog(assurance[2])

            if dialog.exec():

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    UPDATE assurances

                    SET nom = ?

                    WHERE id = ?
                    """,
                    (dialog.nom.text(), identifiant)
                )

                conn.commit()
                conn.close()

                self.charger()

            return

        dialog = AssuranceEditDialog(assurance, self)

        if dialog.exec():

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE assurances

                SET

                compagnie = ?,

                nom = ?,

                type_assurance = ?,

                prime = ?

                WHERE id = ?
                """,
                (
                    dialog.compagnie.text(),
                    dialog.nom.text(),
                    dialog.type_assurance.text(),
                    self.convertir(dialog.prime.text()),
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
            "Supprimer cette ligne ?"
        )

        if confirmation == QMessageBox.Yes:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM couvertures

                WHERE assurance_id = ?
                """,
                (identifiant,)
            )

            cursor.execute(
                """
                DELETE FROM assurances

                WHERE id = ?
                """,
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
            """
            SELECT id

            FROM assurances

            ORDER BY position
            """
        )

        lignes = cursor.fetchall()

        for index, ligne in enumerate(lignes):

            cursor.execute(
                """
                UPDATE assurances

                SET position = ?

                WHERE id = ?
                """,
                (index, ligne[0])
            )

        conn.commit()
        conn.close()
