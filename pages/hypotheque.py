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

from pages.hypotheque_dialog import (
    HypothequeDialog,
    HypothequeEditDialog
)

from pages.amortissement_view_dialog import AmortissementViewDialog
from pages.separateur_dialog import SeparateurDialog
from pages.prets import (
    calculer_paiement,
    construire_tableau
)



class HypothequePage(QWidget):

    def __init__(self):

        super().__init__()


        layout = QVBoxLayout()


        titre = QLabel(
            "Hypothèques"
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
            12
        )


        self.table.setHorizontalHeaderLabels(
            [
                "Nom",
                "Institution",
                "Valeur propriété",
                "Prêt total",
                "Montant payé",
                "Restant à payer",
                "Équité",
                "% intérêt",
                "Mois",
                "Montant final total",
                "Tableau",
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
            QHeaderView.Stretch
        )


        for i in range(2, 12):

            header.setSectionResizeMode(
                i,
                QHeaderView.ResizeToContents
            )


        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
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
            "+ Ajouter une hypothèque"
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

        self.total_restant = QLabel()

        self.total_equite = QLabel()


        self.total_restant.setStyleSheet(
            "font-size:16px;"
        )

        self.total_equite.setStyleSheet(
            "font-size:20px;font-weight:bold;"
        )


        layout.addWidget(
            self.total_restant
        )

        layout.addWidget(
            self.total_equite
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
                .replace("%", "")
            )

        except:

            return 0



    def convertir_entier(
        self,
        valeur
    ):

        try:

            return int(
                str(valeur).strip()
            )

        except:

            return 0



    # =========================
    # AJOUT
    # =========================

    def ouvrir_dialog(
        self
    ):

        dialog = HypothequeDialog()


        if dialog.exec():


            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT COUNT(*)

                FROM hypotheques
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO hypotheques

                (
                nom,
                institution,
                valeur_propriete,
                montant_initial,
                montant_paye,
                taux,
                mois,
                position
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,

                (
                    dialog.nom.text(),

                    dialog.institution.text(),

                    self.convertir(
                        dialog.valeur_propriete.text()
                    ),

                    self.convertir(
                        dialog.montant_initial.text()
                    ),

                    self.convertir(
                        dialog.montant_paye.text()
                    ),

                    self.convertir(
                        dialog.taux.text()
                    ),

                    self.convertir_entier(
                        dialog.mois.text()
                    ),

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

                FROM hypotheques
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO hypotheques

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



    # =========================
    # CHARGEMENT
    # =========================

    def charger(
        self
    ):

        self.table.blockSignals(
            True
        )


        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT

            id,
            nom,
            institution,
            valeur_propriete,
            montant_initial,
            montant_paye,
            taux,
            mois,
            est_separateur

            FROM hypotheques

            ORDER BY position, id
            """
        )


        resultats = cursor.fetchall()


        conn.close()


        self.table.clearSpans()


        self.table.setRowCount(
            0
        )


        total_restant = 0

        total_equite = 0


        for (
            identifiant,
            nom,
            institution,
            valeur_propriete,
            montant_initial,
            montant_paye,
            taux,
            mois,
            est_separateur
        ) in resultats:


            row = self.table.rowCount()


            self.table.insertRow(
                row
            )


            if est_separateur:


                self.table.setSpan(
                    row,
                    0,
                    1,
                    11
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
                    identifiant,
                    True
                )


                self.table.setRowHeight(
                    row,
                    22
                )


                continue


            valeur_propriete = valeur_propriete or 0

            montant_initial = montant_initial or 0

            montant_paye = montant_paye or 0

            taux = taux or 0

            mois = mois or 0


            restant = montant_initial - montant_paye


            if restant < 0:

                restant = 0


            equite = valeur_propriete - restant


            paiement = calculer_paiement(
                montant_initial,
                taux,
                mois
            )


            calcul = construire_tableau(
                restant,
                taux,
                mois,
                paiement
            )


            montant_final = montant_paye + calcul["total_paye"]


            total_restant += restant

            total_equite += equite


            valeurs = [

                nom,

                institution,

                self.formater_montant(
                    valeur_propriete
                ),

                self.formater_montant(
                    montant_initial
                ),

                self.formater_montant(
                    montant_paye
                ),

                self.formater_montant(
                    restant
                ),

                self.formater_montant(
                    equite
                ),

                f"{taux:.2f} %",

                str(mois),

                self.formater_montant(
                    montant_final
                )

            ]


            for colonne, valeur in enumerate(valeurs):


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
                identifiant,
                False
            )


        self.total_restant.setText(
            f"Total restant à payer : {self.formater_montant(total_restant)}"
        )


        self.total_equite.setText(
            f"Équité totale : {self.formater_montant(total_equite)}"
        )


        self.table.blockSignals(
            False
        )



    # =========================
    # MODIFICATION MONTANT PAYE
    # =========================

    def valeur_modifiee(
        self,
        row,
        column
    ):

        if column != 4:

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

            FROM hypotheques

            ORDER BY position, id
            """
        )


        lignes = cursor.fetchall()


        if row < len(lignes):


            cursor.execute(
                """
                UPDATE hypotheques

                SET montant_paye = ?

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
    # ACTIONS
    # =========================

    def creer_actions(
        self,
        row,
        identifiant,
        est_separateur=False
    ):

        if not est_separateur:


            bouton_voir = QPushButton(
                "Voir"
            )

            bouton_voir.setFixedWidth(
                50
            )

            bouton_voir.clicked.connect(
                lambda checked=False:
                self.voir(
                    identifiant
                )
            )


            self.table.setCellWidget(
                row,
                10,
                bouton_voir
            )


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
            11,
            actions
        )



    # =========================
    # VOIR
    # =========================

    def voir(
        self,
        identifiant
    ):

        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT

            nom,
            montant_initial,
            montant_paye,
            taux,
            mois,
            est_separateur

            FROM hypotheques

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


        if resultat[5]:

            return


        montant_initial = resultat[1] or 0

        montant_paye = resultat[2] or 0

        taux = resultat[3] or 0

        mois = resultat[4] or 0


        restant = montant_initial - montant_paye


        if restant < 0:

            restant = 0


        paiement = calculer_paiement(
            montant_initial,
            taux,
            mois
        )


        calcul = construire_tableau(
            restant,
            taux,
            mois,
            paiement
        )


        calcul["nom"] = resultat[0]


        dialog = AmortissementViewDialog(
            calcul,
            self
        )


        dialog.exec()



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

            FROM hypotheques

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
            UPDATE hypotheques

            SET position = position + 1

            WHERE position = ?
            """,
            (
                position - 1,
            )
        )


        cursor.execute(
            """
            UPDATE hypotheques

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

            FROM hypotheques

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

            FROM hypotheques
            """
        )


        total = cursor.fetchone()[0]


        if position >= total - 1:

            conn.close()

            return


        cursor.execute(
            """
            UPDATE hypotheques

            SET position = position - 1

            WHERE position = ?
            """,
            (
                position + 1,
            )
        )


        cursor.execute(
            """
            UPDATE hypotheques

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
            nom,
            institution,
            valeur_propriete,
            montant_initial,
            montant_paye,
            taux,
            mois,
            est_separateur

            FROM hypotheques

            WHERE id = ?
            """,
            (
                identifiant,
            )
        )


        hypotheque = cursor.fetchone()


        conn.close()


        if hypotheque is None:

            return


        if hypotheque[8]:


            dialog = SeparateurDialog(
                hypotheque[1]
            )


            if dialog.exec():


                conn = get_connection()

                cursor = conn.cursor()


                cursor.execute(
                    """
                    UPDATE hypotheques

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


        dialog = HypothequeEditDialog(
            hypotheque,
            self
        )


        if dialog.exec():


            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                UPDATE hypotheques

                SET

                nom = ?,

                institution = ?,

                valeur_propriete = ?,

                montant_initial = ?,

                montant_paye = ?,

                taux = ?,

                mois = ?

                WHERE id = ?
                """,

                (
                    dialog.nom.text(),

                    dialog.institution.text(),

                    self.convertir(
                        dialog.valeur_propriete.text()
                    ),

                    self.convertir(
                        dialog.montant_initial.text()
                    ),

                    self.convertir(
                        dialog.montant_paye.text()
                    ),

                    self.convertir(
                        dialog.taux.text()
                    ),

                    self.convertir_entier(
                        dialog.mois.text()
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
                DELETE FROM hypotheques

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

            FROM hypotheques

            ORDER BY position
            """
        )


        lignes = cursor.fetchall()


        for index, ligne in enumerate(lignes):

            cursor.execute(
                """
                UPDATE hypotheques

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
