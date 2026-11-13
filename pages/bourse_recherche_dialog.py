import json
import urllib.request
import urllib.parse
import urllib.error

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QAbstractItemView
)

from PySide6.QtCore import Qt

from pages.bourse_graphique_dialog import BourseGraphiqueDialog


class BourseRechercheDialog(QDialog):

    def __init__(self, type_ligne="Bourse", nom_recherche="", parent=None):

        super().__init__(parent)

        self.prix_selectionne = None
        self.symbole_selectionne = None
        self.nom_selectionne = None

        self.setWindowTitle("Recherche de prix")
        self.resize(800, 550)

        layout = QVBoxLayout()

        titre = QLabel("Recherche de prix en ligne")
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        layout.addWidget(QLabel("Type"))
        self.type_ligne = QComboBox()
        self.type_ligne.addItem("Bourse")
        self.type_ligne.addItem("Crypto")
        self.type_ligne.setCurrentText(type_ligne or "Bourse")
        layout.addWidget(self.type_ligne)

        layout.addWidget(QLabel("Nom ou symbole"))
        rech_layout = QHBoxLayout()
        self.recherche = QLineEdit()
        self.recherche.setText(nom_recherche or "")
        self.recherche.setPlaceholderText("Ex: AAPL, BTC, Bitcoin, Tesla...")
        rech_layout.addWidget(self.recherche)

        bouton_rechercher = QPushButton("Rechercher")
        bouton_rechercher.clicked.connect(self.rechercher)
        rech_layout.addWidget(bouton_rechercher)
        layout.addLayout(rech_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Symbole", "Nom", "Marché", "Prix (CAD)", "Graphique"])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        layout.addWidget(self.table)

        boutons = QHBoxLayout()
        annuler = QPushButton("Annuler")
        utiliser = QPushButton("Utiliser ce prix")
        boutons.addWidget(annuler)
        boutons.addWidget(utiliser)
        layout.addLayout(boutons)

        annuler.clicked.connect(self.reject)
        utiliser.clicked.connect(self.utiliser_prix)

        self.setLayout(layout)

        if nom_recherche:
            self.rechercher()


    def rechercher(self):

        terme = self.recherche.text().strip()
        if not terme:
            return

        type_ligne = self.type_ligne.currentText()

        if type_ligne == "Crypto":
            resultats = self.rechercher_crypto(terme)
        else:
            resultats = self.rechercher_bourse(terme)

        self.afficher_resultats(resultats)


    def rechercher_crypto(self, terme):

        # Auto: essayer CoinCap puis CoinGecko
        resultats = self.rechercher_coincap(terme)
        if resultats:
            return resultats

        resultats = self.rechercher_coingecko(terme)
        if resultats:
            return resultats

        QMessageBox.warning(
            self,
            "Aucun résultat",
            f"Aucune crypto trouvée pour '{terme}'.\n\n"
            "Assurez-vous d'entrer le symbole exact (ex: BTC, ETH, SOL)\n"
            "ou le nom complet (ex: Bitcoin, Ethereum)."
        )
        return []


    def rechercher_coincap(self, terme):

        try:

            terme_lower = terme.lower().strip()

            url = "https://api.coincap.io/v2/assets?limit=200"
            req = urllib.request.Request(url, headers={"User-Agent": "MBDL/1.0"})

            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))

            assets = data.get("data", [])
            if not assets:
                return []

            resultats = []
            taux = self.recuperer_taux_usd_cad()

            for asset in assets:
                symbole = asset.get("symbol", "").upper()
                nom = asset.get("name", "")
                prix_usd = float(asset.get("priceUsd", 0) or 0)

                if terme_lower in symbole.lower() or terme_lower in nom.lower():
                    prix_cad = prix_usd * taux
                    resultats.append({
                        "symbole": symbole,
                        "nom": nom,
                        "marche": "CoinCap",
                        "prix": prix_cad
                    })
                    if len(resultats) >= 10:
                        break

            return resultats

        except urllib.error.URLError:
            return []
        except:
            return []


    def recuperer_taux_usd_cad(self):

        try:
            url = "https://api.coincap.io/v2/rates/canadian-dollar"
            req = urllib.request.Request(url, headers={"User-Agent": "MBDL/1.0"})

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))

            taux_usd_cad = float(data.get("data", {}).get("rateUsd", 1.35))
            if taux_usd_cad > 0:
                return 1.0 / taux_usd_cad
            return 1.35
        except:
            return 1.35


    def rechercher_coingecko(self, terme):

        try:
            url = f"https://api.coingecko.com/api/v3/search?query={urllib.parse.quote(terme)}"
            req = urllib.request.Request(url, headers={"User-Agent": "MBDL/1.0", "Accept": "application/json"})

            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))

            coins = data.get("coins", [])[:10]
            if not coins:
                return []

            resultats = []

            for coin in coins:
                coin_id = coin["id"]
                symbole = coin.get("symbol", "").upper()
                nom = coin.get("name", "")
                prix = 0

                try:
                    url_prix = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=cad"
                    req2 = urllib.request.Request(url_prix, headers={"User-Agent": "MBDL/1.0", "Accept": "application/json"})

                    with urllib.request.urlopen(req2, timeout=10) as response2:
                        data_prix = json.loads(response2.read().decode("utf-8"))

                    prix = data_prix.get(coin_id, {}).get("cad", 0)
                except:
                    pass

                resultats.append({
                    "symbole": symbole,
                    "nom": nom,
                    "marche": "CoinGecko",
                    "prix": prix
                })

            return resultats

        except urllib.error.HTTPError as e:
            if e.code == 429:
                QMessageBox.warning(self, "Limite atteinte", "CoinGecko: trop de requêtes. Attendez quelques secondes.")
            else:
                QMessageBox.warning(self, "Erreur", f"CoinGecko: erreur HTTP {e.code}.")
            return []
        except urllib.error.URLError:
            QMessageBox.warning(self, "Connection impossible", "Impossible de se connecter à CoinGecko.")
            return []
        except:
            return []


    def rechercher_bourse(self, terme):

        try:
            url = f"https://query1.finance.yahoo.com/v1/finance/search?q={urllib.parse.quote(terme)}&quotesCount=20"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))

            quotes = data.get("quotes", [])
            if not quotes:
                return []

            resultats = []

            for q in quotes:
                symbole = q.get("symbol", "")
                nom = q.get("shortname", q.get("longname", ""))
                marche = q.get("exchange", "")
                type_quote = q.get("quoteType", "")

                if type_quote not in ("EQUITY", "ETF"):
                    continue
                if not symbole or not nom:
                    continue

                resultats.append({
                    "symbole": symbole,
                    "nom": nom,
                    "marche": marche,
                    "prix": 0
                })

            if resultats:
                self.remplir_prix_bourse(resultats[:10])

            return resultats

        except urllib.error.HTTPError as e:
            QMessageBox.warning(self, "Erreur", f"Yahoo Finance: erreur HTTP {e.code}.")
            return []
        except urllib.error.URLError:
            QMessageBox.warning(self, "Connection impossible", "Impossible de se connecter à Yahoo Finance.")
            return []
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Yahoo Finance: {e}")
            return []


    def remplir_prix_bourse(self, resultats):

        for r in resultats:
            symbole = r["symbole"]
            try:
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbole)}?range=1d&interval=1d"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read().decode("utf-8"))

                meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
                r["prix"] = meta.get("regularMarketPrice", 0)
            except:
                r["prix"] = 0


    def afficher_resultats(self, resultats):

        self.table.setRowCount(0)

        for r in resultats:
            row = self.table.rowCount()
            self.table.insertRow(row)

            if r["prix"] > 0:
                if self.type_ligne.currentText() == "Crypto":
                    prix_texte = f"{r['prix']:.5f} $"
                else:
                    prix_texte = f"{r['prix']:.2f} $"
            else:
                prix_texte = "N/A"

            valeurs = [r["symbole"], r["nom"], r["marche"], prix_texte]

            for colonne, valeur in enumerate(valeurs):
                item = QTableWidgetItem(str(valeur))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.table.setItem(row, colonne, item)

            bouton_graph = QPushButton("📊")
            bouton_graph.setFixedWidth(40)
            bouton_graph.clicked.connect(
                lambda checked=False, s=r["symbole"], n=r["nom"]:
                self.ouvrir_graphique(s, n)
            )
            self.table.setCellWidget(row, 4, bouton_graph)


    def ouvrir_graphique(self, symbole, nom):
        type_ligne = self.type_ligne.currentText()
        dialog = BourseGraphiqueDialog(type_ligne, symbole, nom, self)
        dialog.exec()


    def utiliser_prix(self):

        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Sélection", "Veuillez sélectionner une ligne.")
            return

        prix_texte = self.table.item(row, 3).text()
        if prix_texte == "N/A":
            QMessageBox.warning(self, "Prix indisponible", "Le prix n'a pas pu être récupéré.")
            return

        try:
            self.prix_selectionne = float(prix_texte.replace(" $", "").replace(",", "."))
        except:
            self.prix_selectionne = 0

        self.symbole_selectionne = self.table.item(row, 0).text()
        self.nom_selectionne = self.table.item(row, 1).text()
        self.accept()
