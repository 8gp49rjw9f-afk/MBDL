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


class CasePin(QLineEdit):

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

        self.actuel = QLineEdit()

        self.actuel.setPlaceholderText("1234")
        self.actuel.setMaxLength(4)
        self.actuel.setEchoMode(QLineEdit.Password)
        self.actuel.setValidator(QIntValidator(0, 9, self))
        self.actuel.setFixedWidth(120)

        layout.addWidget(self.actuel)


        # =========================
        # NOUVEAU NIP
        # =========================

        layout.addWidget(QLabel("Nouveau NIP"))

        self.nouveau = QLineEdit()

        self.nouveau.setPlaceholderText("4 chiffres")
        self.nouveau.setMaxLength(4)
        self.nouveau.setEchoMode(QLineEdit.Password)
        self.nouveau.setValidator(QIntValidator(0, 9, self))
        self.nouveau.setFixedWidth(120)

        layout.addWidget(self.nouveau)


        # =========================
        # CONFIRMATION
        # =========================

        layout.addWidget(QLabel("Confirmer le nouveau NIP"))

        self.confirmation = QLineEdit()

        self.confirmation.setPlaceholderText("4 chiffres")
        self.confirmation.setMaxLength(4)
        self.confirmation.setEchoMode(QLineEdit.Password)
        self.confirmation.setValidator(QIntValidator(0, 9, self))
        self.confirmation.setFixedWidth(120)

        layout.addWidget(self.confirmation)


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


    def confirmer_changement(self):

        nouveau = self.nouveau.text().strip()
        confirmation = self.confirmation.text().strip()

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

        if self.actuel.text().strip() != nip_actuel:

            conn.close()

            QMessageBox.warning(
                self,
                "Erreur",
                "NIP actuel incorrect."
            )

            return

        if len(nouveau) != 4 or not nouveau.isdigit():

            conn.close()

            QMessageBox.warning(
                self,
                "Erreur",
                "Le nouveau NIP doit contenir exactement 4 chiffres."
            )

            return

        if nouveau != confirmation:

            conn.close()

            QMessageBox.warning(
                self,
                "Erreur",
                "La confirmation ne correspond pas au nouveau NIP."
            )

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
