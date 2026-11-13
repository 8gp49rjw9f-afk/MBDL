import json
import urllib.request
import urllib.parse
import urllib.error
import time

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QMessageBox,
    QScrollArea
)

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import (
    QPixmap,
    QPainter,
    QPen,
    QColor,
    QFont,
    QBrush,
    QPolygonF
)


PERIODES_BOURSE = [
    ("1 jour", "1d", "5m"),
    ("1 semaine", "5d", "30m"),
    ("1 mois", "1mo", "1d"),
    ("6 mois", "6mo", "1d"),
    ("1 an", "1y", "1wk"),
    ("2 ans", "2y", "1wk"),
    ("5 ans", "5y", "1mo"),
]

PERIODES_CRYPTO = [
    ("1 jour", 1),
    ("1 semaine", 7),
    ("1 mois", 30),
    ("3 mois", 90),
    ("6 mois", 180),
    ("1 an", 365),
]


class BourseGraphiqueDialog(QDialog):

    def __init__(self, type_ligne, symbole, nom, parent=None):

        super().__init__(parent)

        self.type_ligne = type_ligne
        self.symbole = symbole
        self.nom = nom

        self.setWindowTitle(f"Graphique - {nom}")
        self.resize(950, 650)

        layout = QVBoxLayout()

        titre = QLabel(f"Graphique historique - {nom} ({symbole or 'Inconnu'})")
        titre.setStyleSheet("font-size:20px;font-weight:bold;")
        layout.addWidget(titre)

        controles_layout = QHBoxLayout()

        controles_layout.addWidget(QLabel("Période:"))
        self.choix_periode = QComboBox()
        controles_layout.addWidget(self.choix_periode)

        controles_layout.addWidget(QLabel("Source:"))
        self.choix_source = QComboBox()

        if type_ligne == "Crypto":
            self.choix_source.addItem("Auto", "auto")
            self.choix_source.addItem("CoinGecko", "coingecko")
            self.choix_source.addItem("CoinCap", "coincap")
            self.choix_source.addItem("Binance", "binance")
            self.choix_source.addItem("Messari", "messari")

            for libelle, jours in PERIODES_CRYPTO:
                self.choix_periode.addItem(libelle, jours)
        else:
            self.choix_source.addItem("Yahoo Finance", "yahoo")
            self.choix_source.addItem("Stooq", "stooq")

            for libelle, range_val, interval in PERIODES_BOURSE:
                self.choix_periode.addItem(libelle, (range_val, interval))

        self.choix_periode.currentIndexChanged.connect(self.charger_graphique)
        self.choix_source.currentIndexChanged.connect(self.charger_graphique)
        controles_layout.addWidget(self.choix_source)

        controles_layout.addStretch()

        bouton_maj = QPushButton("🔄 Rafraîchir")
        bouton_maj.clicked.connect(self.charger_graphique)
        controles_layout.addWidget(bouton_maj)

        layout.addLayout(controles_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        self.label_graphique = QLabel()
        self.label_graphique.setAlignment(Qt.AlignCenter)
        self.label_graphique.setText("Chargement...")
        self.label_graphique.setMinimumSize(900, 500)
        scroll.setWidget(self.label_graphique)
        layout.addWidget(scroll)

        self.setLayout(layout)
        self.charger_graphique()



    def charger_graphique(self):

        self.label_graphique.setText("Chargement du graphique...")

        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()

        index = self.choix_periode.currentIndex()
        source = self.choix_source.currentData()

        if self.type_ligne == "Crypto":
            jours = self.choix_periode.itemData(index)
            data = self.recuperer_crypto(source, jours)
        else:
            range_val, interval = self.choix_periode.itemData(index)
            data = self.recuperer_bourse(source, range_val, interval)

        if data == "no_internet":
            self.label_graphique.setText("Impossible de récupérer les données.\n\nVérifiez votre connexion Internet.")
            return

        if data == "not_found":
            self.label_graphique.setText("Symbole introuvable.\n\nAssurez-vous d'avoir rempli le champ 'Symbole' (ex: AAPL, BTC) dans les détails de l'action.")
            return

        if data == "rate_limit":
            self.label_graphique.setText("Limite de requêtes atteinte.\n\nAttendez quelques secondes ou changez de source.")
            return

        if not data or len(data) < 2:
            self.label_graphique.setText("Aucune donnée disponible pour cette période.")
            return

        self.dessiner_graphique(data)



    def recuperer_crypto(self, source, jours):

        if source == "auto":
            for s in ["coingecko", "coincap", "binance", "messari"]:
                data = self.recuperer_crypto(s, jours)
                if data and isinstance(data, list) and len(data) >= 2:
                    return data
            return None

        if source == "coingecko":
            return self.recuperer_donnees_crypto_coingecko(jours)
        elif source == "coincap":
            return self.recuperer_donnees_crypto_coincap(jours)
        elif source == "binance":
            return self.recuperer_donnees_crypto_binance(jours)
        elif source == "messari":
            return self.recuperer_donnees_crypto_messari(jours)

        return None



    def recuperer_donnees_crypto_coingecko(self, jours):

        try:
            terme = self.symbole or self.nom
            if not terme:
                return "not_found"

            url_search = f"https://api.coingecko.com/api/v3/search?query={urllib.parse.quote(terme)}"
            req = urllib.request.Request(url_search, headers={"User-Agent": "MBDL/1.0", "Accept": "application/json"})

            with urllib.request.urlopen(req, timeout=15) as response:
                data_search = json.loads(response.read().decode("utf-8"))

            coins = data_search.get("coins", [])
            if not coins:
                return "not_found"

            coin_id = coins[0]["id"]

            jours = min(jours, 365)

            url_chart = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=cad&days={jours}"

            req2 = urllib.request.Request(url_chart, headers={"User-Agent": "MBDL/1.0", "Accept": "application/json"})

            with urllib.request.urlopen(req2, timeout=15) as response2:
                data_chart = json.loads(response2.read().decode("utf-8"))

            prices = data_chart.get("prices", [])
            return [p[1] for p in prices]

        except urllib.error.HTTPError as e:
            if e.code == 429:
                return "rate_limit"
            elif e.code == 404:
                return "not_found"
            else:
                return None
        except urllib.error.URLError:
            return "no_internet"
        except:
            return None



    def recuperer_donnees_crypto_coincap(self, jours):

        try:
            terme = (self.symbole or self.nom or "").lower().strip()
            if not terme:
                return "not_found"

            url_assets = "https://api.coincap.io/v2/assets?limit=200"
            req = urllib.request.Request(url_assets, headers={"User-Agent": "MBDL/1.0"})

            with urllib.request.urlopen(req, timeout=15) as response:
                data_assets = json.loads(response.read().decode("utf-8"))

            assets = data_assets.get("data", [])
            coin_id = None

            for asset in assets:
                if asset.get("symbol", "").lower() == terme or asset.get("name", "").lower() == terme:
                    coin_id = asset.get("id")
                    break

            if not coin_id:
                return "not_found"

            end = int(time.time() * 1000)
            start = end - (jours * 86400000)

            url_hist = f"https://api.coincap.io/v2/assets/{coin_id}/history?interval=d1&start={start}&end={end}"
            req2 = urllib.request.Request(url_hist, headers={"User-Agent": "MBDL/1.0"})

            with urllib.request.urlopen(req2, timeout=15) as response2:
                data_hist = json.loads(response2.read().decode("utf-8"))

            history = data_hist.get("data", [])

            if not history:
                return None

            taux = self.recuperer_taux_usd_cad()

            return [float(point.get("priceUsd", 0)) * taux for point in history if point.get("priceUsd")]

        except urllib.error.HTTPError as e:
            if e.code == 429:
                return "rate_limit"
            return "not_found"
        except urllib.error.URLError:
            return "no_internet"
        except:
            return None



    def recuperer_donnees_crypto_binance(self, jours):

        try:
            symbole = (self.symbole or "").upper().strip()
            if not symbole:
                return "not_found"

            # Binance klines: interval=1d, limit=jours
            pair = symbole + "USDT"

            url = f"https://api.binance.com/api/v3/klines?symbol={pair}&interval=1d&limit={jours}"

            req = urllib.request.Request(url, headers={"User-Agent": "MBDL/1.0"})

            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))

            if not data:
                return "not_found"

            # Format Binance: [openTime, open, high, low, close, volume, ...]
            taux = self.recuperer_taux_usd_cad()

            return [float(kline[4]) * taux for kline in data]

        except urllib.error.HTTPError as e:
            if e.code == 400:
                return "not_found"
            if e.code == 429:
                return "rate_limit"
            return None
        except urllib.error.URLError:
            return "no_internet"
        except:
            return None



    def recuperer_donnees_crypto_messari(self, jours):

        try:
            terme = (self.symbole or self.nom or "").lower().strip()
            if not terme:
                return "not_found"

            # Messari: chercher l'asset par symbole
            url_search = f"https://data.messari.io/api/v1/assets?fields=id,symbol,name&limit=200"

            req = urllib.request.Request(url_search, headers={"User-Agent": "MBDL/1.0"})

            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))

            assets = data.get("data", [])
            asset_id = None

            for asset in assets:
                if asset.get("symbol", "").lower() == terme or asset.get("name", "").lower() == terme:
                    asset_id = asset.get("id")
                    break

            if not asset_id:
                return "not_found"

            # Messari timeseries: interval=1d
            url_ts = f"https://data.messari.io/api/v1/assets/{asset_id}/metrics/price/time-series?interval=1d&columns=close&limit={jours}"

            req2 = urllib.request.Request(url_ts, headers={"User-Agent": "MBDL/1.0"})

            with urllib.request.urlopen(req2, timeout=15) as response2:
                data_ts = json.loads(response2.read().decode("utf-8"))

            values = data_ts.get("data", {}).get("values", [])

            if not values:
                return None

            taux = self.recuperer_taux_usd_cad()

            # values = [[timestamp, close], ...]
            return [float(v[1]) * taux for v in values if v[1] is not None]

        except urllib.error.HTTPError as e:
            if e.code == 429:
                return "rate_limit"
            if e.code == 404:
                return "not_found"
            return None
        except urllib.error.URLError:
            return "no_internet"
        except:
            return None



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



    def recuperer_bourse(self, source, range_val, interval):

        if source == "auto" or source == "yahoo":
            return self.recuperer_donnees_bourse_yahoo(range_val, interval)
        elif source == "stooq":
            return self.recuperer_donnees_bourse_stooq(range_val)

        return self.recuperer_donnees_bourse_yahoo(range_val, interval)



    def recuperer_donnees_bourse_yahoo(self, range_val, interval):

        try:
            symbole = self.symbole
            if not symbole:
                return "not_found"

            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbole)}?range={range_val}&interval={interval}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))

            result = data.get("chart", {}).get("result", [])
            if not result:
                return "not_found"

            quotes = result[0].get("indicators", {}).get("quote", [])
            if not quotes:
                return "not_found"

            closes = quotes[0].get("close", [])
            return [c for c in closes if c is not None]

        except urllib.error.HTTPError as e:
            if e.code == 404:
                return "not_found"
            elif e.code == 429:
                return "rate_limit"
            return None
        except urllib.error.URLError:
            return "no_internet"
        except:
            return None



    def recuperer_donnees_bourse_stooq(self, range_val):

        try:
            symbole = self.symbole
            if not symbole:
                return "not_found"

            # Stooq: telecharger l'historique en CSV
            # Convertir range_val en jours
            jours_map = {"1d": 1, "5d": 7, "1mo": 30, "6mo": 180, "1y": 365, "2y": 730, "5y": 1825}
            jours = jours_map.get(range_val, 365)

            # Calculer la date de debut
            from datetime import datetime, timedelta
            fin = datetime.now()
            debut = fin - timedelta(days=jours)

            url = f"https://stooq.com/q/d/l/?s={symbole.lower()}&d1={debut.strftime('%Y%m%d')}&d2={fin.strftime('%Y%m%d')}&i=d"

            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

            with urllib.request.urlopen(req, timeout=15) as response:
                csv_data = response.read().decode("utf-8")

            lignes = csv_data.strip().split("\n")

            if len(lignes) < 2:
                return "not_found"

            # Format: Date,Open,High,Low,Close,Volume
            closes = []

            for ligne in lignes[1:]:
                parties = ligne.split(",")
                if len(parties) >= 5:
                    try:
                        closes.append(float(parties[4]))
                    except:
                        pass

            return closes if closes else "not_found"

        except urllib.error.HTTPError as e:
            if e.code == 404:
                return "not_found"
            return None
        except urllib.error.URLError:
            return "no_internet"
        except:
            return None



    def dessiner_graphique(self, data):

        try:
            largeur = 900
            hauteur = 500
            marge_gauche = 80
            marge_droite = 40
            marge_haut = 40
            marge_bas = 60

            largeur_trace = largeur - marge_gauche - marge_droite
            hauteur_trace = hauteur - marge_haut - marge_bas

            prix_min = min(data)
            prix_max = max(data)
            prix_actuel = data[-1]
            prix_initial = data[0]

            if prix_max == prix_min:
                prix_max = prix_min + 1

            couleur_principale = QColor(27, 127, 46) if prix_actuel >= prix_initial else QColor(192, 32, 32)

            pixmap = QPixmap(largeur, hauteur)
            pixmap.fill(QColor(255, 255, 255))

            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)

            painter.fillRect(0, 0, largeur, hauteur, QBrush(QColor(255, 255, 255)))

            pen_grille = QPen(QColor(240, 240, 240), 1, Qt.DashLine)
            painter.setPen(pen_grille)

            for i in range(6):
                y = marge_haut + (hauteur_trace * i / 5)
                painter.drawLine(marge_gauche, y, marge_gauche + largeur_trace, y)

            painter.setPen(QPen(QColor(100, 100, 100), 1))
            painter.drawLine(marge_gauche, marge_haut, marge_gauche, marge_haut + hauteur_trace)
            painter.drawLine(marge_gauche, marge_haut + hauteur_trace, marge_gauche + largeur_trace, marge_haut + hauteur_trace)

            font = QFont("Arial", 9)
            painter.setFont(font)
            painter.setPen(QColor(80, 80, 80))

            for i in range(6):
                y = marge_haut + (hauteur_trace * i / 5)
                prix = prix_max - (prix_max - prix_min) * i / 5
                painter.drawText(QRectF(5, y - 10, marge_gauche - 10, 20), Qt.AlignRight | Qt.AlignVCenter, f"{prix:.2f} $")

            nb_points = len(data)
            for i in range(6):
                x = marge_gauche + (largeur_trace * i / 5)
                index = int(nb_points * i / 5)
                painter.drawText(QRectF(x - 40, marge_haut + hauteur_trace + 5, 80, 20), Qt.AlignCenter, f"{index}")

            painter.drawText(QRectF(marge_gauche + largeur_trace / 2 - 30, marge_haut + hauteur_trace + 30, 60, 20), Qt.AlignCenter, "Points dans le temps →")

            pen_ligne = QPen(couleur_principale, 2)
            painter.setPen(pen_ligne)

            points = []

            for i, prix in enumerate(data):
                x = marge_gauche + (largeur_trace * i / (nb_points - 1)) if nb_points > 1 else marge_gauche
                y = marge_haut + hauteur_trace - (prix - prix_min) / (prix_max - prix_min) * hauteur_trace
                points.append(QPointF(x, y))

            couleur_fill = QColor(couleur_principale)
            couleur_fill.setAlpha(40)

            if len(points) >= 2:
                poly = QPolygonF(points)
                poly.append(QPointF(points[-1].x(), marge_haut + hauteur_trace))
                poly.append(QPointF(points[0].x(), marge_haut + hauteur_trace))
                painter.setBrush(QBrush(couleur_fill))
                painter.setPen(Qt.NoPen)
                painter.drawPolygon(poly)

            painter.setPen(pen_ligne)
            painter.setBrush(Qt.NoBrush)

            for i in range(len(points) - 1):
                painter.drawLine(points[i], points[i + 1])

            painter.setBrush(QBrush(couleur_principale))
            painter.drawEllipse(points[-1], 5, 5)

            font_info = QFont("Arial", 11, QFont.Bold)
            painter.setFont(font_info)

            variation = ((prix_actuel - prix_initial) / prix_initial) * 100 if prix_initial > 0 else 0

            info_texte = f"Min: {prix_min:.2f} $   |   Max: {prix_max:.2f} $   |   Actuel: {prix_actuel:.2f} $   |   Variation: {variation:+.2f}%"

            painter.setPen(couleur_principale)
            painter.drawText(QRectF(marge_gauche, 5, largeur_trace, 30), Qt.AlignLeft | Qt.AlignVCenter, info_texte)

            painter.end()

            self.label_graphique.setPixmap(pixmap)

        except Exception as e:
            self.label_graphique.setText(f"Erreur lors du tracé du graphique:\n\n{e}")
