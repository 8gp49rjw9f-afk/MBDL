from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)



def formater_montant(
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
# VUE GENERIQUE
# =========================

class CroissanceViewDialog(QDialog):

    def __init__(
        self,
        donnees,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            donnees.get(
                "titre",
                "Détail"
            )
        )


        self.resize(
            900,
            650
        )


        layout = QVBoxLayout()


        titre = QLabel(
            donnees.get(
                "nom",
                ""
            )
        )

        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(
            titre
        )


        resume = QLabel(
            "\n".join(
                donnees.get(
                    "resume",
                    []
                )
            )
        )

        resume.setStyleSheet(
            "font-size:16px;"
        )

        layout.addWidget(
            resume
        )


        entetes = donnees.get(
            "entetes",
            []
        )


        lignes = donnees.get(
            "lignes",
            []
        )


        table = QTableWidget()


        table.setColumnCount(
            len(entetes)
        )


        table.setHorizontalHeaderLabels(
            entetes
        )


        header = table.horizontalHeader()


        for i in range(
            len(entetes)
        ):

            header.setSectionResizeMode(
                i,
                QHeaderView.Stretch
            )


        table.setRowCount(
            len(lignes)
        )


        for row, ligne in enumerate(lignes):

            for colonne, valeur in enumerate(ligne):

                table.setItem(
                    row,
                    colonne,
                    QTableWidgetItem(
                        str(valeur)
                    )
                )


        layout.addWidget(
            table
        )


        self.setLayout(
            layout
        )



# =========================
# RENDEMENT
# =========================

class RendementDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Ajouter un calcul de rendement"
        )


        self.resize(
            420,
            440
        )


        layout = QVBoxLayout()


        titre = QLabel(
            "Ajouter un calcul de rendement"
        )

        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(
            titre
        )


        layout.addWidget(
            QLabel(
                "Nom"
            )
        )

        self.nom = QLineEdit()

        self.nom.setPlaceholderText(
            "Ex: CELI 90 mois"
        )

        layout.addWidget(
            self.nom
        )


        layout.addWidget(
            QLabel(
                "Montant initial"
            )
        )

        self.montant_initial = QLineEdit()

        self.montant_initial.setPlaceholderText(
            "Ex: 10000.00"
        )

        layout.addWidget(
            self.montant_initial
        )


        layout.addWidget(
            QLabel(
                "% intérêt annuel"
            )
        )

        self.taux = QLineEdit()

        self.taux.setPlaceholderText(
            "Ex: 4"
        )

        layout.addWidget(
            self.taux
        )


        layout.addWidget(
            QLabel(
                "Nombre de mois"
            )
        )

        self.mois = QLineEdit()

        self.mois.setPlaceholderText(
            "Ex: 90"
        )

        layout.addWidget(
            self.mois
        )


        layout.addWidget(
            QLabel(
                "Cotisation mensuelle"
            )
        )

        self.cotisation_mensuelle = QLineEdit()

        self.cotisation_mensuelle.setPlaceholderText(
            "0.00"
        )

        layout.addWidget(
            self.cotisation_mensuelle
        )


        boutons = QHBoxLayout()


        annuler = QPushButton(
            "Annuler"
        )

        sauvegarder = QPushButton(
            "Sauvegarder"
        )

        sauvegarder.setDefault(
            True
        )

        sauvegarder.setAutoDefault(
            True
        )

        boutons.addWidget(
            annuler
        )

        boutons.addWidget(
            sauvegarder
        )


        layout.addLayout(
            boutons
        )


        annuler.clicked.connect(
            self.reject
        )

        sauvegarder.clicked.connect(
            self.accept
        )


        self.setLayout(
            layout
        )



class RendementEditDialog(RendementDialog):

    def __init__(
        self,
        rendement,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Modifier un calcul de rendement"
        )


        self.nom.setText(
            str(rendement[1] or "")
        )

        self.montant_initial.setText(
            str(rendement[2] or "")
        )

        self.taux.setText(
            str(rendement[3] or "")
        )

        self.mois.setText(
            str(rendement[4] or "")
        )

        self.cotisation_mensuelle.setText(
            str(rendement[5] or "")
        )



# =========================
# RETRAITE
# =========================

class RetraiteDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Ajouter un calcul de retraite"
        )


        self.resize(
            420,
            440
        )


        layout = QVBoxLayout()


        titre = QLabel(
            "Ajouter un calcul de retraite"
        )

        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(
            titre
        )


        layout.addWidget(
            QLabel(
                "Nom"
            )
        )

        self.nom = QLineEdit()

        self.nom.setPlaceholderText(
            "Ex: Retraite à 60 ans"
        )

        layout.addWidget(
            self.nom
        )


        layout.addWidget(
            QLabel(
                "Placement actuel"
            )
        )

        self.placement_actuel = QLineEdit()

        self.placement_actuel.setPlaceholderText(
            "Ex: 50000.00"
        )

        layout.addWidget(
            self.placement_actuel
        )


        layout.addWidget(
            QLabel(
                "Nombre d'années"
            )
        )

        self.annees = QLineEdit()

        self.annees.setPlaceholderText(
            "Ex: 25"
        )

        layout.addWidget(
            self.annees
        )


        layout.addWidget(
            QLabel(
                "% intérêt annuel"
            )
        )

        self.taux = QLineEdit()

        self.taux.setPlaceholderText(
            "Ex: 5"
        )

        layout.addWidget(
            self.taux
        )


        layout.addWidget(
            QLabel(
                "Cotisation par année"
            )
        )

        self.cotisation_annuelle = QLineEdit()

        self.cotisation_annuelle.setPlaceholderText(
            "0.00"
        )

        layout.addWidget(
            self.cotisation_annuelle
        )


        boutons = QHBoxLayout()


        annuler = QPushButton(
            "Annuler"
        )

        sauvegarder = QPushButton(
            "Sauvegarder"
        )

        sauvegarder.setDefault(
            True
        )

        sauvegarder.setAutoDefault(
            True
        )

        boutons.addWidget(
            annuler
        )

        boutons.addWidget(
            sauvegarder
        )


        layout.addLayout(
            boutons
        )


        annuler.clicked.connect(
            self.reject
        )

        sauvegarder.clicked.connect(
            self.accept
        )


        self.setLayout(
            layout
        )



class RetraiteEditDialog(RetraiteDialog):

    def __init__(
        self,
        retraite,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Modifier un calcul de retraite"
        )


        self.nom.setText(
            str(retraite[1] or "")
        )

        self.placement_actuel.setText(
            str(retraite[2] or "")
        )

        self.annees.setText(
            str(retraite[3] or "")
        )

        self.taux.setText(
            str(retraite[4] or "")
        )

        self.cotisation_annuelle.setText(
            str(retraite[5] or "")
        )
