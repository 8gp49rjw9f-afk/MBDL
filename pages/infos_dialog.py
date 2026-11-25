import os
import sys
import shutil

from PySide6.QtWidgets import (
    QDialog,
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



class InfosDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(parent)

        self.setWindowTitle(
            "Infos"
        )

        self.resize(
            560,
            560
        )


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
        # VERSION
        # =========================

        version = QLabel(
            "version 1.41"
        )

        version.setStyleSheet(
            "font-size:24px;font-weight:bold;"
        )

        version.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            version
        )


        # =========================
        # DESCRIPTION
        # =========================

        description = QLabel(
            "Projet personnel de gestion financière."
        )

        description.setStyleSheet(
            "font-size:16px;"
        )

        description.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            description
        )


        layout.addSpacing(
            16
        )


        # =========================
        # DERNIERES MISES A JOUR
        # =========================

        titre_mise_a_jour = QLabel(
            "Dernières mises à jour :"
        )

        titre_mise_a_jour.setStyleSheet(
            "font-size:17px;font-weight:bold;"
        )

        titre_mise_a_jour.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            titre_mise_a_jour
        )


        modifications = QLabel(
            """
• Modifications colonne des onglets
• Modifications fenêtre Login
• Modification du GUI
• Modification fenêtre « Infos »
• Ajout du Simulateur d'impôts
• Ajout du Patrimoine
            """
        )

        modifications.setStyleSheet(
            "font-size:16px;"
        )

        modifications.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            modifications
        )


        layout.addStretch(1)


        # =========================
        # BOUTON FERMER
        # =========================

        boutons = QHBoxLayout()

        boutons.addStretch(1)

        self.bouton_fermer = QPushButton(
            "Fermer"
        )

        self.bouton_fermer.setFixedWidth(120)

        self.bouton_fermer.clicked.connect(
            self.accept
        )

        boutons.addWidget(
            self.bouton_fermer
        )

        boutons.addStretch(1)

        layout.addLayout(
            boutons
        )


        self.setLayout(
            layout
        )



    # =========================
    # EXPORT
    # =========================

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



    # =========================
    # IMPORT
    # =========================

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



    # =========================
    # NIP
    # =========================

    def ouvrir_changement_mot_passe(
        self
    ):

        dialog = ChangerMotDePasseDialog(
            self
        )

        dialog.exec()



    # =========================
    # RESET
    # =========================

    def reset_application(
        self
    ):

        confirmation = QMessageBox.question(
            self,
            "Effacer les données",
            """
ATTENTION !

Cette action va supprimer TOUTES les données de l'application.

- Entrées
- Sorties
- Placements (REER / CELI / Autre)
- Historique des placements
- Prêts
- Bourse et Crypto
- Hypothèques
- Assurances et couvertures
- Taxes et impôts (travail autonome)
- Patrimoine
- Cumulatif (tous les résumés)
- Budgets mensuels
- Budgets prévisionnels
- Tableaux d'amortissement
- Calculs de rendement
- Simulateur d'impôt
- Plafonds REER / CELI
- Acomptes provisionnels

Le NIP sera réinitialisé à 1234 et les indices seront effacés.

La copie de sécurité (.backup) est conservée.

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
                "Veuillez aller dans « Infos » pour configurer un nouveau NIP."
            )
