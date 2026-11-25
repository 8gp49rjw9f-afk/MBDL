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
    QFrame,
    QAbstractItemView
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from database import get_connection

from pages.reer_celi_dialog import (
    ReerCeliDialog,
    ReerCeliEditDialog
)

from pages.separateur_dialog import SeparateurDialog



class ReerCeliPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        titre = QLabel("Cotisations REER/CELI")
        titre.setStyleSheet("font-size:28px;font-weight:bold;")
        layout.addWidget(titre)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Type", "Nom", "Montant", "Actions"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        layout.addWidget(self.table)

        boutons_ajout = QHBoxLayout()
        bouton = QPushButton("+ Ajouter une cotisation")
        bouton.clicked.connect(self.ouvrir_dialog)
        bouton_separateur = QPushButton("+ Ajouter un séparateur")
        bouton_separateur.clicked.connect(self.ouvrir_dialog_separateur)
        boutons_ajout.addWidget(bouton)
        boutons_ajout.addWidget(bouton_separateur)
        layout.addLayout(boutons_ajout)

        ligne = QFrame()
        ligne.setFrameShape(QFrame.HLine)
        layout.addWidget(ligne)

        droits_titre = QLabel("Droits de cotisation pour l'année courante")
        droits_titre.setStyleSheet("font-size:18px;font-weight:bold;")
        layout.addWidget(droits_titre)

        self.reer_maximum = self.creer_ligne("REER Cotisation maximum")
        self.celi_maximum = self.creer_ligne("CELI Cotisation maximum")
        layout.addLayout(self.reer_maximum)
        layout.addLayout(self.celi_maximum)

        self.reer_annee = QLabel()
        self.celi_annee = QLabel()
        self.reer_annee.setStyleSheet("font-size:16px;")
        self.celi_annee.setStyleSheet("font-size:16px;")
        layout.addWidget(self.reer_annee)
        layout.addWidget(self.celi_annee)

        self.setLayout(layout)

        self.table.blockSignals(True)
        self.table.cellChanged.connect(self.valeur_modifiee)
        self.table.blockSignals(False)

        self.charger()



    def creer_ligne(self, texte):
        ligne = QHBoxLayout()
        label = QLabel(texte)
        champ = QLineEdit()
        champ.setPlaceholderText("0.00")
        champ.textChanged.connect(self.sauvegarder_plafonds)
        ligne.addWidget(label)
        ligne.addWidget(champ)
        ligne.champ = champ
        return ligne



    def formater_montant(self, valeur):
        try:
            texte = f"{float(valeur):,.2f}".replace(",", " ").replace(".", ",")
            return texte + " $"
        except:
            return "0,00 $"



    def convertir(self, valeur):
        try:
            return float(str(valeur).replace(" ", "").replace(",", ".").replace("$", ""))
        except:
            return 0



    def valeur_modifiee(self, row, column):

        if column != 2:
            return

        item = self.table.item(row, column)
        if item is None:
            return

        nouvelle_valeur = self.convertir(item.text())

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM reer_celi ORDER BY position")
        lignes = cursor.fetchall()

        if row < len(lignes):
            cursor.execute(
                "UPDATE reer_celi SET montant = ? WHERE id = ?",
                (nouvelle_valeur, lignes[row][0])
            )
            conn.commit()

        conn.close()
        self.charger()



    def ouvrir_dialog(self):

        dialog = ReerCeliDialog()

        if dialog.exec():
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM reer_celi")
            position = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO reer_celi (type_ligne, nom, montant, position) VALUES (?, ?, ?, ?)",
                (dialog.type_ligne.currentText(), dialog.nom.text(), self.convertir(dialog.montant.text()), position)
            )
            conn.commit()
            conn.close()
            self.charger()



    def ouvrir_dialog_separateur(self):

        dialog = SeparateurDialog()

        if dialog.exec():
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM reer_celi")
            position = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO reer_celi (type_ligne, nom, montant, position, est_separateur) VALUES ('', ?, 0, ?, 1)",
                (dialog.nom.text(), position)
            )
            conn.commit()
            conn.close()
            self.charger()



    def charger(self):

        self.table.blockSignals(True)
        self.table.clearSpans()
        self.table.setRowCount(0)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, type_ligne, nom, montant, est_separateur FROM reer_celi ORDER BY position"
        )
        resultats = cursor.fetchall()
        conn.close()

        total_reer = 0
        total_celi = 0

        for identifiant, type_ligne, nom, montant, est_separateur in resultats:

            row = self.table.rowCount()
            self.table.insertRow(row)

            if est_separateur:
                self.table.setSpan(row, 0, 1, 3)
                item = QTableWidgetItem(nom)
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QColor(210, 210, 210))
                police = QFont()
                police.setBold(True)
                item.setFont(police)
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(row, 0, item)
                self.creer_actions(row, identifiant)
                self.table.setRowHeight(row, 22)
                continue

            montant = montant or 0
            if type_ligne == "REER":
                total_reer += montant
            elif type_ligne == "CELI":
                total_celi += montant

            # Type (non editable)
            item_type = QTableWidgetItem(type_ligne)
            item_type.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(row, 0, item_type)

            # Nom (non editable)
            item_nom = QTableWidgetItem(nom)
            item_nom.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(row, 1, item_nom)

            # Montant (editable)
            item_montant = QTableWidgetItem(self.formater_montant(montant))
            item_montant.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
            item_montant.setToolTip("Valeur modifiable directement")
            self.table.setItem(row, 2, item_montant)

            self.creer_actions(row, identifiant)

        self.total_reer = total_reer
        self.total_celi = total_celi

        self.table.blockSignals(False)
        self.charger_plafonds()



    def creer_actions(self, row, identifiant):

        actions = QWidget()
        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(0, 0, 0, 0)

        monter = QPushButton("↑")
        monter.setFixedWidth(25)
        monter.clicked.connect(lambda: self.monter(identifiant))

        descendre = QPushButton("↓")
        descendre.setFixedWidth(25)
        descendre.clicked.connect(lambda: self.descendre(identifiant))

        modifier = QPushButton("Edit")
        modifier.setFixedWidth(45)
        modifier.clicked.connect(lambda: self.modifier(identifiant))

        supprimer = QPushButton("X")
        supprimer.setFixedWidth(25)
        supprimer.clicked.connect(lambda: self.supprimer(identifiant))

        actions_layout.addWidget(monter)
        actions_layout.addWidget(descendre)
        actions_layout.addWidget(modifier)
        actions_layout.addWidget(supprimer)
        actions.setLayout(actions_layout)
        self.table.setCellWidget(row, 3, actions)



    def charger_plafonds(self):

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT reer_possible, celi_possible FROM plafonds WHERE id = 1")
        resultat = cursor.fetchone()
        conn.close()

        self.reer_maximum.champ.blockSignals(True)
        self.celi_maximum.champ.blockSignals(True)

        if resultat:
            self.reer_maximum.champ.setText(f"{resultat[0]:.2f}")
            self.celi_maximum.champ.setText(f"{resultat[1]:.2f}")

        self.reer_maximum.champ.blockSignals(False)
        self.celi_maximum.champ.blockSignals(False)

        self.afficher_totaux()



    def sauvegarder_plafonds(self):

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE plafonds SET reer_possible = ?, celi_possible = ? WHERE id = 1",
            (self.convertir(self.reer_maximum.champ.text()), self.convertir(self.celi_maximum.champ.text()))
        )
        conn.commit()
        conn.close()
        self.afficher_totaux()



    def afficher_totaux(self):

        reer_max = self.convertir(self.reer_maximum.champ.text())
        celi_max = self.convertir(self.celi_maximum.champ.text())

        vert = "font-size:16px;font-weight:bold;color:#1b7f2e;"
        rouge = "font-size:16px;font-weight:bold;color:#c02020;"

        self.reer_annee.setText(f"REER Total : {self.formater_montant(self.total_reer)}")
        self.reer_annee.setStyleSheet(rouge if self.total_reer > reer_max else vert)

        self.celi_annee.setText(f"CELI Total : {self.formater_montant(self.total_celi)}")
        self.celi_annee.setStyleSheet(rouge if self.total_celi > celi_max else vert)



    def monter(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT position FROM reer_celi WHERE id = ?", (identifiant,))
        actuel = cursor.fetchone()
        if actuel is None or actuel[0] <= 0:
            conn.close()
            return
        position = actuel[0]
        cursor.execute("UPDATE reer_celi SET position = position + 1 WHERE position = ?", (position - 1,))
        cursor.execute("UPDATE reer_celi SET position = ? WHERE id = ?", (position - 1, identifiant))
        conn.commit()
        conn.close()
        self.charger()



    def descendre(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT position FROM reer_celi WHERE id = ?", (identifiant,))
        actuel = cursor.fetchone()
        if actuel is None:
            conn.close()
            return
        position = actuel[0]
        cursor.execute("SELECT COUNT(*) FROM reer_celi")
        total = cursor.fetchone()[0]
        if position >= total - 1:
            conn.close()
            return
        cursor.execute("UPDATE reer_celi SET position = position - 1 WHERE position = ?", (position + 1,))
        cursor.execute("UPDATE reer_celi SET position = ? WHERE id = ?", (position + 1, identifiant))
        conn.commit()
        conn.close()
        self.charger()



    def modifier(self, identifiant):

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, type_ligne, nom, montant, est_separateur FROM reer_celi WHERE id = ?",
            (identifiant,)
        )
        resultat = cursor.fetchone()
        conn.close()

        if resultat is None:
            return

        if resultat[4]:
            dialog = SeparateurDialog(resultat[2])
            if dialog.exec():
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE reer_celi SET nom = ? WHERE id = ?", (dialog.nom.text(), identifiant))
                conn.commit()
                conn.close()
                self.charger()
            return

        dialog = ReerCeliEditDialog(resultat[1], resultat[2], resultat[3], self)
        if dialog.exec():
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE reer_celi SET type_ligne = ?, nom = ?, montant = ? WHERE id = ?",
                (dialog.type_ligne.currentText(), dialog.nom.text(), self.convertir(dialog.montant.text()), identifiant)
            )
            conn.commit()
            conn.close()
            self.charger()



    def supprimer(self, identifiant):

        confirmation = QMessageBox.question(self, "Suppression", "Supprimer cette ligne ?")
        if confirmation == QMessageBox.Yes:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reer_celi WHERE id = ?", (identifiant,))
            conn.commit()
            conn.close()
            self.reorganiser_positions()
            self.charger()



    def reorganiser_positions(self):

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM reer_celi ORDER BY position")
        lignes = cursor.fetchall()
        for index, ligne in enumerate(lignes):
            cursor.execute("UPDATE reer_celi SET position = ? WHERE id = ?", (index, ligne[0]))
        conn.commit()
        conn.close()
