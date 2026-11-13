from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)



class AmortissementViewDialog(QDialog):

    def __init__(
        self,
        tableau,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Voir le tableau d'amortissement"
        )


        self.resize(
            900,
            650
        )


        layout = QVBoxLayout()


        titre = QLabel(
            f"Tableau d'amortissement - {tableau['nom']}"
        )

        titre.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(
            titre
        )


        resume = QLabel(
            (
                f"Montant financé : {self.formater_montant(tableau['montant_finance'])}\n"
                f"Paiement mensuel : {self.formater_montant(tableau['paiement_mensuel'])}\n"
                f"Intérêts totaux : {self.formater_montant(tableau['interets_totaux'])}\n"
                f"Total payé : {self.formater_montant(tableau['total_paye'])}\n"
                f"Nombre réel de mois : {tableau['nombre_mois_reel']}"
            )
        )

        resume.setStyleSheet(
            "font-size:16px;"
        )

        layout.addWidget(
            resume
        )


        self.table = QTableWidget()


        self.table.setColumnCount(
            5
        )


        self.table.setHorizontalHeaderLabels(
            [
                "Mois",
                "Paiement",
                "Intérêt",
                "Capital",
                "Solde restant"
            ]
        )


        header = self.table.horizontalHeader()


        for i in range(5):

            header.setSectionResizeMode(
                i,
                QHeaderView.Stretch
            )


        lignes = tableau["lignes"]


        self.table.setRowCount(
            len(lignes)
        )


        for row, ligne in enumerate(lignes):


            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(ligne["mois"])
                )
            )


            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    self.formater_montant(
                        ligne["paiement"]
                    )
                )
            )


            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    self.formater_montant(
                        ligne["interet"]
                    )
                )
            )


            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    self.formater_montant(
                        ligne["capital"]
                    )
                )
            )


            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    self.formater_montant(
                        ligne["solde"]
                    )
                )
            )


        layout.addWidget(
            self.table
        )


        self.setLayout(
            layout
        )



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
