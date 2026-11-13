from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QStackedWidget
)

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QBrush, QFont

from pages.entrees import EntreesPage
from pages.sorties import SortiesPage
from pages.patrimoine import PatrimoinePage
from pages.taxes import TaxesPage
from pages.placements import PlacementsPage
from pages.reer_celi import ReerCeliPage
from pages.bourse import BoursePage
from pages.prets import PretsPage
from pages.hypotheque import HypothequePage
from pages.assurances import AssurancesPage
from pages.cumulatif import CumulatifPage
from pages.budget_mensuel import BudgetMensuelPage
from pages.budgets import BudgetsPage
from pages.tps_tvq import TpsTvqPage
from pages.amortissement import AmortissementPage
from pages.rendement import RendementPage
from pages.devises import DevisesPage
from pages.impot import ImpotPage
from pages.a_propos import AProposPage


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Mon bas de laine")
        self.setFixedSize(1400, 750)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout()
        central.setLayout(layout)


        # =========================
        # MENU GAUCHE
        # =========================

        self.menu = QListWidget()
        self.menu.setFixedWidth(230)

        # 0 --- ACTIFS
        self.ajouter_separateur("ACTIFS")
        # 1
        self.menu.addItem("Entrées")
        # 2
        self.menu.addItem("Sorties")

        # 3 - Patrimoine
        self.menu.addItem("Patrimoine")

        # 4
        self.menu.addItem("Taxes et impôts")

        # 5 --- INVESTISSEMENTS
        self.ajouter_separateur("INVESTISSEMENTS")
        # 6
        self.menu.addItem("Placements")
        # 7
        self.menu.addItem("Cotisations REER/CELI")
        # 8
        self.menu.addItem("Bourse et Cryptos")

        # 8 --- DETTES
        self.ajouter_separateur("DETTES")
        # 9
        self.menu.addItem("Prêts")
        # 10
        self.menu.addItem("Hypothèques")

        # 11 --- MON DOSSIER
        self.ajouter_separateur("MON DOSSIER")
        # 12
        self.menu.addItem("Assurances")

        # 13 --- TOTAUX
        self.ajouter_separateur("TOTAUX")
        # 14
        self.menu.addItem("Cumulatif")
        # 15
        self.ajouter_ligne_vide()

        # 16 --- BUDGETS
        self.ajouter_separateur("BUDGETS")
        # 17
        self.menu.addItem("Budgets mensuels")
        # 18
        self.menu.addItem("Budgets prévisionnels")
        # 19
        self.ajouter_ligne_vide()

        # 20 --- CALCULATRICE
        self.ajouter_separateur("CALCULATRICE")
        # 21
        self.menu.addItem("TPS/TVQ")
        # 22
        self.menu.addItem("Tableaux d'amortissements")
        # 24
        self.menu.addItem("Rendements")
        # 25
        self.menu.addItem("Devises")
        self.menu.addItem("Simulateur d'impôt")
        # 26
        self.ajouter_ligne_vide()

        # 27 --- AUTRES
        self.ajouter_separateur("AUTRES")
        # 28
        self.menu.addItem("À Propos")


        layout.addWidget(self.menu)


        # =========================
        # PAGES
        # =========================

        self.pages = QStackedWidget()
        layout.addWidget(self.pages)


        # =========================
        # CREATION DES PAGES
        # =========================

        # 0 - separateur
        self.pages.addWidget(QWidget())
        # 1
        self.pages.addWidget(EntreesPage())
        # 2
        self.pages.addWidget(SortiesPage())

        # 3
        self.pages.addWidget(PatrimoinePage())

        # 4
        self.pages.addWidget(TaxesPage())
        # 5 - separateur
        self.pages.addWidget(QWidget())
        # 6
        self.pages.addWidget(PlacementsPage())
        # 7
        self.pages.addWidget(ReerCeliPage())
        # 8
        self.pages.addWidget(BoursePage())
        # 9 - separateur
        self.pages.addWidget(QWidget())
        # 10
        self.pages.addWidget(PretsPage())
        # 11
        self.pages.addWidget(HypothequePage())
        # 12 - separateur
        self.pages.addWidget(QWidget())
        # 13
        self.pages.addWidget(AssurancesPage())
        # 14 - separateur
        self.pages.addWidget(QWidget())
        # 15
        self.pages.addWidget(CumulatifPage())
        # 16 - ligne vide
        self.pages.addWidget(QWidget())
        # 17 - separateur
        self.pages.addWidget(QWidget())
        # 18
        self.pages.addWidget(BudgetMensuelPage())
        # 19
        self.pages.addWidget(BudgetsPage())
        # 20 - ligne vide
        self.pages.addWidget(QWidget())
        # 21 - separateur
        self.pages.addWidget(QWidget())
        # 22
        self.pages.addWidget(TpsTvqPage())
        # 23
        self.pages.addWidget(AmortissementPage())
        # 25
        self.pages.addWidget(RendementPage())
        # 26
        self.pages.addWidget(DevisesPage())
        # 27
        self.pages.addWidget(ImpotPage())
        # 28 - ligne vide
        self.pages.addWidget(QWidget())
        # 29 - separateur
        self.pages.addWidget(QWidget())
        # 30
        self.pages.addWidget(AProposPage())


        # =========================
        # CHANGEMENT PAGE
        # =========================

        # Chaque item cliquable memorise l'index de sa page.
        # L'association se construit en parcourant le menu et la pile
        # dans le meme ordre : plus aucune liste d'index a maintenir.
        page_suivante = 0

        for ligne in range(self.menu.count()):

            item = self.menu.item(ligne)

            if item is None:
                continue

            if item.flags() & Qt.ItemIsSelectable:

                # Item cliquable : il consomme la page correspondante
                item.setData(Qt.UserRole, page_suivante)
                page_suivante += 1

            else:

                # Separateur ou ligne vide : il consomme aussi une page
                page_suivante += 1

        self.menu.currentRowChanged.connect(self.changer_page)

        # Ouverture sur Entrées
        self.menu.setCurrentRow(1)



    def ajouter_separateur(self, texte):

        item = QListWidgetItem(texte)
        item.setFlags(Qt.NoItemFlags)
        item.setBackground(QBrush(QColor(210, 210, 210)))
        item.setForeground(QBrush(QColor(0, 0, 0)))
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        police = QFont()
        police.setBold(True)
        item.setFont(police)

        self.menu.addItem(item)



    def ajouter_ligne_vide(self):

        item = QListWidgetItem("")
        item.setFlags(Qt.NoItemFlags)
        item.setSizeHint(QSize(0, 8))
        self.menu.addItem(item)



    def changer_page(self, index):

        if index < 0:
            return

        item = self.menu.item(index)

        if item is None:
            return

        # Ne rien faire si l'item n'est pas selectionnable
        if not (item.flags() & Qt.ItemIsSelectable):
            return

        page = item.data(Qt.UserRole)

        if page is None:
            return

        self.pages.setCurrentIndex(page)
