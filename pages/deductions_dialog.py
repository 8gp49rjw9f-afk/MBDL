from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QAbstractItemView
)


from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from database import get_connection


# =========================================
# LECTURE DU TOTAL
# =========================================

def total_deductions():

    """
    Retourne la somme des deductions enregistrees.
    Utilisee par la page Simulateur d'impot.
    """

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            "SELECT SUM(montant) FROM deductions_impot"
        )

        resultat = cursor.fetchone()

        conn.close()

        return float(resultat[0] or 0.0)

    except Exception:

        return 0.0



class DeductionDialog(QDialog):

    def __init__(
        self,
        nom="",
        montant="",
        parent=None
    ):

        super().__init__(parent)

        self.setWindowTitle("Déduction")
        self.resize(400, 240)

        layout = QVBoxLayout()

        titre = QLabel("Déduction")
        titre.setStyleSheet("font-size:20px;font-weight:bold;")
        layout.addWidget(titre)

        layout.addWidget(QLabel("Nom"))
        self.nom = QLineEdit()
        self.nom.setText(str(nom or ""))
        self.nom.setPlaceholderText("Ex: Frais de garde")
        layout.addWidget(self.nom)

        layout.addWidget(QLabel("Montant"))
        self.montant = QLineEdit()
        self.montant.setText(str(montant or ""))
        self.montant.setPlaceholderText("0.00")
        layout.addWidget(self.montant)

        boutons = QHBoxLayout()

        annuler = QPushButton("Annuler")
        sauvegarder = QPushButton("Sauvegarder")

        sauvegarder.setDefault(
            True
        )

        sauvegarder.setAutoDefault(
            True
        )

        boutons.addWidget(annuler)
        boutons.addWidget(sauvegarder)
        layout.addLayout(boutons)

        annuler.clicked.connect(self.reject)
        sauvegarder.clicked.connect(self.accept)

        self.setLayout(layout)



class DeductionsDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Déductions")
        self.resize(700, 480)

        self.total = 0.0

        layout = QVBoxLayout()

        titre = QLabel("Déductions")
        titre.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(titre)

        info = QLabel(
            "Ajoutez vos dépenses déductibles. "
            "Le total est reporté automatiquement dans le simulateur."
        )
        info.setStyleSheet("color:#555555;font-size:14px;")
        layout.addWidget(info)

        # =========================
        # TABLEAU
        # =========================

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(
            ["Nom", "Montant ✎", "Actions"]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        layout.addWidget(self.table)

        # =========================
        # BOUTON AJOUT
        # =========================

        ligne_ajout = QHBoxLayout()

        bouton_ajout = QPushButton("+ Ajouter une déduction")
        bouton_ajout.clicked.connect(self.ouvrir_dialog)

        ligne_ajout.addWidget(bouton_ajout)
        ligne_ajout.addStretch()

        layout.addLayout(ligne_ajout)

        # =========================
        # TOTAL
        # =========================

        self.label_total = QLabel("Total des déductions : 0,00 $")
        self.label_total.setStyleSheet("font-size:18px;font-weight:bold;")
        layout.addWidget(self.label_total)

        layout.addStretch()

        # =========================
        # FERMER
        # =========================

        ligne_fermer = QHBoxLayout()
        ligne_fermer.addStretch()

        bouton_fermer = QPushButton("Fermer")
        bouton_fermer.setFixedWidth(120)
        bouton_fermer.clicked.connect(self.accept)

        ligne_fermer.addWidget(bouton_fermer)
        ligne_fermer.addStretch()

        layout.addLayout(ligne_fermer)

        self.setLayout(layout)

        self.table.cellChanged.connect(self.valeur_modifiee)

        self.charger()



    # =========================
    # FORMAT
    # =========================

    def formater_montant(self, valeur):

        try:

            texte = (
                f"{float(valeur):,.2f}"
                .replace(",", " ")
                .replace(".", ",")
            )

            return texte + " $"

        except Exception:

            return "0,00 $"



    def convertir(self, valeur):

        try:

            return float(
                str(valeur)
                .replace(" ", "")
                .replace(",", ".")
                .replace("$", "")
            )

        except Exception:

            return 0.0



    # =========================
    # CHARGEMENT
    # =========================

    def charger(self):

        self.table.blockSignals(True)

        self.table.setRowCount(0)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, nom, montant
            FROM deductions_impot
            ORDER BY position
            """
        )

        resultats = cursor.fetchall()

        conn.close()

        total = 0.0

        for identifiant, nom, montant in resultats:

            row = self.table.rowCount()
            self.table.insertRow(row)

            montant = montant or 0
            total += montant

            item_nom = QTableWidgetItem(str(nom or ""))
            item_nom.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(row, 0, item_nom)

            item_montant = QTableWidgetItem(
                self.formater_montant(montant)
            )
            item_montant.setFlags(
                Qt.ItemIsEnabled | Qt.ItemIsEditable
            )
            item_montant.setToolTip("Valeur modifiable directement")
            self.table.setItem(row, 1, item_montant)

            self.creer_actions(row, identifiant)

        self.table.blockSignals(False)

        self.total = total

        self.label_total.setText(
            "Total des déductions : " + self.formater_montant(total)
        )



    # =========================
    # ACTIONS
    # =========================

    def creer_actions(self, row, identifiant):

        actions = QWidget()
        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(0, 0, 0, 0)

        monter = QPushButton("↑")
        monter.setFixedWidth(25)
        monter.clicked.connect(
            lambda checked=False:
            self.monter(identifiant)
        )

        descendre = QPushButton("↓")
        descendre.setFixedWidth(25)
        descendre.clicked.connect(
            lambda checked=False:
            self.descendre(identifiant)
        )

        modifier = QPushButton("Edit")
        modifier.setFixedWidth(45)
        modifier.clicked.connect(
            lambda checked=False:
            self.modifier(identifiant)
        )

        supprimer = QPushButton("X")
        supprimer.setFixedWidth(25)
        supprimer.clicked.connect(
            lambda checked=False:
            self.supprimer(identifiant)
        )

        actions_layout.addWidget(monter)
        actions_layout.addWidget(descendre)
        actions_layout.addWidget(modifier)
        actions_layout.addWidget(supprimer)

        actions.setLayout(actions_layout)

        self.table.setCellWidget(row, 2, actions)



    # =========================
    # MODIFICATION DIRECTE DU MONTANT
    # =========================

    def valeur_modifiee(self, row, column):

        if column != 1:
            return

        item = self.table.item(row, column)

        if item is None:
            return

        nouvelle_valeur = self.convertir(item.text())

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM deductions_impot ORDER BY position"
        )

        lignes = cursor.fetchall()

        if row < len(lignes):

            cursor.execute(
                "UPDATE deductions_impot SET montant = ? WHERE id = ?",
                (nouvelle_valeur, lignes[row][0])
            )

            conn.commit()

        conn.close()

        self.charger()



    # =========================
    # AJOUT
    # =========================

    def ouvrir_dialog(self):

        dialog = DeductionDialog()

        if dialog.exec():

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT COUNT(*) FROM deductions_impot"
            )

            position = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO deductions_impot
                (nom, montant, position)
                VALUES (?, ?, ?)
                """,
                (
                    dialog.nom.text(),
                    self.convertir(dialog.montant.text()),
                    position
                )
            )

            conn.commit()
            conn.close()

            self.charger()



    # =========================
    # MODIFIER
    # =========================

    def modifier(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT nom, montant FROM deductions_impot WHERE id = ?",
            (identifiant,)
        )

        resultat = cursor.fetchone()

        conn.close()

        if resultat is None:
            return

        dialog = DeductionDialog(
            resultat[0],
            resultat[1],
            self
        )

        if dialog.exec():

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE deductions_impot
                SET nom = ?, montant = ?
                WHERE id = ?
                """,
                (
                    dialog.nom.text(),
                    self.convertir(dialog.montant.text()),
                    identifiant
                )
            )

            conn.commit()
            conn.close()

            self.charger()



    # =========================
    # SUPPRIMER
    # =========================

    def supprimer(self, identifiant):

        confirmation = QMessageBox.question(
            self,
            "Suppression",
            "Supprimer cette déduction ?"
        )

        if confirmation == QMessageBox.Yes:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM deductions_impot WHERE id = ?",
                (identifiant,)
            )

            conn.commit()
            conn.close()

            self.reorganiser_positions()
            self.charger()



    # =========================
    # ORDRE
    # =========================

    def monter(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT position FROM deductions_impot WHERE id = ?",
            (identifiant,)
        )

        actuel = cursor.fetchone()

        if actuel is None or actuel[0] <= 0:

            conn.close()
            return

        position = actuel[0]

        cursor.execute(
            """
            UPDATE deductions_impot
            SET position = position + 1
            WHERE position = ?
            """,
            (position - 1,)
        )

        cursor.execute(
            "UPDATE deductions_impot SET position = ? WHERE id = ?",
            (position - 1, identifiant)
        )

        conn.commit()
        conn.close()

        self.charger()



    def descendre(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT position FROM deductions_impot WHERE id = ?",
            (identifiant,)
        )

        actuel = cursor.fetchone()

        if actuel is None:

            conn.close()
            return

        position = actuel[0]

        cursor.execute("SELECT COUNT(*) FROM deductions_impot")
        total = cursor.fetchone()[0]

        if position >= total - 1:

            conn.close()
            return

        cursor.execute(
            """
            UPDATE deductions_impot
            SET position = position - 1
            WHERE position = ?
            """,
            (position + 1,)
        )

        cursor.execute(
            "UPDATE deductions_impot SET position = ? WHERE id = ?",
            (position + 1, identifiant)
        )

        conn.commit()
        conn.close()

        self.charger()



    def reorganiser_positions(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM deductions_impot ORDER BY position"
        )

        lignes = cursor.fetchall()

        for index, ligne in enumerate(lignes):

            cursor.execute(
                "UPDATE deductions_impot SET position = ? WHERE id = ?",
                (index, ligne[0])
            )

        conn.commit()
        conn.close()
