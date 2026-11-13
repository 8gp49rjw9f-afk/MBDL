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
    QAbstractItemView,
    QProgressDialog
)

import json
import time
import urllib.request
import urllib.parse
import urllib.error

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from database import get_connection

from pages.bourse_dialog import (
    BourseDialog,
    BourseEditDialog
)

from pages.separateur_dialog import SeparateurDialog
from pages.bourse_graphique_dialog import BourseGraphiqueDialog



class BoursePage(QWidget):

    def __init__(self):

        super().__init__()


        layout = QVBoxLayout()


        # =========================
        # TITRE
        # =========================

        titre = QLabel(
            "Bourse et Cryptos"
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
            13
        )


        self.table.setHorizontalHeaderLabels(
            [
                "Type",
                "Date d'achat",
                "Institution",
                "Nom",
                "Symbole",
                "Nb",
                "Prix achat",
                "Val. achat",
                "Prix actuel",
                "Val. actuelle",
                "% Profit",
                "Graph.",
                ""
            ]
        )


        header = self.table.horizontalHeader()

        # Type
        header.setSectionResizeMode(0, QHeaderView.Interactive)
        self.table.setColumnWidth(0, 70)

        # Date
        header.setSectionResizeMode(1, QHeaderView.Interactive)
        self.table.setColumnWidth(1, 80)

        # Institution
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        # Nom
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        # Symbole
        header.setSectionResizeMode(4, QHeaderView.Interactive)
        self.table.setColumnWidth(4, 80)

        # Nb
        header.setSectionResizeMode(5, QHeaderView.Interactive)
        self.table.setColumnWidth(5, 50)

        # Prix achat
        header.setSectionResizeMode(6, QHeaderView.Interactive)
        self.table.setColumnWidth(6, 90)

        # Val. achat
        header.setSectionResizeMode(7, QHeaderView.Interactive)
        self.table.setColumnWidth(7, 90)

        # Prix actuel
        header.setSectionResizeMode(8, QHeaderView.Interactive)
        self.table.setColumnWidth(8, 90)

        # Val. actuelle
        header.setSectionResizeMode(9, QHeaderView.Interactive)
        self.table.setColumnWidth(9, 100)

        # % Profit
        header.setSectionResizeMode(10, QHeaderView.Interactive)
        self.table.setColumnWidth(10, 70)

        # Graphique
        header.setSectionResizeMode(11, QHeaderView.Interactive)
        self.table.setColumnWidth(11, 50)

        # Actions
        header.setSectionResizeMode(12, QHeaderView.Interactive)
        self.table.setColumnWidth(12, 120)


        layout.addWidget(
            self.table
        )


        # =========================
        # BOUTONS AJOUT
        # =========================

        boutons_ajout = QHBoxLayout()


        bouton = QPushButton(
            "+ Ajouter Bourse ou Crypto"
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

        self.total_achat = QLabel()

        self.total_actuel = QLabel()


        self.total_achat.setStyleSheet(
            "font-size:16px;"
        )

        self.total_actuel.setStyleSheet(
            "font-size:20px;font-weight:bold;"
        )


        layout.addWidget(
            self.total_achat
        )

        layout.addWidget(
            self.total_actuel
        )


        # =========================
        # BOUTON MISE A JOUR
        # =========================

        bouton_maj = QPushButton("🌐 MISE À JOUR (Internet)")
        bouton_maj.setStyleSheet("font-size:16px;font-weight:bold;padding:10px;")
        bouton_maj.clicked.connect(self.mettre_a_jour_prix)
        layout.addWidget(bouton_maj)


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

        if column != 8:
            return

        item = self.table.item(
            row,
            column
        )

        if item is None:
            return

        nouveau_prix = self.convertir(
            item.text()
        )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id,
            symbole,
            nombre_actions

            FROM bourse

            ORDER BY position, id
            """
        )

        lignes = cursor.fetchall()

        if row < len(lignes):

            identifiant = lignes[row][0]

            nombre = lignes[row][1] or 0

            cursor.execute(
                """
                UPDATE bourse

                SET prix_actuel = ?,
                valeur_actuelle = ?

                WHERE id = ?
                """,
                (
                    nouveau_prix,
                    nombre * nouveau_prix,
                    identifiant
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
        valeur,
        decimales=2
    ):

        try:

            format_str = f"{{:,.{decimales}f}}"

            texte = (
                format_str.format(float(valeur))
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

        dialog = BourseDialog()


        if dialog.exec():


            nombre = self.convertir(
                dialog.nombre_actions.text()
            )

            prix_actuel = self.convertir(
                dialog.prix_actuel.text()
            )


            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT COUNT(*)

                FROM bourse
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO bourse

                (
                type_ligne,
                date_achat,
                institution,
                nom,
                symbole,
                nombre_actions,
                prix_achat,
                prix_actuel,
                valeur_actuelle,
                position
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,

                (
                    dialog.type_ligne.currentText(),

                    dialog.date_achat.date().toString(
                        "yyyy-MM-dd"
                    ),

                    dialog.institution.text(),

                    dialog.nom.text(),

                    dialog.symbole.text(),

                    nombre,

                    self.convertir(
                        dialog.prix_achat.text()
                    ),

                    prix_actuel,

                    nombre * prix_actuel,

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

                FROM bourse
                """
            )


            position = cursor.fetchone()[0]


            cursor.execute(
                """
                INSERT INTO bourse

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
            date_achat,
            institution,
            nom,
            symbole,
            nombre_actions,
            prix_achat,
            prix_actuel,
            type_ligne,
            est_separateur

            FROM bourse

            ORDER BY position, id
            """
        )


        actions = cursor.fetchall()


        conn.close()


        self.table.blockSignals(True)

        self.table.clearSpans()


        self.table.setRowCount(
            0
        )


        total_achat = 0

        total_actuel = 0


        for action in actions:


            row = self.table.rowCount()


            self.table.insertRow(
                row
            )


            (
                identifiant,
                date_achat,
                institution,
                nom,
                symbole,
                nombre,
                prix_achat,
                prix_actuel,
                type_ligne,
                est_separateur

            ) = action


            if est_separateur:


                self.table.setSpan(
                    row,
                    0,
                    1,
                    12
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


            nombre = nombre or 0

            prix_achat = prix_achat or 0

            prix_actuel = prix_actuel or 0


            valeur_achat = nombre * prix_achat

            valeur_actuelle = nombre * prix_actuel


            total_achat += valeur_achat

            total_actuel += valeur_actuelle


            profit = 0


            if valeur_achat > 0:

                profit = (
                    valeur_actuelle - valeur_achat
                ) / valeur_achat * 100


            valeurs = [

                type_ligne or "Bourse",

                date_achat or "",

                institution,

                nom,

                symbole or "",

                f"{nombre:,.5f}".replace(",", " ").replace(".", ",") if type_ligne == "Crypto" else f"{nombre:,.2f}".replace(",", " ").replace(".", ","),

                self.formater_montant(
                    prix_achat,
                    5 if type_ligne == "Crypto" else 2
                ),

                self.formater_montant(
                    valeur_achat,
                    5 if type_ligne == "Crypto" else 2
                ),

                self.formater_montant(
                    prix_actuel,
                    5 if type_ligne == "Crypto" else 2
                ),

                self.formater_montant(
                    valeur_actuelle,
                    5 if type_ligne == "Crypto" else 2
                ),

                f"{profit:.2f} %"

            ]


            for colonne, valeur in enumerate(valeurs):


                item = QTableWidgetItem(
                    valeur
                )


                if colonne != 8:

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


                if colonne == 9:


                    if valeur_actuelle > valeur_achat:

                        item.setBackground(
                            QColor(
                                210,
                                255,
                                210
                            )
                        )


                    elif valeur_actuelle < valeur_achat:

                        item.setBackground(
                            QColor(
                                255,
                                210,
                                210
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


        self.total_achat.setText(
            f"Valeur totale d'achat : {self.formater_montant(total_achat)}"
        )


        self.total_actuel.setText(
            f"Valeur totale actuelle : {self.formater_montant(total_actuel)}"
        )


        self.table.blockSignals(
            False
        )



    # =========================
    # MODIFICATION PRIX ACTUEL
    # =========================

    def valeur_modifiee(
        self,
        row,
        column
    ):

        if column != 7:

            return


        item = self.table.item(
            row,
            column
        )


        if item is None:

            return


        nouveau_prix = self.convertir(
            item.text()
        )


        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT id,
            nombre_actions

            FROM bourse

            ORDER BY position, id
            """
        )


        lignes = cursor.fetchall()


        if row < len(lignes):


            identifiant = lignes[row][0]

            nombre = lignes[row][1] or 0


            cursor.execute(
                """
                UPDATE bourse

                SET prix_actuel = ?,

                valeur_actuelle = ?

                WHERE id = ?
                """,
                (
                    nouveau_prix,
                    nombre * nouveau_prix,
                    identifiant
                )
            )


            conn.commit()


        conn.close()


        self.charger()



    # =========================
    # ACTIONS
    # =========================

    def ouvrir_graphique(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT type_ligne, symbole, nom

            FROM bourse

            WHERE id = ?
            """,
            (identifiant,)
        )

        resultat = cursor.fetchone()
        conn.close()

        if resultat is None:
            return

        dialog = BourseGraphiqueDialog(
            type_ligne=resultat[0] or "Bourse",
            symbole=resultat[1] or "",
            nom=resultat[2] or "",
            parent=self
        )

        dialog.exec()



    def creer_actions(
        self,
        row,
        identifiant
    ):

        # Bouton graphique
        bouton_graph = QPushButton("📊")
        bouton_graph.setFixedWidth(40)
        bouton_graph.clicked.connect(
            lambda checked=False:
            self.ouvrir_graphique(identifiant)
        )
        self.table.setCellWidget(row, 11, bouton_graph)

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
            12,
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

            FROM bourse

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
            UPDATE bourse

            SET position = position + 1

            WHERE position = ?
            """,
            (
                position - 1,
            )
        )


        cursor.execute(
            """
            UPDATE bourse

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

            FROM bourse

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

            FROM bourse
            """
        )


        nombre = cursor.fetchone()[0]


        if position >= nombre - 1:

            conn.close()

            return


        cursor.execute(
            """
            UPDATE bourse

            SET position = position - 1

            WHERE position = ?
            """,
            (
                position + 1,
            )
        )


        cursor.execute(
            """
            UPDATE bourse

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
            date_achat,
            institution,
            nom,
            symbole,
            nombre_actions,
            prix_achat,
            prix_actuel,
            type_ligne,
            est_separateur

            FROM bourse

            WHERE id = ?
            """,
            (
                identifiant,
            )
        )


        action = cursor.fetchone()


        conn.close()


        if action is None:

            return


        if action[9]:


            dialog = SeparateurDialog(
                action[3]
            )


            if dialog.exec():


                conn = get_connection()

                cursor = conn.cursor()


                cursor.execute(
                    """
                    UPDATE bourse

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


        dialog = BourseEditDialog(
            action,
            self
        )


        if dialog.exec():


            nombre = self.convertir(
                dialog.nombre_actions.text()
            )

            prix_actuel = self.convertir(
                dialog.prix_actuel.text()
            )


            conn = get_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                UPDATE bourse

                SET

                type_ligne = ?,

                date_achat = ?,

                institution = ?,

                nom = ?,

                symbole = ?,

                nombre_actions = ?,

                prix_achat = ?,

                prix_actuel = ?,

                valeur_actuelle = ?

                WHERE id = ?
                """,

                (
                    dialog.type_ligne.currentText(),

                    dialog.date_achat.date().toString(
                        "yyyy-MM-dd"
                    ),

                    dialog.institution.text(),

                    dialog.nom.text(),

                    dialog.symbole.text(),

                    nombre,

                    self.convertir(
                        dialog.prix_achat.text()
                    ),

                    prix_actuel,

                    nombre * prix_actuel,

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
                DELETE FROM bourse

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
    # MISE A JOUR DES PRIX
    # =========================

    def mettre_a_jour_prix(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, type_ligne, symbole, nom

            FROM bourse

            WHERE est_separateur = 0
            """
        )

        actions = cursor.fetchall()
        conn.close()

        if not actions:
            QMessageBox.information(self, "Mise à jour", "Aucune action à mettre à jour.")
            return

        # Barre de progression
        total = len(actions)
        progress = QProgressDialog("Mise à jour des prix en cours...", "Annuler", 0, total, self)
        progress.setWindowTitle("Mise à jour")
        progress.setWindowModality(__import__('PySide6.QtCore', fromlist=['Qt']).Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)

        from PySide6.QtWidgets import QApplication

        mis_a_jour = 0
        echecs = 0

        for i, (action_id, type_ligne, symbole, nom) in enumerate(actions):

            if progress.wasCanceled():
                break

            progress.setLabelText(f"Mise à jour: {nom or symbole} ({i+1}/{total})")
            progress.setValue(i)
            QApplication.processEvents()

            prix = None

            if type_ligne == "Crypto":
                prix = self.recuperer_prix_crypto(symbole, nom)
            else:
                prix = self.recuperer_prix_bourse(symbole, nom)

            if prix is not None and prix > 0:

                conn2 = get_connection()
                cursor2 = conn2.cursor()

                cursor2.execute(
                    "SELECT nombre_actions FROM bourse WHERE id = ?",
                    (action_id,)
                )

                nombre = cursor2.fetchone()[0] or 0

                cursor2.execute(
                    """
                    UPDATE bourse

                    SET prix_actuel = ?,
                    valeur_actuelle = ?

                    WHERE id = ?
                    """,
                    (prix, nombre * prix, action_id)
                )

                conn2.commit()
                conn2.close()

                mis_a_jour += 1

            else:

                echecs += 1

        progress.setValue(total)
        progress.close()

        self.charger()

        if mis_a_jour > 0:
            QMessageBox.information(
                self,
                "Mise à jour",
                f"{mis_a_jour} prix mis à jour avec succès."
                + (f"\n{echecs} échec(s)." if echecs > 0 else "")
            )
        else:
            QMessageBox.warning(
                self,
                "Mise à jour",
                "Aucun prix n'a pu être récupéré.\n\nVérifiez votre connexion Internet."
            )


    def recuperer_taux_usd_cad(self):

        try:

            url = "https://api.exchangerate-api.com/v4/latest/USD"

            req = urllib.request.Request(url, headers={"User-Agent": "MBDL/1.0"})

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))

            return data.get("rates", {}).get("CAD", 1.35)

        except:
            # Taux par defaut si Internet ne fonctionne pas
            return 1.35



    def recuperer_prix_crypto(self, symbole, nom):

        # Source 1: CoinCap (gratuit, pas de geo-blocage)
        prix = self.recuperer_prix_coincap(symbole, nom)

        if prix and prix > 0:
            return prix

        # Source 2: CoinGecko (backup)
        prix = self.recuperer_prix_coingecko(symbole, nom)

        if prix and prix > 0:
            return prix

        return None



    def recuperer_prix_coincap(self, symbole, nom):

        try:

            terme = (symbole or nom or "").lower().strip()

            if not terme:
                return None

            url = "https://api.coincap.io/v2/assets?limit=200"

            req = urllib.request.Request(url, headers={"User-Agent": "MBDL/1.0"})

            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))

            assets = data.get("data", [])

            if not assets:
                return None

            for asset in assets:

                asset_symbole = asset.get("symbol", "").lower()
                asset_nom = asset.get("name", "").lower()

                if terme == asset_symbole or terme == asset_nom:

                    prix_usd = float(asset.get("priceUsd", 0) or 0)

                    if prix_usd > 0:
                        taux = self.recuperer_taux_usd_cad()
                        return prix_usd * taux

            return None

        except:
            return None



    def recuperer_prix_coingecko(self, symbole, nom):

        try:

            terme = symbole or nom
            if not terme:
                return None

            url = f"https://api.coingecko.com/api/v3/search?query={urllib.parse.quote(terme)}"

            req = urllib.request.Request(url, headers={"User-Agent": "MBDL/1.0", "Accept": "application/json"})

            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))

            coins = data.get("coins", [])

            if not coins:
                return None

            coin_id = coins[0]["id"]

            url_prix = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=cad"

            req2 = urllib.request.Request(url_prix, headers={"User-Agent": "MBDL/1.0", "Accept": "application/json"})

            with urllib.request.urlopen(req2, timeout=15) as response2:
                data_prix = json.loads(response2.read().decode("utf-8"))

            return data_prix.get(coin_id, {}).get("cad")

        except:
            return None


    def recuperer_prix_bourse(self, symbole, nom):

        try:

            if symbole:
                terme = symbole
            else:
                terme = nom

            if not terme:
                return None

            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(terme)}?range=1d&interval=1d"

            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))

            meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})

            return meta.get("regularMarketPrice")

        except urllib.error.URLError:
            return None
        except:
            return None

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

            FROM bourse

            ORDER BY position
            """
        )


        lignes = cursor.fetchall()


        for index, ligne in enumerate(lignes):

            cursor.execute(
                """
                UPDATE bourse

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
