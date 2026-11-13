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

from pages.pret_dialog import (
    PretDialog,
    PretEditDialog
)

from pages.amortissement_view_dialog import AmortissementViewDialog
from pages.separateur_dialog import SeparateurDialog



def calculer_paiement(
    montant,
    taux_annuel,
    mois
):

    if mois <= 0 or montant <= 0:

        return 0


    taux_mensuel = taux_annuel / 100 / 12


    if taux_mensuel == 0:

        return montant / mois


    return (
        taux_mensuel * montant
    ) / (
        1 - (1 + taux_mensuel) ** (-mois)
    )



def construire_tableau(
    montant,
    taux_annuel,
    mois,
    paiement=0
):

    if paiement <= 0:

        paiement = calculer_paiement(
            montant,
            taux_annuel,
            mois
        )


    if montant <= 0 or paiement <= 0:

        return {
            "montant_finance": montant,
            "paiement_mensuel": paiement,
            "interets_totaux": 0,
            "total_paye": 0,
            "nombre_mois_reel": 0,
            "lignes": []
        }


    taux_mensuel = taux_annuel / 100 / 12

    solde = montant

    interets_totaux = 0

    total_paye = 0

    lignes = []

    numero = 0


    while solde > 0.009 and numero < 2000:


        numero += 1


        interet = solde * taux_mensuel

        capital = paiement - interet


        if capital <= 0:

            capital = 0

            paiement_reel = interet

        else:

            paiement_reel = paiement


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
                "mois": numero,
                "paiement": paiement_reel,
                "interet": interet,
                "capital": capital,
                "solde": solde
            }
        )


        if capital <= 0:

            break


    return {
        "montant_finance": montant,
        "paiement_mensuel": paiement,
        "interets_totaux": interets_totaux,
        "total_paye": total_paye,
        "nombre_mois_reel": len(lignes),
        "lignes": lignes
    }



class PretsPage(QWidget):

    def __init__(self):

        super().__init__()


        layout = QVBoxLayout()


        titre = QLabel(
            "Prêts"
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
                "Date début",
                "Mois",
                "Institution",
                "Nom",
                "Initial",
                "Montant avancé",
                "Capital",
                "Taux",
                "Paiement mensuel",
                "Montant final",
                "% Remboursé",
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
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.Stretch
        )


        for i in range(4, 12):

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
            "+ Ajouter un prêt"
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

        self.total_final = QLabel()

        self.total = QLabel()


        self.total_final.setStyleSheet(
            "font-size:16px;"
        )

        self.total.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )


        layout.addWidget(
            self.total_final
        )

        layout.addWidget(
            self.total
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

        dialog = PretDialog()


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

                FROM prets
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO prets

                (
                date_debut,
                date_fin,
                institution,
                nom,
                montant_initial,
                solde_actuel,
                taux,
                mois,
                paiement_mensuel,
                position
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,

                (
                    dialog.date_debut.date().toString(
                        "yyyy-MM-dd"
                    ),

                    date_fin,

                    dialog.institution.text(),

                    dialog.nom.text(),

                    self.convertir(
                        dialog.montant_initial.text()
                    ),

                    self.convertir(
                        dialog.solde_actuel.text()
                    ),

                    self.convertir(
                        dialog.taux.text()
                    ),

                    self.convertir_entier(
                        dialog.mois.text()
                    ),

                    self.convertir(
                        dialog.paiement_mensuel.text()
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

                FROM prets
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO prets

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
            date_debut,
            date_fin,
            institution,
            nom,
            montant_initial,
            solde_actuel,
            taux,
            paiement_mensuel,
            mois,
            est_separateur

            FROM prets

            ORDER BY position, id
            """
        )


        prets = cursor.fetchall()


        conn.close()


        self.table.clearSpans()


        self.table.setRowCount(
            0
        )


        total_restant = 0

        total_final = 0


        for pret in prets:


            row = self.table.rowCount()


            self.table.insertRow(
                row
            )


            (
                identifiant,
                date1,
                date2,
                institution,
                nom,
                initial,
                avance,
                taux,
                paiement,
                mois,
                est_separateur

            ) = pret


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


            initial = initial or 0

            avance = avance or 0

            taux = taux or 0

            paiement = paiement or 0

            mois = mois or 0


            restant = initial - avance


            if restant < 0:

                restant = 0


            total_restant += restant


            rembourse = 0


            if initial > 0:

                rembourse = avance / initial * 100


                if rembourse > 100:

                    rembourse = 100


            paiement_reference = paiement


            if paiement_reference <= 0:

                paiement_reference = calculer_paiement(
                    initial,
                    taux,
                    mois
                )


            montant_final = paiement_reference * mois


            total_final += montant_final


            valeurs = [

                date1 or "",

                str(mois),

                institution,

                nom,

                self.formater_montant(
                    initial
                ),

                self.formater_montant(
                    avance
                ),

                self.formater_montant(
                    restant
                ),

                f"{taux:.2f} %",

                self.formater_montant(
                    paiement_reference
                ),

                self.formater_montant(
                    montant_final
                ),

                f"{rembourse:.2f} %"

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


        self.total.setText(
            f"Total restant à payer : {self.formater_montant(total_restant)}"
        )


        self.total_final.setText(
            f"Montant final total : {self.formater_montant(total_final)}"
        )


        self.table.blockSignals(
            False
        )



    # =========================
    # MODIFICATION MONTANT AVANCE
    # =========================

    def valeur_modifiee(
        self,
        row,
        column
    ):

        if column != 5:

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

            FROM prets

            ORDER BY position, id
            """
        )


        lignes = cursor.fetchall()


        if row < len(lignes):


            cursor.execute(
                """
                UPDATE prets

                SET solde_actuel = ?

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


        if not est_separateur:


            voir = QPushButton(
                "Voir"
            )

            voir.setFixedWidth(
                50
            )

            voir.clicked.connect(
                lambda checked=False:
                self.voir(
                    identifiant
                )
            )


            actions_layout.addWidget(
                voir
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
            solde_actuel,
            taux,
            mois,
            paiement_mensuel,
            est_separateur

            FROM prets

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


        if resultat[6]:

            return


        initial = resultat[1] or 0

        avance = resultat[2] or 0


        restant = initial - avance


        if restant < 0:

            restant = 0


        paiement = resultat[5] or 0


        if paiement <= 0:

            paiement = calculer_paiement(
                initial,
                resultat[3] or 0,
                resultat[4] or 0
            )


        calcul = construire_tableau(
            restant,
            resultat[3] or 0,
            resultat[4] or 0,
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

            FROM prets

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
            UPDATE prets

            SET position = position + 1

            WHERE position = ?
            """,
            (
                position - 1,
            )
        )


        cursor.execute(
            """
            UPDATE prets

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

            FROM prets

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

            FROM prets
            """
        )


        nombre = cursor.fetchone()[0]


        if position >= nombre - 1:

            conn.close()

            return


        cursor.execute(
            """
            UPDATE prets

            SET position = position - 1

            WHERE position = ?
            """,
            (
                position + 1,
            )
        )


        cursor.execute(
            """
            UPDATE prets

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
            date_debut,
            date_fin,
            institution,
            nom,
            montant_initial,
            solde_actuel,
            taux,
            paiement_mensuel,
            mois,
            est_separateur

            FROM prets

            WHERE id = ?
            """,
            (
                identifiant,
            )
        )


        pret = cursor.fetchone()


        conn.close()


        if pret is None:

            return


        if pret[10]:


            dialog = SeparateurDialog(
                pret[4]
            )


            if dialog.exec():


                conn = get_connection()

                cursor = conn.cursor()


                cursor.execute(
                    """
                    UPDATE prets

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


        dialog = PretEditDialog(
            pret,
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
                UPDATE prets

                SET

                date_debut = ?,

                date_fin = ?,

                institution = ?,

                nom = ?,

                montant_initial = ?,

                solde_actuel = ?,

                taux = ?,

                mois = ?,

                paiement_mensuel = ?

                WHERE id = ?
                """,

                (
                    dialog.date_debut.date().toString(
                        "yyyy-MM-dd"
                    ),

                    date_fin,

                    dialog.institution.text(),

                    dialog.nom.text(),

                    self.convertir(
                        dialog.montant_initial.text()
                    ),

                    self.convertir(
                        dialog.solde_actuel.text()
                    ),

                    self.convertir(
                        dialog.taux.text()
                    ),

                    self.convertir_entier(
                        dialog.mois.text()
                    ),

                    self.convertir(
                        dialog.paiement_mensuel.text()
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
                DELETE FROM prets

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

            FROM prets

            ORDER BY position
            """
        )


        lignes = cursor.fetchall()


        for index, ligne in enumerate(lignes):

            cursor.execute(
                """
                UPDATE prets

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
