import os
import sys
import shutil

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QFileDialog
)

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from database import reset_database, DATABASE_NAME
from pages.changer_mot_passe_dialog import ChangerMotDePasseDialog



def resource_path(
    relative_path
):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(
        base_path,
        relative_path
    )



class AProposPage(QWidget):

    def __init__(self):

        super().__init__()


        layout = QVBoxLayout()


        # =========================
        # LOGO
        # =========================

        logo = QLabel()

        pixmap = QPixmap(
            resource_path("assets/Logo.png")
        )

        if not pixmap.isNull():

            logo.setPixmap(
                pixmap.scaled(
                    160,
                    160,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        logo.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            logo
        )


        # =========================
        # TITRE
        # =========================

        titre = QLabel(
            "Mon bas de laine"
        )

        titre.setStyleSheet(
            "font-size:28px;font-weight:bold;"
        )

        titre.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            titre
        )

        version = QLabel(
            "version 1.3"
        )

        version.setStyleSheet(
            "font-size:15px;color:#777777;"
        )

        version.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            version
        )


        # =========================
        # INFOS
        # =========================

        info = QLabel(
            """
Projet personnel de gestion financière.

Fonctions actuelles :

• Entrées d'argent
• Sorties d'argent
• Placements (REER / CELI / Autre)
• Prêts
• Bourse et Crypto
• Hypothèques
• Assurances
• Taxes et impôts (travail autonome)
• Cumulatif (mise à jour v1.1)
• Mot de passe en NIP (4 chiffres)
• Calculatrices TVQ / TPS (mise à jour v1.3)
• Budget mensuel
• Tableau d'amortissement
• Calculateur de rendement
• Simulateur d'impôt (mise à jour v1.3)


Développé avec Python + PySide6 + SQLite.
            """
        )

        info.setStyleSheet(
            "font-size:16px;"
        )

        info.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            info
        )


        # =========================
        # IMPORT / EXPORT
        # =========================

        donnees = QHBoxLayout()


        exporter = QPushButton(
            "Exporter les données"
        )

        exporter.clicked.connect(
            self.exporter_donnees
        )


        importer = QPushButton(
            "Importer des données"
        )

        importer.clicked.connect(
            self.importer_donnees
        )


        donnees.addWidget(
            exporter
        )

        donnees.addWidget(
            importer
        )


        layout.addLayout(
            donnees
        )


        # =========================
        # MOT DE PASSE
        # =========================

        mot_de_passe = QPushButton(
            "Modifier le NIP"
        )

        mot_de_passe.clicked.connect(
            self.ouvrir_changement_mot_passe
        )

        layout.addWidget(
            mot_de_passe
        )


        # =========================
        # RESET
        # =========================

        reset = QPushButton(
            "Effacer toutes les données"
        )

        reset.clicked.connect(
            self.reset_application
        )

        layout.addWidget(
            reset
        )


        self.setLayout(
            layout
        )



    def exporter_donnees(
        self
    ):

        chemin, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter les données",
            "mon_bas_de_laine_sauvegarde.db",
            "Base de données (*.db)"
        )


        if not chemin:

            return


        try:

            shutil.copyfile(
                DATABASE_NAME,
                chemin
            )


            QMessageBox.information(
                self,
                "Export terminé",
                "Les données ont été exportées avec succès."
            )


        except Exception as erreur:

            QMessageBox.warning(
                self,
                "Erreur",
                f"Impossible d'exporter les données.\n\n{erreur}"
            )



    def importer_donnees(
        self
    ):

        chemin, _ = QFileDialog.getOpenFileName(
            self,
            "Importer des données",
            "",
            "Base de données (*.db)"
        )


        if not chemin:

            return


        confirmation = QMessageBox.question(
            self,
            "Importer",
            """
ATTENTION !

L'importation va remplacer toutes vos données actuelles.

Une copie de sécurité sera créée automatiquement.

Voulez-vous continuer ?
            """,
            QMessageBox.Yes |
            QMessageBox.No
        )


        if confirmation != QMessageBox.Yes:

            return


        try:

            if os.path.exists(DATABASE_NAME):

                shutil.copyfile(
                    DATABASE_NAME,
                    DATABASE_NAME + ".backup"
                )


            shutil.copyfile(
                chemin,
                DATABASE_NAME
            )


            QMessageBox.information(
                self,
                "Import terminé",
                "Les données ont été importées.\n\n"
                "Veuillez redémarrer le logiciel."
            )


        except Exception as erreur:

            QMessageBox.warning(
                self,
                "Erreur",
                f"Impossible d'importer les données.\n\n{erreur}"
            )



    def ouvrir_changement_mot_passe(
        self
    ):

        dialog = ChangerMotDePasseDialog(
            self
        )

        dialog.exec()



    def reset_application(
        self
    ):

        confirmation = QMessageBox.question(
            self,
            "Effacer les données",
            """
ATTENTION !

Cette action va supprimer toutes les données de l'application.

- Entrées
- Sorties
- Placements
- REER / CELI
- Prêts
- Bourse et Crypto
- Hypothèques
- Assurances
- Taxes et impôts
- Budget mensuel
- Tableaux d'amortissement
- Calculs de rendement

Le NIP sera réinitialisé à 1234.

Voulez-vous continuer ?
            """,
            QMessageBox.Yes |
            QMessageBox.No
        )


        if confirmation == QMessageBox.Yes:

            reset_database()

            QMessageBox.information(
                self,
                "Effacement terminé",
                "Toutes les données ont été effacées.\n\n"
                "Le NIP a été réinitialisé à 1234.\n\n"
                "Veuillez aller dans « À Propos » pour configurer un nouveau NIP."
            )
