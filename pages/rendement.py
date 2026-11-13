from PySide6.QtWidgets import (
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

from pages.croissance_dialog import (
    RendementDialog,
    RendementEditDialog,
    CroissanceViewDialog
)

from pages.separateur_dialog import SeparateurDialog



def calculer_rendement(
    montant_initial,
    taux_annuel,
    mois,
    cotisation_mensuelle=0
):

    taux_mensuel = taux_annuel / 100 / 12

    solde = montant_initial

    interets_totaux = 0

    cotisations_totales = 0

    lignes = []


    for numero in range(1, int(mois) + 1):


        solde += cotisation_mensuelle

        cotisations_totales += cotisation_mensuelle


        interet = solde * taux_mensuel

        solde += interet

        interets_totaux += interet


        lignes.append(
            {
                "mois": numero,
                "cotisation": cotisation_mensuelle,
                "interet": interet,
                "solde": solde
            }
        )


    return {
        "montant_initial": montant_initial,
        "cotisations_totales": cotisations_totales,
        "interets_totaux": interets_totaux,
        "solde_final": solde,
        "lignes": lignes
    }



class RendementPage(QWidget):

    def __init__(self):

        super().__init__()


        layout = QVBoxLayout()


        titre = QLabel(
            "Calculateur de rendement"
        )

        titre.setStyleSheet(
            "font-size:28px;font-weight:bold;"
        )

        layout.addWidget(
            titre
        )


        self.table = QTableWidget()


        self.table.setColumnCount(
            10
        )


        self.table.setHorizontalHeaderLabels(
            [
                "Nom",
                "Montant initial",
                "% intérêt",
                "Mois",
                "Cotisation mensuelle",
                "Cotisations totales",
                "Intérêts gagnés",
                "Valeur finale",
                "Tableau",
                "Actions"
            ]
        )


        header = self.table.horizontalHeader()


        header.setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )


        for i in range(1, 10):

            header.setSectionResizeMode(
                i,
                QHeaderView.ResizeToContents
            )


        layout.addWidget(
            self.table
        )


        boutons_ajout = QHBoxLayout()


        bouton = QPushButton(
            "+ Ajouter un calcul"
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



    def ouvrir_dialog(
        self
    ):

        dialog = RendementDialog()


        if dialog.exec():


            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT COUNT(*)

                FROM rendements
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO rendements

                (
                nom,
                montant_initial,
                taux,
                mois,
                cotisation_mensuelle,
                position
                )

                VALUES (?, ?, ?, ?, ?, ?)
                """,

                (
                    dialog.nom.text(),

                    self.convertir(
                        dialog.montant_initial.text()
                    ),

                    self.convertir(
                        dialog.taux.text()
                    ),

                    self.convertir_entier(
                        dialog.mois.text()
                    ),

                    self.convertir(
                        dialog.cotisation_mensuelle.text()
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

                FROM rendements
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO rendements

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
            montant_initial,
            taux,
            mois,
            cotisation_mensuelle,
            est_separateur

            FROM rendements

            ORDER BY position, id
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
            montant_initial,
            taux,
            mois,
            cotisation,
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
                    9
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


            calcul = calculer_rendement(
                montant_initial or 0,
                taux or 0,
                mois or 0,
                cotisation or 0
            )


            valeurs = [

                nom,

                self.formater_montant(
                    montant_initial or 0
                ),

                f"{(taux or 0):.2f} %",

                str(mois or 0),

                self.formater_montant(
                    cotisation or 0
                ),

                self.formater_montant(
                    calcul["cotisations_totales"]
                ),

                self.formater_montant(
                    calcul["interets_totaux"]
                ),

                self.formater_montant(
                    calcul["solde_final"]
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


            self.table.setCellWidget(
                row,
                8,
                voir
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
            9,
            actions
        )



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
            taux,
            mois,
            cotisation_mensuelle,
            est_separateur

            FROM rendements

            WHERE id = ?
            """,
            (
                identifiant,
            )
        )


        resultat = cursor.fetchone()


        conn.close()


        if resultat is None or resultat[5]:

            return


        calcul = calculer_rendement(
            resultat[1] or 0,
            resultat[2] or 0,
            resultat[3] or 0,
            resultat[4] or 0
        )


        lignes = [

            [
                ligne["mois"],
                self.formater_montant(
                    ligne["cotisation"]
                ),
                self.formater_montant(
                    ligne["interet"]
                ),
                self.formater_montant(
                    ligne["solde"]
                )
            ]

            for ligne in calcul["lignes"]

        ]


        dialog = CroissanceViewDialog(
            {
                "titre": "Détail du rendement",

                "nom": f"Rendement - {resultat[0]}",

                "resume": [
                    f"Montant initial : {self.formater_montant(calcul['montant_initial'])}",
                    f"Cotisations totales : {self.formater_montant(calcul['cotisations_totales'])}",
                    f"Intérêts gagnés : {self.formater_montant(calcul['interets_totaux'])}",
                    f"Valeur finale : {self.formater_montant(calcul['solde_final'])}"
                ],

                "entetes": [
                    "Mois",
                    "Cotisation",
                    "Intérêt",
                    "Valeur totale"
                ],

                "lignes": lignes
            },
            self
        )


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

            FROM rendements

            WHERE id = ?
            """,
            (
                identifiant,
            )
        )


        actuel = cursor.fetchone()


        if actuel is None or actuel[0] <= 0:

            conn.close()

            return


        position = actuel[0]


        cursor.execute(
            """
            UPDATE rendements

            SET position = position + 1

            WHERE position = ?
            """,
            (
                position - 1,
            )
        )


        cursor.execute(
            """
            UPDATE rendements

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



    def descendre(
        self,
        identifiant
    ):

        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT position

            FROM rendements

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

            FROM rendements
            """
        )


        total = cursor.fetchone()[0]


        if position >= total - 1:

            conn.close()

            return


        cursor.execute(
            """
            UPDATE rendements

            SET position = position - 1

            WHERE position = ?
            """,
            (
                position + 1,
            )
        )


        cursor.execute(
            """
            UPDATE rendements

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
            montant_initial,
            taux,
            mois,
            cotisation_mensuelle,
            est_separateur

            FROM rendements

            WHERE id = ?
            """,
            (
                identifiant,
            )
        )


        rendement = cursor.fetchone()


        conn.close()


        if rendement is None:

            return


        if rendement[6]:


            dialog = SeparateurDialog(
                rendement[1]
            )


            if dialog.exec():


                conn = get_connection()

                cursor = conn.cursor()


                cursor.execute(
                    """
                    UPDATE rendements

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


        dialog = RendementEditDialog(
            rendement,
            self
        )


        if dialog.exec():


            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                UPDATE rendements

                SET

                nom = ?,

                montant_initial = ?,

                taux = ?,

                mois = ?,

                cotisation_mensuelle = ?

                WHERE id = ?
                """,

                (
                    dialog.nom.text(),

                    self.convertir(
                        dialog.montant_initial.text()
                    ),

                    self.convertir(
                        dialog.taux.text()
                    ),

                    self.convertir_entier(
                        dialog.mois.text()
                    ),

                    self.convertir(
                        dialog.cotisation_mensuelle.text()
                    ),

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
                DELETE FROM rendements

                WHERE id = ?
                """,
                (
                    identifiant,
                )
            )


            cursor.execute(
                """
                SELECT id

                FROM rendements

                ORDER BY position
                """
            )


            lignes = cursor.fetchall()


            for index, ligne in enumerate(lignes):

                cursor.execute(
                    """
                    UPDATE rendements

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


            self.charger()
