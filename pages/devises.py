import json
import urllib.request
import urllib.error

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QAbstractItemView
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont


# Liste des devises supportees
DEVISES = [
    ("Canada", "Dollar Canadien", "CAD", "$"),
    ("États-Unis", "Dollar Américain", "USD", "$"),
    ("Europe", "Euro", "EUR", "€"),
    ("Royaume-Uni", "Livre Sterling", "GBP", "£"),
    ("Suisse", "Franc Suisse", "CHF", "Fr"),
    ("Japon", "Yen", "JPY", "¥"),
    ("Australie", "Dollar Australien", "AUD", "$"),
    ("Chine", "Yuan", "CNY", "¥"),
    ("Inde", "Roupie", "INR", "₹"),
    ("Mexique", "Peso", "MXN", "$"),
    ("Brésil", "Real", "BRL", "R$"),
    ("Norvège", "Couronne", "NOK", "kr"),
    ("Suède", "Couronne", "SEK", "kr"),
    ("Danemark", "Couronne", "DKK", "kr"),
    ("Nouvelle-Zélande", "Dollar Néo-Zélandais", "NZD", "$"),
    ("Singapour", "Dollar de Singapour", "SGD", "$"),
    ("Hong Kong", "Dollar de Hong Kong", "HKD", "$"),
    ("Corée du Sud", "Won", "KRW", "₩"),
    ("Taïwan", "Dollar Taïwanais", "TWD", "$"),
    ("Thaïlande", "Baht", "THB", "฿"),
    ("Malaisie", "Ringgit", "MYR", "RM"),
    ("Indonésie", "Roupie Indonésienne", "IDR", "Rp"),
    ("Philippines", "Peso Philippin", "PHP", "₱"),
    ("Vietnam", "Dong", "VND", "₫"),
    ("Pologne", "Zloty", "PLN", "zł"),
    ("Tchéquie", "Couronne Tchèque", "CZK", "Kč"),
    ("Hongrie", "Forint", "HUF", "Ft"),
    ("Roumanie", "Leu", "RON", "lei"),
    ("Turquie", "Livre Turque", "TRY", "₺"),
    ("Russie", "Rouble", "RUB", "₽"),
    ("Afrique du Sud", "Rand", "ZAR", "R"),
    ("Israël", "Shekel", "ILS", "₪"),
    ("Émirats Arabes Unis", "Dirham", "AED", "د.إ"),
    ("Arabie Saoudite", "Riyal", "SAR", "﷼"),
    ("Argentine", "Peso Argentin", "ARS", "$"),
    ("Chili", "Peso Chilien", "CLP", "$"),
    ("Colombie", "Peso Colombien", "COP", "$"),
]


class DevisesPage(QWidget):

    def __init__(self):

        super().__init__()

        # Taux de change par defaut (1 CAD = X)
        # Ces valeurs seront mises a jour avec le bouton
        self.taux = {
            "CAD": 1.0,
            "USD": 0.73,
            "EUR": 0.80,
            "GBP": 0.59,
            "CHF": 0.65,
            "JPY": 109.50,
            "AUD": 1.10,
            "CNY": 5.30,
            "INR": 61.00,
            "MXN": 12.50,
            "BRL": 3.60,
            "NOK": 6.80,
            "SEK": 6.90,
            "DKK": 5.00,
            "NZD": 1.19,
            "SGD": 0.98,
            "HKD": 5.70,
            "KRW": 960.00,
            "TWD": 22.90,
            "THB": 26.50,
            "MYR": 3.30,
            "IDR": 11500.00,
            "PHP": 41.00,
            "VND": 18500.00,
            "PLN": 2.90,
            "CZK": 16.50,
            "HUF": 265.00,
            "RON": 3.30,
            "TRY": 23.00,
            "RUB": 68.00,
            "ZAR": 13.50,
            "ILS": 2.70,
            "AED": 2.70,
            "SAR": 2.75,
            "ARS": 620.00,
            "CLP": 690.00,
            "COP": 2950.00,
        }

        layout = QVBoxLayout()


        titre = QLabel("Devises")
        titre.setStyleSheet("font-size:28px;font-weight:bold;")
        layout.addWidget(titre)


        # =========================
        # SECTION DU HAUT
        # =========================

        haut_layout = QHBoxLayout()

        haut_layout.addWidget(QLabel("Devise source:"))

        self.devise_source = QComboBox()
        for pays, nom, code, symbole in DEVISES:
            self.devise_source.addItem(f"{nom} ({code})", code)

        # Defaut: Dollar Canadien
        self.devise_source.setCurrentIndex(0)
        self.devise_source.currentIndexChanged.connect(self.recalculer)

        haut_layout.addWidget(self.devise_source)

        haut_layout.addWidget(QLabel("Montant:"))

        self.montant = QLineEdit()
        self.montant.setText("100")
        self.montant.textChanged.connect(self.recalculer)

        haut_layout.addWidget(self.montant)

        layout.addLayout(haut_layout)


        # =========================
        # TABLEAU
        # =========================

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Pays", "Nom de la devise", "Valeur", "Montant"]
        )

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        layout.addWidget(self.table)


        # =========================
        # BOUTON MISE A JOUR
        # =========================

        bouton_maj = QPushButton("MISE À JOUR (Internet)")
        bouton_maj.setStyleSheet("font-size:16px;font-weight:bold;padding:10px;")
        bouton_maj.clicked.connect(self.mettre_a_jour)

        layout.addWidget(bouton_maj)


        self.setLayout(layout)

        self.recalculer()



    def formater_montant(self, valeur, symbole="$"):

        try:
            texte = (
                f"{float(valeur):,.2f}"
                .replace(",", " ")
                .replace(".", ",")
            )
            return texte + " " + symbole
        except:
            return "0,00 " + symbole



    def convertir(self, valeur):

        try:
            return float(
                str(valeur)
                .replace(" ", "")
                .replace(",", ".")
                .replace("$", "")
            )
        except:
            return 0



    def recalculer(self):

        montant_source = self.convertir(self.montant.text())
        code_source = self.devise_source.currentData()
        taux_source = self.taux.get(code_source, 1.0)


        self.table.setRowCount(0)

        for pays, nom, code, symbole in DEVISES:

            if code == code_source:
                continue

            row = self.table.rowCount()
            self.table.insertRow(row)

            taux_devise = self.taux.get(code, 1.0)

            # Convertir: montant_source -> source -> CAD -> devise cible
            if taux_source > 0:
                montant_cad = montant_source / taux_source
            else:
                montant_cad = 0

            montant_cible = montant_cad * taux_devise

            valeurs = [
                pays,
                nom,
                f"{taux_devise:.4f}",
                self.formater_montant(montant_cible, symbole)
            ]

            for colonne, valeur in enumerate(valeurs):
                item = QTableWidgetItem(valeur)
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(row, colonne, item)



    def mettre_a_jour(self):

        code_source = self.devise_source.currentData()

        try:

            url = f"[open.er-api.com](https://open.er-api.com/v6/latest/{code_source})"

            req = urllib.request.Request(url, headers={"User-Agent": "MBDL/1.0"})

            with urllib.request.urlopen(req, timeout=10) as response:

                data = json.loads(response.read().decode("utf-8"))


            if data.get("result") != "success":

                QMessageBox.warning(
                    self,
                    "Erreur",
                    "Les taux de change n'ont pas pu être récupérés."
                )

                return


            rates = data.get("rates", {})

            manquants = []

            for code in self.taux:
                if code in rates:
                    self.taux[code] = rates[code]
                else:
                    manquants.append(code)


            self.recalculer()


            message = "Les taux de change ont été mis à jour avec succès."

            if manquants:
                message += (
                    "\n\nCodes sans taux reçu : "
                    + ", ".join(manquants)
                )


            QMessageBox.information(
                self,
                "Mise à jour",
                message
            )


        except urllib.error.URLError:

            QMessageBox.warning(
                self,
                "Connection impossible",
                "Impossible de se connecter à Internet.\n\n"
                "Vérifiez votre connexion réseau."
            )


        except Exception as e:

            QMessageBox.warning(
                self,
                "Erreur",
                f"Une erreur est survenue:\n\n{e}"
            )
