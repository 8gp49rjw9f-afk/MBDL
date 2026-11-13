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

from pages.amortissement_dialog import (
    AmortissementDialog,
    AmortissementEditDialog
)

from pages.amortissement_view_dialog import AmortissementViewDialog
from pages.separateur_dialog import SeparateurDialog



class AmortissementPage(QWidget):

    def __init__(self):

        super().__init__()


        layout = QVBoxLayout()


        # =========================
        # TITRE
        # =========================

        titre = QLabel(
            "Tableau d'amortissement"
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
                "Nom",
                "Montant initial",
                "Mise de fond",
                "Montant financé",
                "% intérêt",
                "Mois",
                "Paiement mensuel",
                "Paiement additionnel mensuel",
                "Montant final total",
                "Voir",
                "Actions"
            ]
        )


        header = self.table.horizontalHeader()


        header.setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )


        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )


        for i in range(1, 11):

            header.setSectionResizeMode(
                i,
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
            "+ Ajouter un tableau"
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
    # CALCUL
    # =========================

    def calculer_tableau(
        self,
        montant_initial,
        mise_fond,
        taux_annuel,
        mois,
        paiement_additionnel=0
    ):

        montant_finance = montant_initial - mise_fond


        if montant_finance < 0:

            montant_finance = 0


        if mois <= 0 or montant_finance <= 0:

            return {
                "montant_finance": montant_finance,
                "paiement_mensuel": 0,
                "interets_totaux": 0,
                "total_paye": 0,
                "nombre_mois_reel": 0,
                "lignes": []
            }


        taux_mensuel = taux_annuel / 100 / 12


        if taux_mensuel == 0:

            paiement_base = montant_finance / mois

        else:

            paiement_base = (
                taux_mensuel * montant_finance
            ) / (
                1 - (1 + taux_mensuel) ** (-mois)
            )


        paiement_mensuel = paiement_base + paiement_additionnel


        solde = montant_finance

        interets_totaux = 0

        total_paye = 0

        lignes = []

        numero_mois = 0


        while solde > 0.009 and numero_mois < 2000:


            numero_mois += 1


            interet = solde * taux_mensuel

            capital = paiement_mensuel - interet


            if capital <= 0:

                capital = 0

                paiement_reel = interet

            else:

                paiement_reel = paiement_mensuel


            if capital > solde:

                capital = solde

                paiement_reel = interet + capital


            solde -= capital


            if solde < 0:

                solde = 0


            interets_totaux += interet

            total_paye += paiement_reel


            lignes.append(
                {
                    "mois": numero_mois,
                    "paiement": paiement_reel,
                    "interet": interet,
                    "capital": capital,
                    "solde": solde
                }
            )


            if capital <= 0:

                break


        return {
            "montant_finance": montant_finance,
            "paiement_mensuel": paiement_mensuel,
            "interets_totaux": interets_totaux,
            "total_paye": total_paye,
            "nombre_mois_reel": len(lignes),
            "lignes": lignes
        }



    # =========================
    # AJOUT
    # =========================

    def ouvrir_dialog(
        self
    ):

        dialog = AmortissementDialog()


        if dialog.exec():


            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT COUNT(*)

                FROM amortissements
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO amortissements

                (
                nom,
                date_depart,
                montant_initial,
                mise_fond,
                taux,
                mois,
                paiement_additionnel,
                position
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,

                (
                    dialog.nom.text(),

                    dialog.date_depart.date().toString(
                        "yyyy-MM-dd"
                    ),

                    self.convertir(
                        dialog.montant_initial.text()
                    ),

                    self.convertir(
                        dialog.mise_fond.text()
                    ),

                    self.convertir(
                        dialog.taux.text()
                    ),

                    self.convertir_entier(
                        dialog.mois.text()
                    ),

                    self.convertir(
                        dialog.paiement_additionnel.text()
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

                FROM amortissements
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO amortissements

                (
                nom,
                date_depart,
                position,
                est_separateur
                )

                VALUES (?, '', ?, 1)
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
            date_depart,
            montant_initial,
            mise_fond,
            taux,
            mois,
            paiement_additionnel,
            est_separateur

            FROM amortissements

            ORDER BY position
            """
        )


        resultats = cursor.fetchall()


        conn.close()


        self.table.clearSpans()


        self.table.setRowCount(
            0
        )


        for (
            identifiant,
            nom,
            date_depart,
            montant_initial,
            mise_fond,
            taux,
            mois,
            paiement_additionnel,
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
                    identifiant,
                    est_separateur
                )


                self.table.setRowHeight(
                    row,
                    22
                )


                continue


            calcul = self.calculer_tableau(
                montant_initial or 0,
                mise_fond or 0,
                taux or 0,
                mois or 0,
                paiement_additionnel or 0
            )


            valeurs = [

                nom,

                self.formater_montant(
                    montant_initial or 0
                ),

                self.formater_montant(
                    mise_fond or 0
                ),

                self.formater_montant(
                    calcul["montant_finance"]
                ),

                f"{(taux or 0):.2f} %",

                str(mois or 0),

                self.formater_montant(
                    calcul["paiement_mensuel"]
                ),

                self.formater_montant(
                    paiement_additionnel or 0
                ),

                self.formater_montant(
                    calcul["total_paye"]
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
                est_separateur
            )



    # =========================
    # ACTIONS
    # =========================

    def creer_actions(
        self,
        row,
        identifiant,
        est_separateur=0
    ):


        # ---- Colonne VOIR ----

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
                9,
                bouton_voir
            )


        # ---- Colonne ACTIONS ----

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

            id,
            nom,
            date_depart,
            montant_initial,
            mise_fond,
            taux,
            mois,
            paiement_additionnel,
            est_separateur

            FROM amortissements

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


        if resultat[8]:

            return


        calcul = self.calculer_tableau(
            resultat[3] or 0,
            resultat[4] or 0,
            resultat[5] or 0,
            resultat[6] or 0,
            resultat[7] or 0
        )


        calcul["nom"] = resultat[1]


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

            FROM amortissements

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
            UPDATE amortissements

            SET position = position + 1

            WHERE position = ?
            """,
            (
                position - 1,
            )
        )


        cursor.execute(
            """
            UPDATE amortissements

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

            FROM amortissements

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

            FROM amortissements
            """
        )


        total = cursor.fetchone()[0]


        if position >= total - 1:

            conn.close()

            return


        cursor.execute(
            """
            UPDATE amortissements

            SET position = position - 1

            WHERE position = ?
            """,
            (
                position + 1,
            )
        )


        cursor.execute(
            """
            UPDATE amortissements

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
            date_depart,
            montant_initial,
            mise_fond,
            taux,
            mois,
            paiement_additionnel,
            est_separateur

            FROM amortissements

            WHERE id = ?
            """,
            (
                identifiant,
            )
        )


        tableau = cursor.fetchone()


        conn.close()


        if tableau is None:

            return


        if tableau[8]:


            dialog = SeparateurDialog(
                tableau[1]
            )


            if dialog.exec():


                conn = get_connection()

                cursor = conn.cursor()


                cursor.execute(
                    """
                    UPDATE amortissements

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


        dialog = AmortissementEditDialog(
            tableau,
            self
        )


        if dialog.exec():


            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                UPDATE amortissements

                SET

                nom = ?,

                date_depart = ?,

                montant_initial = ?,

                mise_fond = ?,

                taux = ?,

                mois = ?,

                paiement_additionnel = ?

                WHERE id = ?
                """,

                (
                    dialog.nom.text(),

                    dialog.date_depart.date().toString(
                        "yyyy-MM-dd"
                    ),

                    self.convertir(
                        dialog.montant_initial.text()
                    ),

                    self.convertir(
                        dialog.mise_fond.text()
                    ),

                    self.convertir(
                        dialog.taux.text()
                    ),

                    self.convertir_entier(
                        dialog.mois.text()
                    ),

                    self.convertir(
                        dialog.paiement_additionnel.text()
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
                DELETE FROM amortissements

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

            FROM amortissements

            ORDER BY position
            """
        )


        lignes = cursor.fetchall()


        for index, ligne in enumerate(lignes):

            cursor.execute(
                """
                UPDATE amortissements

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
