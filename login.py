from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIntValidator

from database import get_connection, reset_database


# Duree de l'affichage vert ou rouge, en millisecondes
DUREE_COULEUR = 500


class CaseChiffre(QLineEdit):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(parent)

        self.setMaxLength(1)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(50, 60)
        self.setValidator(QIntValidator(0, 9, self))
        self.setEchoMode(QLineEdit.Password)

        self.appliquer_contour(
            "normal"
        )



    # =========================
    # CONTOUR SELON L'ETAT
    # =========================

    def appliquer_contour(
        self,
        etat
    ):

        if etat == "bon":

            bordure = "#1b7f2e"

        elif etat == "mauvais":

            bordure = "#c02020"

        else:

            bordure = "#999999"

        self.setStyleSheet(
            f"""
            QLineEdit {{
                font-size: 28px;
                font-weight: bold;
                border: 2px solid {bordure};
                border-radius: 6px;
                background-color: #ffffff;
            }}
            QLineEdit:focus {{
                border: 2px solid {bordure};
            }}
            """
        )



class LoginWindow(QWidget):

    def __init__(self, on_success):

        super().__init__()

        self.on_success = on_success

        self.setWindowTitle(
            "Mon bas de laine - Connexion"
        )

        self.resize(
            420,
            380
        )

        layout = QVBoxLayout()

        layout.setSpacing(
            14
        )


        # =========================
        # TITRE
        # =========================

        titre = QLabel(
            "Bienvenue dans Mon bas de laine"
        )

        titre.setStyleSheet(
            "font-size: 22px;"
        )

        titre.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            titre
        )


        # =========================
        # PIN - 4 CASES
        # =========================

        label_pin = QLabel(
            "Entrez votre NIP (4 chiffres)"
        )

        label_pin.setAlignment(
            Qt.AlignCenter
        )

        label_pin.setStyleSheet(
            "font-size: 15px; color: #555555;"
        )

        layout.addWidget(
            label_pin
        )


        zone_pin = QHBoxLayout()

        zone_pin.setSpacing(
            12
        )

        zone_pin.addStretch()

        self.cases = []

        for index in range(4):

            case = CaseChiffre()

            case.textChanged.connect(
                lambda texte, i=index:
                self.case_remplie(i, texte)
            )

            case.returnPressed.connect(
                self.verifier
            )

            zone_pin.addWidget(
                case
            )

            self.cases.append(
                case
            )

        zone_pin.addStretch()

        layout.addLayout(
            zone_pin
        )


        # =========================
        # BOUTON ENTRER
        # =========================

        bouton = QPushButton(
            "Entrer"
        )

        bouton.setStyleSheet(
            "font-size: 16px; padding: 8px;"
        )

        bouton.clicked.connect(
            self.verifier
        )

        layout.addWidget(
            bouton
        )


        # =========================
        # INDICES
        # =========================

        bouton_indices = QPushButton(
            "Indices"
        )

        bouton_indices.clicked.connect(
            self.afficher_indices
        )

        layout.addWidget(
            bouton_indices
        )


        # Ligne séparatrice
        ligne = QLabel("")

        ligne.setFixedHeight(
            10
        )

        layout.addWidget(
            ligne
        )


        # =========================
        # NOUVEAU PROJET
        # =========================

        bouton_nouveau = QPushButton(
            "Nouveau projet (effacer tout)"
        )

        bouton_nouveau.clicked.connect(
            self.nouveau_projet
        )

        layout.addWidget(
            bouton_nouveau
        )


        self.setLayout(
            layout
        )


        self.cases[0].setFocus()



    # =========================
    # PASSAGE AUTOMATIQUE
    # =========================

    def case_remplie(
        self,
        index,
        texte
    ):

        if texte and index < 3:

            self.cases[index + 1].setFocus()

            self.cases[index + 1].selectAll()


        if len(texte) == 1 and index == 3:

            self.verifier()



    # =========================
    # LECTURE DU PIN
    # =========================

    def lire_pin(
        self
    ):

        return "".join(
            case.text()
            for case in self.cases
        )



    # =========================
    # COULEUR DES CASES
    # =========================

    def colorer_cases(
        self,
        etat
    ):

        for case in self.cases:

            case.appliquer_contour(
                etat
            )


    def remettre_cases_normales(
        self
    ):

        self.colorer_cases(
            "normal"
        )



    # =========================
    # VERIFICATION
    # =========================

    def verifier(self):

        pin = self.lire_pin()

        if len(pin) < 4:

            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez entrer les 4 chiffres."
            )

            return

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT password

            FROM users

            WHERE id = 1
            """
        )

        resultat = cursor.fetchone()

        conn.close()

        pin_actuel = (
            resultat[0]
            if resultat
            else "1234"
        )

        if pin == pin_actuel:

            # Contour vert, puis ouverture de l'application
            self.colorer_cases(
                "bon"
            )

            QTimer.singleShot(
                DUREE_COULEUR,
                self.ouvrir_application
            )

        else:

            # Contour rouge, puis effacement du NIP
            self.colorer_cases(
                "mauvais"
            )

            QTimer.singleShot(
                DUREE_COULEUR,
                self.echec_connexion
            )



    # =========================
    # SUITE DU SUCCES
    # =========================

    def ouvrir_application(self):

        self.close()

        self.on_success()



    # =========================
    # SUITE DE L'ECHEC
    # =========================

    def echec_connexion(self):

        for case in self.cases:

            case.clear()

        self.remettre_cases_normales()

        self.cases[0].setFocus()

        QMessageBox.warning(
            self,
            "Erreur",
            "Mauvais NIP"
        )



    # =========================
    # INDICES
    # =========================

    def afficher_indices(self):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT indice1, indice2

            FROM users

            WHERE id = 1
            """
        )

        resultat = cursor.fetchone()

        conn.close()

        indice1 = ""
        indice2 = ""

        if resultat:

            indice1 = str(
                resultat[0] or ""
            )

            indice2 = str(
                resultat[1] or ""
            )

        QMessageBox.information(
            self,
            "Indices",
            f"Indice 1 : {indice1}\n\nIndice 2 : {indice2}"
        )



    # =========================
    # NOUVEAU PROJET
    # =========================

    def nouveau_projet(self):

        confirmation = QMessageBox.question(
            self,
            "Nouveau projet",
            """
ATTENTION !

Cette action va effacer TOUTES les données de l'application.

Le NIP sera réinitialisé à 1234.

Vous devrez aller dans « Infos » pour configurer un nouveau NIP.

Voulez-vous continuer ?
            """,
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmation != QMessageBox.Yes:

            return

        reset_database()

        QMessageBox.information(
            self,
            "Nouveau projet créé",
            "Toutes les données ont été effacées.\n\n"
            "Le NIP par défaut est 1234.\n\n"
            "Allez dans « Infos » pour configurer votre NIP."
        )

        for case in self.cases:

            case.clear()

        self.remettre_cases_normales()

        self.cases[0].setFocus()
