from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
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
from pages.infos_dialog import InfosDialog


# =========================================
# REGLAGE DE LA COLONNE DE GAUCHE
# =========================================

LISTE_HAUT = 18

LISTE_HAUTEUR = 575

BOUTON_BAS = 20

# Taille commune des boutons de gauche
BOUTON_LARGEUR = 200

BOUTON_HAUTEUR = 28


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Mon bas de laine v1.41")
        self.setFixedSize(1400, 750)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout()
        central.setLayout(layout)


        # =========================
        # COLONNE DE GAUCHE
        # =========================

        colonne = QVBoxLayout()

        colonne.setSpacing(0)

        colonne.setContentsMargins(0, 0, 0, 0)


        # =========================
        # MENU GAUCHE
        # =========================

        self.menu = QListWidget()
        self.menu.setFixedWidth(230)

        self.menu.setFixedHeight(
            LISTE_HAUTEUR
        )

        # ---------------------------------
        # ACTIFS
        # ---------------------------------

        self.ajouter_separateur("ACTIFS")

        self.menu.addItem("Entrées")
        self.menu.addItem("Sorties")
        self.menu.addItem("Patrimoine")
        self.menu.addItem("Taxes et impôts")

        # ---------------------------------
        # INVESTISSEMENTS
        # ---------------------------------

        self.ajouter_separateur("INVESTISSEMENTS")

        self.menu.addItem("Placements")
        self.menu.addItem("Cotisations REER/CELI")
        self.menu.addItem("Bourse et Cryptos")

        # ---------------------------------
        # DETTES
        # ---------------------------------

        self.ajouter_separateur("DETTES")

        self.menu.addItem("Prêts")
        self.menu.addItem("Hypothèques")

        # ---------------------------------
        # TOTAUX
        # ---------------------------------

        self.ajouter_separateur("TOTAUX")

        self.menu.addItem("Cumulatif")

        # ---------------------------------
        # GRAND ESPACE - avant BUDGETS
        # ---------------------------------

        self.ajouter_grand_espace()

        # ---------------------------------
        # BUDGETS
        # ---------------------------------

        self.ajouter_separateur("BUDGETS")

        self.menu.addItem("Budgets mensuels")
        self.menu.addItem("Budgets prévisionnels")

        # ---------------------------------
        # MEME ESPACE QU'AVANT BUDGETS
        # ---------------------------------

        self.ajouter_grand_espace()

        # ---------------------------------
        # CALCULATRICES
        # ---------------------------------

        self.ajouter_separateur("CALCULATRICES")

        self.menu.addItem("TPS/TVQ")
        self.menu.addItem("Tableaux d'amortissements")
        self.menu.addItem("Rendements")
        self.menu.addItem("Devises")
        self.menu.addItem("Simulateur d'impôt")

        # ---------------------------------
        # MEME ESPACE QU'AVANT BUDGETS
        # ---------------------------------

        self.ajouter_grand_espace()

        # ---------------------------------
        # MON DOSSIER
        # ---------------------------------

        self.ajouter_separateur("MON DOSSIER")

        self.menu.addItem("Assurances")


        colonne.addSpacing(
            LISTE_HAUT
        )

        colonne.addWidget(self.menu)


        # =========================
        # BOUTONS SOUS LA LISTE
        # =========================

        colonne.addSpacing(
            16
        )


        self.bouton_exporter = QPushButton(
            "Exporter les données"
        )

        self.bouton_importer = QPushButton(
            "Importer les données"
        )

        self.bouton_nip = QPushButton(
            "Modifier le NIP"
        )

        self.bouton_effacer = QPushButton(
            "Effacer toutes les données"
        )


        for bouton in (
            self.bouton_exporter,
            self.bouton_importer,
            self.bouton_nip,
            self.bouton_effacer
        ):

            bouton.setFixedSize(
                BOUTON_LARGEUR,
                BOUTON_HAUTEUR
            )

            colonne.addWidget(
                bouton,
                0,
                Qt.AlignHCenter
            )


        # =========================
        # ESPACE PUIS BOUTON INFOS
        # =========================

        colonne.addStretch(1)


        self.bouton_infos = QPushButton(
            "Infos"
        )

        self.bouton_infos.setFixedSize(
            BOUTON_LARGEUR,
            BOUTON_HAUTEUR
        )

        self.bouton_infos.clicked.connect(
            self.ouvrir_infos
        )

        colonne.addWidget(
            self.bouton_infos,
            0,
            Qt.AlignHCenter
        )


        colonne.addSpacing(
            BOUTON_BAS
        )


        layout.addLayout(colonne)


        # =========================
        # PAGES
        # =========================

        self.pages = QStackedWidget()
        layout.addWidget(self.pages)


        # =========================
        # CREATION DES PAGES
        # =========================
        # Un widget par ligne du menu, dans le meme ordre :
        # separateurs et espaces compris.

        # 0 - separateur ACTIFS
        self.pages.addWidget(QWidget())
        # 1
        self.pages.addWidget(EntreesPage())
        # 2
        self.pages.addWidget(SortiesPage())
        # 3
        self.pages.addWidget(PatrimoinePage())
        # 4
        self.pages.addWidget(TaxesPage())

        # 5 - separateur INVESTISSEMENTS
        self.pages.addWidget(QWidget())
        # 6
        self.pages.addWidget(PlacementsPage())
        # 7
        self.pages.addWidget(ReerCeliPage())
        # 8
        self.pages.addWidget(BoursePage())

        # 9 - separateur DETTES
        self.pages.addWidget(QWidget())
        # 10
        self.pages.addWidget(PretsPage())
        # 11
        self.pages.addWidget(HypothequePage())

        # 12 - separateur TOTAUX
        self.pages.addWidget(QWidget())
        # 13
        self.pages.addWidget(CumulatifPage())

        # 14 - grand espace
        self.pages.addWidget(QWidget())

        # 15 - separateur BUDGETS
        self.pages.addWidget(QWidget())
        # 16
        self.pages.addWidget(BudgetMensuelPage())
        # 17
        self.pages.addWidget(BudgetsPage())

        # 18 - grand espace
        self.pages.addWidget(QWidget())

        # 19 - separateur CALCULATRICES
        self.pages.addWidget(QWidget())
        # 20
        self.pages.addWidget(TpsTvqPage())
        # 21
        self.pages.addWidget(AmortissementPage())
        # 22
        self.pages.addWidget(RendementPage())
        # 23
        self.pages.addWidget(DevisesPage())
        # 24
        self.pages.addWidget(ImpotPage())

        # 25 - grand espace
        self.pages.addWidget(QWidget())

        # 26 - separateur MON DOSSIER
        self.pages.addWidget(QWidget())
        # 27
        self.pages.addWidget(AssurancesPage())


        # =========================
        # DIALOGUE INFOS
        # =========================

        self.dialogue_infos = InfosDialog(
            self
        )


        # =========================
        # BRANCHEMENT DES BOUTONS
        # =========================

        self.bouton_exporter.clicked.connect(
            self.dialogue_infos.exporter_donnees
        )

        self.bouton_importer.clicked.connect(
            self.dialogue_infos.importer_donnees
        )

        self.bouton_nip.clicked.connect(
            self.dialogue_infos.ouvrir_changement_mot_passe
        )

        self.bouton_effacer.clicked.connect(
            self.dialogue_infos.reset_application
        )


        # =========================
        # CHANGEMENT PAGE
        # =========================

        page_suivante = 0

        for ligne in range(self.menu.count()):

            item = self.menu.item(ligne)

            if item is None:
                continue

            if item.flags() & Qt.ItemIsSelectable:

                item.setData(Qt.UserRole, page_suivante)
                page_suivante += 1

            else:

                page_suivante += 1

        self.menu.currentRowChanged.connect(self.changer_page)

        # Ouverture sur Entrées
        self.menu.setCurrentRow(1)



    # =========================
    # INFOS
    # =========================

    def ouvrir_infos(self):

        self.dialogue_infos.exec()



    # =========================
    # AJOUT D'ITEMS
    # =========================

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



    def ajouter_grand_espace(self):

        item = QListWidgetItem("")
        item.setFlags(Qt.NoItemFlags)
        item.setSizeHint(QSize(0, 40))
        self.menu.addItem(item)



    def changer_page(self, index):

        if index < 0:
            return

        item = self.menu.item(index)

        if item is None:
            return

        if not (item.flags() & Qt.ItemIsSelectable):
            return

        page = item.data(Qt.UserRole)

        if page is None:
            return

        self.pages.setCurrentIndex(page)
