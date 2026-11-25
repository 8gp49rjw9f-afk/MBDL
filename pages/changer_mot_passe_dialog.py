from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator

from database import get_connection


class CaseChiffre(QLineEdit):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(parent)

        self.setMaxLength(1)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(46, 54)
        self.setValidator(QIntValidator(0, 9, self))

        self.setStyleSheet(
            """
            QLineEdit {
                font-size: 24px;
                font-weight: bold;
                border: 2px solid #999999;
                border-radius: 6px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #2d7ff9;
            }
            """
        )


class ChangerMotDePasseDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(parent)

        self.setWindowTitle("Modifier le NIP")
        self.resize(400, 620)

        layout = QVBoxLayout()

        layout.setSpacing(10)

        titre = QLabel("Modifier le NIP")

        titre.setStyleSheet(
            "font-size:20px;font-weight:bold;"
        )

        layout.addWidget(titre)

        info = QLabel(
            "Le NIP est composé de 4 chiffres."
        )

        info.setStyleSheet(
            "color: #555555;"
        )

        layout.addWidget(info)


        # =========================
        # NIP ACTUEL
        # =========================

        layout.addWidget(QLabel("NIP actuel"))

        self.cases_actuel = self.creer_cases()

        layout.addLayout(
            self.rangee_cases(self.cases_actuel)
        )


        # =========================
        # NOUVEAU NIP
        # =========================

        layout.addWidget(QLabel("Nouveau NIP"))

        self.cases_nouveau = self.creer_cases()

        layout.addLayout(
            self.rangee_cases(self.cases_nouveau)
        )


        # =========================
        # CONFIRMATION
        # =========================

        layout.addWidget(QLabel("Confirmer le nouveau NIP"))

        self.cases_confirmation = self.creer_cases()

        layout.addLayout(
            self.rangee_cases(self.cases_confirmation)
        )


        # =========================
        # INDICES
        # =========================

        layout.addWidget(
            QLabel("Indice 1 (pour retrouver le NIP)")
        )

        self.indice1 = QLineEdit()

        layout.addWidget(self.indice1)


        layout.addWidget(
            QLabel("Indice 2 (pour retrouver le NIP)")
        )

        self.indice2 = QLineEdit()

        layout.addWidget(self.indice2)


        # Charger les indices existants

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT indice1, indice2

            FROM users

            WHERE id = 1
            """
        )

        res = cursor.fetchone()

        conn.close()

        if res:

            self.indice1.setText(
                str(res[0] or "")
            )

            self.indice2.setText(
                str(res[1] or "")
            )


        # =========================
        # BOUTONS
        # =========================

        boutons = QHBoxLayout()

        annuler = QPushButton("Annuler")
        confirmer = QPushButton("Confirmer")

        boutons.addWidget(annuler)
        boutons.addWidget(confirmer)

        layout.addLayout(boutons)

        annuler.clicked.connect(self.reject)
        confirmer.clicked.connect(self.confirmer_changement)

        self.setLayout(layout)

        self.cases_actuel[0].setFocus()


    # =========================
    # FABRICATION DES CASES
    # =========================

    def creer_cases(
        self
    ):

        cases = []

        for index in range(4):

            case = CaseChiffre()

            case.textChanged.connect(
                lambda texte, i=index, groupe=cases:
                self.case_remplie(groupe, i, texte)
            )

            case.returnPressed.connect(
                self.confirmer_changement
            )

            cases.append(case)

        return cases


    def rangee_cases(
        self,
        cases
    ):

        rangee = QHBoxLayout()

        rangee.setSpacing(8)

        for case in cases:

            rangee.addWidget(case)

        rangee.addStretch()

        return rangee


    # =========================
    # NAVIGATION ENTRE LES CASES
    # =========================

    def case_remplie(
        self,
        cases,
        index,
        texte
    ):

        if len(texte) > 1:

            # Collage : on repartit les chiffres
            chiffres = "".join(
                caractere
                for caractere in texte
                if caractere.isdigit()
            )[:4]

            for position, chiffre in enumerate(chiffres):

                cases[position].setText(chiffre)

            self.aller_a(cases, len(chiffres))

            return

        if texte and index < 3:

            cases[index + 1].setFocus()

            cases[index + 1].selectAll()


    def aller_a(
        self,
        cases,
        position
    ):

        if position > 3:

            position = 3

        cases[position].setFocus()

        cases[position].selectAll()


    # =========================
    # LECTURE D'UN NIP
    # =========================

    def lire_cases(
        self,
        cases
    ):

        return "".join(
            case.text()
            for case in cases
        )


    def vider_cases(
        self,
        cases
    ):

        for case in cases:

            case.clear()


    # =========================
    # CONFIRMATION
    # =========================

    def confirmer_changement(self):

        actuel = self.lire_cases(self.cases_actuel)
        nouveau = self.lire_cases(self.cases_nouveau)
        confirmation = self.lire_cases(self.cases_confirmation)

        if len(actuel) != 4 or len(nouveau) != 4:

            QMessageBox.warning(
                self,
                "Erreur",
                "Le NIP doit contenir exactement 4 chiffres."
            )

            return

        if nouveau != confirmation:

            QMessageBox.warning(
                self,
                "Erreur",
                "La confirmation ne correspond pas au nouveau NIP."
            )

            self.vider_cases(self.cases_confirmation)

            self.cases_confirmation[0].setFocus()

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

        nip_actuel = (
            resultat[0]
            if resultat
            else "1234"
        )

        if actuel != nip_actuel:

            conn.close()

            QMessageBox.warning(
                self,
                "Erreur",
                "NIP actuel incorrect."
            )

            self.vider_cases(self.cases_actuel)

            self.cases_actuel[0].setFocus()

            return

        cursor.execute(
            """
            UPDATE users

            SET password = ?,
                indice1 = ?,
                indice2 = ?

            WHERE id = 1
            """,
            (
                nouveau,
                self.indice1.text(),
                self.indice2.text()
            )
        )

        conn.commit()
        conn.close()

        QMessageBox.information(
            self,
            "Succès",
            "NIP modifié avec succès."
        )

        self.accept()
