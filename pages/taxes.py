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
    QFrame
)

from PySide6.QtCore import Qt

from database import get_connection

from pages.taxe_dialog import TaxeDialog
from pages.taxe_edit_dialog import TaxeEditDialog


TAUX_TPS = 0.05
TAUX_TVQ = 0.09975



class TaxesPage(QWidget):

    def __init__(self):

        super().__init__()


        layout = QVBoxLayout()



        # =========================
        # TITRE
        # =========================

        titre = QLabel(
            "Taxes et impôts - Travail autonome"
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
            8
        )


        self.table.setHorizontalHeaderLabels(
            [
                "Année",
                "Contrat",
                "Montant facturé",
                "Montant total",
                "TPS",
                "TVQ",
                "Impôt à payer",
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
            QHeaderView.Stretch
        )


        for i in range(
            2,
            7
        ):

            header.setSectionResizeMode(
                i,
                QHeaderView.ResizeToContents
            )


        header.setSectionResizeMode(
            7,
            QHeaderView.ResizeToContents
        )


        self.table.setAlternatingRowColors(
            False
        )


        layout.addWidget(
            self.table
        )



        # =========================
        # AJOUT
        # =========================

        bouton = QPushButton(
            "+ Ajouter un contrat"
        )


        bouton.clicked.connect(
            self.ouvrir_dialog
        )


        layout.addWidget(
            bouton
        )



        # =========================
        # SEPARATEUR
        # =========================

        separateur = QFrame()

        separateur.setFrameShape(
            QFrame.HLine
        )

        layout.addWidget(
            separateur
        )



        # =========================
        # ACOMPTES PROVISIONNELS
        # =========================

        acomptes_titre = QLabel(
            "Acomptes provisionnels versés"
        )

        acomptes_titre.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )

        layout.addWidget(
            acomptes_titre
        )


        self.provincial_paye = self.creer_ligne(
            "Impôt provincial déjà payé"
        )


        self.federal_paye = self.creer_ligne(
            "Impôt fédéral déjà payé"
        )


        layout.addLayout(
            self.provincial_paye
        )

        layout.addLayout(
            self.federal_paye
        )



        # =========================
        # SEPARATEUR ACOMPTES
        # =========================

        sep1 = QFrame()
        sep1.setFrameShape(QFrame.HLine)
        layout.addWidget(sep1)


        acomptes_titre = QLabel("Acomptes provisionnels versés")
        acomptes_titre.setStyleSheet("font-size:18px;font-weight:bold;")
        layout.addWidget(acomptes_titre)

        self.total_acompte = QLabel()
        self.total_acompte.setStyleSheet("font-size:16px;font-weight:bold;")
        layout.addWidget(self.total_acompte)


        # =========================
        # SEPARATEUR TAXES
        # =========================

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        layout.addWidget(sep2)


        # =========================
        # RESULTATS FINAUX
        # =========================

        self.total_tps = QLabel()
        self.total_tvq = QLabel()
        self.total_impot = QLabel()

        gras = "font-size:18px;font-weight:bold;"

        self.total_tps.setStyleSheet(gras)
        self.total_tvq.setStyleSheet(gras)
        self.total_impot.setStyleSheet(gras)

        layout.addWidget(self.total_tps)
        layout.addWidget(self.total_tvq)
        layout.addWidget(self.total_impot)


        # =========================
        # SEPARATEUR FINAL
        # =========================

        sep3 = QFrame()
        sep3.setFrameShape(QFrame.HLine)
        layout.addWidget(sep3)


        self.setLayout(layout)
        self.charger()



    # =========================
    # LIGNE ACOMPTE
    # =========================

    def creer_ligne(
        self,
        texte
    ):

        ligne = QHBoxLayout()


        label = QLabel(
            texte
        )


        champ = QLineEdit()


        champ.setPlaceholderText(
            "0.00"
        )


        champ.textChanged.connect(
            self.sauvegarder_acomptes
        )


        ligne.addWidget(
            label
        )

        ligne.addWidget(
            champ
        )


        ligne.champ = champ


        return ligne



    # =========================
    # AJOUT CONTRAT
    # =========================

    def ouvrir_dialog(
        self
    ):

        dialog = TaxeDialog()


        if dialog.exec():


            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT COUNT(*)

                FROM travail_autonome

                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO travail_autonome

                (
                annee,
                contrat,
                montant_facture,
                sans_tps,
                sans_tvq,
                sans_impot,
                pourcentage_impot,
                position
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)

                """,

                (
                    self.convertir_entier(
                        dialog.annee.text()
                    ),

                    dialog.contrat.text(),

                    self.convertir(
                        dialog.montant_facture.text()
                    ),

                    1 if dialog.sans_tps.isChecked() else 0,

                    1 if dialog.sans_tvq.isChecked() else 0,

                    1 if dialog.sans_impot.isChecked() else 0,

                    self.convertir(
                        dialog.pourcentage_impot.text()
                    ),

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
            annee,
            contrat,
            montant_facture,
            sans_tps,
            sans_tvq,
            sans_impot,
            pourcentage_impot

            FROM travail_autonome

            ORDER BY position,id

            """
        )


        contrats = cursor.fetchall()


        conn.close()


        self.table.setRowCount(
            0
        )


        total_tps = 0

        total_tvq = 0

        total_impot = 0


        for contrat in contrats:


            row = self.table.rowCount()


            self.table.insertRow(
                row
            )


            (
                identifiant,
                annee,
                nom,
                facture,
                sans_tps,
                sans_tvq,
                sans_impot,
                pourcentage_impot

            ) = contrat


            facture = facture or 0

            pourcentage_impot = (
                pourcentage_impot
                if pourcentage_impot is not None
                else 33
            )


            if sans_tps:

                tps = 0

            else:

                tps = facture * TAUX_TPS


            if sans_tvq:

                tvq = 0

            else:

                tvq = facture * TAUX_TVQ


            if sans_impot:

                impot = 0

            else:

                impot = facture * pourcentage_impot / 100


            total_tps += tps

            total_tvq += tvq

            total_impot += impot


            montant_total = facture + tps + tvq


            valeurs = [

                str(
                    annee or ""
                ),

                nom,

                self.formater_montant(
                    facture
                ),

                self.formater_montant(
                    montant_total
                ),

                self.formater_montant(
                    tps
                ),

                self.formater_montant(
                    tvq
                ),

                self.formater_montant(
                    impot
                )

            ]


            for colonne, valeur in enumerate(
                valeurs
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



            # =====================
            # ACTIONS
            # =====================

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
                lambda checked=False,
                id=identifiant:
                self.monter(id)
            )


            descendre = QPushButton(
                "↓"
            )

            descendre.setFixedWidth(
                25
            )

            descendre.clicked.connect(
                lambda checked=False,
                id=identifiant:
                self.descendre(id)
            )


            modifier = QPushButton(
                "Edit"
            )

            modifier.setFixedWidth(
                45
            )

            modifier.clicked.connect(
                lambda checked=False,
                id=identifiant:
                self.modifier(id)
            )


            supprimer = QPushButton(
                "X"
            )

            supprimer.setFixedWidth(
                25
            )

            supprimer.clicked.connect(
                lambda checked=False,
                id=identifiant:
                self.supprimer(id)
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
                7,
                actions
            )


        self.total_tps_du = total_tps

        self.total_tvq_du = total_tvq

        self.total_impot_du = total_impot


        self.charger_acomptes()



    # =========================
    # CHARGEMENT ACOMPTES
    # =========================

    def charger_acomptes(
        self
    ):

        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT provincial_paye,
            federal_paye

            FROM acomptes

            WHERE id=1

            """
        )


        resultat = cursor.fetchone()


        conn.close()


        self.provincial_paye.champ.blockSignals(
            True
        )

        self.federal_paye.champ.blockSignals(
            True
        )


        if resultat:

            self.provincial_paye.champ.setText(
                f"{resultat[0]:.2f}"
            )

            self.federal_paye.champ.setText(
                f"{resultat[1]:.2f}"
            )


        self.provincial_paye.champ.blockSignals(
            False
        )

        self.federal_paye.champ.blockSignals(
            False
        )


        self.calculer_cumulatif()



    # =========================
    # SAUVEGARDE ACOMPTES
    # =========================

    def sauvegarder_acomptes(
        self
    ):

        conn = get_connection()

        cursor = conn.cursor()


        provincial = self.convertir(
            self.provincial_paye.champ.text()
        )


        federal = self.convertir(
            self.federal_paye.champ.text()
        )


        cursor.execute(
            """
            UPDATE acomptes

            SET provincial_paye=?,
            federal_paye=?

            WHERE id=1

            """,

            (
                provincial,
                federal
            )
        )


        conn.commit()

        conn.close()


        self.calculer_cumulatif()



    # =========================
    # CUMULATIF
    # =========================

    def calculer_cumulatif(
        self
    ):

        provincial = self.convertir(
            self.provincial_paye.champ.text()
        )


        federal = self.convertir(
            self.federal_paye.champ.text()
        )


        total_verse = provincial + federal


        impot_net = self.total_impot_du - total_verse


        self.total_tps.setText(
            f"TPS à payer : {self.formater_montant(self.total_tps_du)}"
        )


        self.total_tvq.setText(
            f"TVQ à payer : {self.formater_montant(self.total_tvq_du)}"
        )


        self.total_acompte.setText(
            f"Total : {self.formater_montant(total_verse)}"
        )


        self.total_tps.setText(
            f"TPS à payer : {self.formater_montant(self.total_tps_du)}"
        )


        self.total_tvq.setText(
            f"TVQ à payer : {self.formater_montant(self.total_tvq_du)}"
        )


        self.total_impot.setText(
            f"Impôts à payer : {self.formater_montant(impot_net)}"
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

            FROM travail_autonome

            WHERE id=?

            """,
            (
                identifiant,
            )
        )


        resultat = cursor.fetchone()


        if resultat is None:

            conn.close()

            return


        position = resultat[0]


        if position == 0:

            conn.close()

            return


        cursor.execute(
            """
            UPDATE travail_autonome

            SET position = position + 1

            WHERE position = ?

            """,
            (
                position - 1,
            )
        )


        cursor.execute(
            """
            UPDATE travail_autonome

            SET position = ?

            WHERE id=?

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

            FROM travail_autonome

            WHERE id=?

            """,
            (
                identifiant,
            )
        )


        resultat = cursor.fetchone()


        if resultat is None:

            conn.close()

            return


        position = resultat[0]


        cursor.execute(
            """
            SELECT COUNT(*)

            FROM travail_autonome

            """
        )


        nombre = cursor.fetchone()[0]


        if position >= nombre - 1:

            conn.close()

            return


        cursor.execute(
            """
            UPDATE travail_autonome

            SET position = position - 1

            WHERE position = ?

            """,
            (
                position + 1,
            )
        )


        cursor.execute(
            """
            UPDATE travail_autonome

            SET position = ?

            WHERE id=?

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
    # EDIT
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
            annee,
            contrat,
            montant_facture,
            sans_tps,
            sans_tvq,
            sans_impot,
            pourcentage_impot

            FROM travail_autonome

            WHERE id = ?

            """,
            (
                identifiant,
            )
        )


        contrat = cursor.fetchone()


        conn.close()


        if contrat is None:

            return


        dialog = TaxeEditDialog(
            contrat,
            self
        )


        if dialog.exec():


            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                UPDATE travail_autonome

                SET

                annee = ?,

                contrat = ?,

                montant_facture = ?,

                sans_tps = ?,

                sans_tvq = ?,

                sans_impot = ?,

                pourcentage_impot = ?

                WHERE id = ?

                """,

                (
                    self.convertir_entier(
                        dialog.annee.text()
                    ),

                    dialog.contrat.text(),

                    self.convertir(
                        dialog.montant_facture.text()
                    ),

                    1 if dialog.sans_tps.isChecked() else 0,

                    1 if dialog.sans_tvq.isChecked() else 0,

                    1 if dialog.sans_impot.isChecked() else 0,

                    self.convertir(
                        dialog.pourcentage_impot.text()
                    ),

                    identifiant
                )
            )


            conn.commit()

            conn.close()


            self.charger()



    # =========================
    # SUPPRESSION
    # =========================

    def supprimer(
        self,
        identifiant
    ):

        confirmation = QMessageBox.question(
            self,
            "Suppression",
            "Supprimer ce contrat ?"
        )


        if confirmation == QMessageBox.Yes:


            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                DELETE FROM travail_autonome

                WHERE id=?

                """,
                (
                    identifiant,
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
                .replace(
                    ",",
                    " "
                )
                .replace(
                    ".",
                    ","
                )
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
                .replace(
                    " ",
                    ""
                )
                .replace(
                    ",",
                    "."
                )
                .replace(
                    "$",
                    ""
                )
                .replace(
                    "%",
                    ""
                )
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
