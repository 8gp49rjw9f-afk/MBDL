from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QMessageBox,
    QFrame
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from pages import impot_donnees
from pages import impot_parametres
from pages.deductions_dialog import (
    DeductionsDialog,
    total_deductions
)


class ImpotPage(QWidget):

    def __init__(self):

        super().__init__()

        self.donnees = impot_donnees.charger()

        layout = QVBoxLayout()

        layout.setSpacing(10)

        # =========================
        # DEUX COLONNES
        # =========================

        colonnes = QHBoxLayout()

        colonnes.setSpacing(0)

        colonnes.addLayout(self.colonne_gauche(), 1)

        colonnes.addWidget(self.separateur_vertical())

        colonnes.addLayout(self.colonne_droite(), 1)

        layout.addLayout(colonnes, 1)

        layout.addStretch()

        # =========================
        # PALIERS D'IMPOSITION (en bas de page)
        # =========================

        layout.addWidget(self.bloc_paliers())

        self.setLayout(layout)

        self.afficher_source()

        self.afficher_paliers()

        self.charger_champs()

        self.calculer()

    # =========================
    # COLONNE DE GAUCHE
    # =========================

    def colonne_gauche(self):

        colonne = QVBoxLayout()

        colonne.setSpacing(12)

        colonne.setContentsMargins(0, 0, 24, 0)

        titre = QLabel("Simulateur d'impôt")

        titre.setStyleSheet(
            "font-size:28px;font-weight:bold;"
        )

        colonne.addWidget(titre)

        sous_titre = QLabel(
            "Estimation pour un résident célibataire du Québec."
        )

        sous_titre.setStyleSheet(
            "color:#555555;font-size:15px;"
        )

        colonne.addWidget(sous_titre)

        colonne.addSpacing(10)

        self.champs = {}

        definitions = [

            ("emploi", "Revenu d'emploi"),
            ("autonome", "Revenu d'un travail autonome"),
            ("impot_paye", "Impôt sur le revenu payé"),
            ("reer", "Cotisations au REER et au CELIAPP"),
            ("autres_revenus", "Autres revenus"),
            ("gains_capital", "Gains en capital"),
            ("impot_paye_qc", "Impôt sur le revenu payé (Québec)")

        ]

        for cle, libelle in definitions:

            ligne = QHBoxLayout()

            etiquette = QLabel(libelle)

            etiquette.setMinimumWidth(230)

            ligne.addWidget(etiquette)

            champ = QLineEdit()

            champ.setPlaceholderText("0")

            champ.setMinimumWidth(180)

            champ.setAlignment(Qt.AlignRight)

            champ.textChanged.connect(self.calculer)

            champ.textChanged.connect(self.sauvegarder_champs)

            champ.editingFinished.connect(self.sauvegarder_champs)

            ligne.addWidget(champ)

            ligne.addStretch()

            colonne.addLayout(ligne)

            self.champs[cle] = champ

        # =========================
        # LIGNE DES DEDUCTIONS
        # =========================

        ligne_deductions = QHBoxLayout()

        etiquette_ded = QLabel("Autres déductions")

        etiquette_ded.setMinimumWidth(230)

        ligne_deductions.addWidget(etiquette_ded)

        self.bouton_deductions = QPushButton("Voir")

        self.bouton_deductions.setFixedWidth(70)

        self.bouton_deductions.setCursor(Qt.PointingHandCursor)

        self.bouton_deductions.clicked.connect(
            self.ouvrir_deductions
        )

        ligne_deductions.addWidget(self.bouton_deductions)

        self.label_deductions = QLabel("0,00 $")

        self.label_deductions.setMinimumWidth(100)

        self.label_deductions.setAlignment(Qt.AlignRight)

        self.label_deductions.setStyleSheet(
            "color:#555555;"
        )

        ligne_deductions.addWidget(self.label_deductions)

        ligne_deductions.addStretch()

        colonne.addLayout(ligne_deductions)

        colonne.addSpacing(6)

        self.case_rrq = QCheckBox(
            "Cotiser au RRQ et au RQAP (travailleur autonome)"
        )

        self.case_rrq.setChecked(False)

        self.case_rrq.stateChanged.connect(self.calculer)

        self.case_rrq.stateChanged.connect(self.sauvegarder_champs)

        colonne.addWidget(self.case_rrq)

        colonne.addSpacing(10)

        self.bouton_effacer = QPushButton("Effacer toutes les informations")

        self.bouton_effacer.setCursor(Qt.PointingHandCursor)

        self.bouton_effacer.clicked.connect(self.effacer_tout)

        ligne_effacer = QHBoxLayout()

        ligne_effacer.addWidget(self.bouton_effacer)

        ligne_effacer.addStretch()

        colonne.addLayout(ligne_effacer)

        colonne.addStretch()

        return colonne

    # =========================
    # COLONNE DE DROITE
    # =========================

    def colonne_droite(self):

        colonne = QVBoxLayout()

        colonne.setSpacing(8)

        colonne.setContentsMargins(24, 0, 0, 0)

        titre = QLabel("Montant estimé")

        titre.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )

        colonne.addWidget(titre)

        self.montant_estime = QLabel("0 $")

        self.montant_estime.setStyleSheet(
            "font-size:42px;font-weight:bold;color:#333333;"
        )

        colonne.addWidget(self.montant_estime)

        self.legende_montant = QLabel("")

        self.legende_montant.setStyleSheet(
            "color:#555555;"
        )

        colonne.addWidget(self.legende_montant)

        colonne.addWidget(self.separateur_horizontal())

        self.resultats = {}

        for cle, libelle, gras in [

            ("revenu_total", "Revenu total", True),
            ("deductions", "Autres déductions", False),
            ("revenu_imposable", "Revenu imposable", False),
            ("impot_federal", "Impôt fédéral", False),
            ("impot_provincial", "Impôt provincial", False),
            ("cotisations", "Cotisations au RRQ et à l'AE", False),
            ("impot_total", "Impôt total", True),
            ("revenu_net", "Revenu net", True)

        ]:

            ligne = self.ligne_resultat(libelle, gras)

            colonne.addLayout(ligne)

            self.resultats[cle] = ligne.itemAt(
                ligne.count() - 1
            ).widget()

        colonne.addWidget(self.separateur_horizontal())

        self.taux_ligne = {}

        for cle, libelle in [

            ("taux_moyen", "Taux d'imposition moyen"),
            ("marginal_federal", "Taux marginal fédéral"),
            ("marginal_quebec", "Taux marginal Québec")

        ]:

            ligne = QHBoxLayout()

            etiquette = QLabel(libelle)

            etiquette.setStyleSheet("color:#555555;")

            ligne.addWidget(etiquette)

            ligne.addStretch()

            valeur = QLabel("0,00 %")

            valeur.setStyleSheet("color:#555555;")

            ligne.addWidget(valeur)

            colonne.addLayout(ligne)

            self.taux_ligne[cle] = valeur

        colonne.addStretch()

        return colonne

    # =========================
    # SÉPARATEURS
    # =========================

    def separateur_vertical(self):

        ligne = QFrame()

        ligne.setFrameShape(QFrame.VLine)

        ligne.setFrameShadow(QFrame.Sunken)

        ligne.setStyleSheet("color:#cccccc;")

        return ligne


    def separateur_horizontal(self):

        ligne = QFrame()

        ligne.setFrameShape(QFrame.HLine)

        ligne.setFrameShadow(QFrame.Sunken)

        ligne.setStyleSheet("color:#dddddd;")

        return ligne

    # =========================
    # LIGNES DE RÉSULTAT
    # =========================

    def ligne_resultat(self, libelle, gras=False):

        ligne = QHBoxLayout()

        etiquette = QLabel(libelle)

        if gras:

            police = QFont()

            police.setBold(True)

            etiquette.setFont(police)

        ligne.addWidget(etiquette)

        ligne.addStretch()

        valeur = QLabel("0 $")

        if gras:

            police = QFont()

            police.setBold(True)

            valeur.setFont(police)

        ligne.addWidget(valeur)

        return ligne

    # =========================
    # BLOC DES PALIERS
    # =========================

    def bloc_paliers(self):

        groupe = QFrame()

        groupe.setObjectName("cadrePaliers")

        groupe.setStyleSheet(
            """
            QFrame#cadrePaliers {
                border: 1px solid #dddddd;
                border-radius: 8px;
            }
            """
        )

        interieur = QVBoxLayout(groupe)

        interieur.setContentsMargins(20, 14, 20, 16)

        interieur.setSpacing(6)


        # --- Deux boutons : annee courante et annee precedente ---

        from datetime import datetime as _dt

        annee_courante = _dt.now().year

        ligne_boutons = QHBoxLayout()

        ligne_boutons.setSpacing(10)

        self.bouton_annee_courante = QPushButton(
            f"Utiliser paliers {annee_courante}"
        )

        self.bouton_annee_courante.clicked.connect(
            lambda checked=False:
            self.mettre_a_jour(annee_courante)
        )

        ligne_boutons.addWidget(self.bouton_annee_courante)

        self.bouton_annee_passee = QPushButton(
            f"Utiliser paliers {annee_courante - 1}"
        )

        self.bouton_annee_passee.clicked.connect(
            lambda checked=False:
            self.mettre_a_jour(annee_courante - 1)
        )

        ligne_boutons.addWidget(self.bouton_annee_passee)

        ligne_boutons.addStretch()

        interieur.addLayout(ligne_boutons)

        interieur.addSpacing(8)


        # --- En-tete ---

        self.label_paliers = QLabel("")

        self.label_paliers.setStyleSheet(
            "font-weight:bold;font-size:15px;"
        )

        interieur.addWidget(self.label_paliers)

        self.label_paliers_detail = QLabel("")

        self.label_paliers_detail.setStyleSheet(
            "color:#777777;font-size:13px;"
        )

        interieur.addWidget(self.label_paliers_detail)

        interieur.addSpacing(8)


        # --- Tableau : deux blocs separes par une ligne verticale ---

        self.zone_paliers = QVBoxLayout()

        self.zone_paliers.setContentsMargins(0, 0, 0, 0)

        self.conteneur_paliers = None

        interieur.addLayout(self.zone_paliers)

        return groupe



    # =========================
    # AFFICHAGE DES PALIERS
    # =========================

    def afficher_paliers(self):

        annee = self.donnees.get("annee", "")

        self.label_paliers.setText(f"Paliers d'imposition {annee}")

        brut = self.donnees.get("date_telechargement")

        if brut:

            try:

                from datetime import datetime as _dt

                moment = _dt.fromisoformat(brut).strftime("%Y-%m-%d à %H:%M")

            except Exception:

                moment = str(brut)

            self.label_paliers_detail.setText(f"Téléchargés le {moment}")

        else:

            self.label_paliers_detail.setText("Paliers intégrés au programme")

        # --- Retirer l'ancien tableau ---

        if self.conteneur_paliers is not None:

            self.zone_paliers.removeWidget(self.conteneur_paliers)

            self.conteneur_paliers.deleteLater()

        # --- Nouveau tableau ---

        self.conteneur_paliers = QWidget()

        grille = QGridLayout(self.conteneur_paliers)

        grille.setContentsMargins(0, 0, 0, 0)
        grille.setHorizontalSpacing(18)
        grille.setVerticalSpacing(5)

        style_titre = "font-weight:bold;color:#333333;font-size:13px;"
        style_ligne = "color:#444444;font-size:13px;"

        for colonne, titre, alignement in [
            (0, "Fédéral", Qt.AlignLeft),
            (1, "Taux", Qt.AlignRight),
            (3, "Québec", Qt.AlignLeft),
            (4, "Taux", Qt.AlignRight)
        ]:

            etiquette = QLabel(titre)

            etiquette.setStyleSheet(style_titre)

            etiquette.setAlignment(alignement | Qt.AlignVCenter)

            grille.addWidget(etiquette, 0, colonne)

        nombre_lignes = 1

        for colonne, cle in [(0, "federal"), (3, "quebec")]:

            paliers = self.donnees.get(cle, {}).get("paliers", [])

            precedent = 0

            for numero, palier in enumerate(paliers):

                limite = palier.get("limite")

                if limite is None:

                    tranche = f"Plus de {precedent:,.0f} $"

                elif precedent == 0:

                    tranche = f"{limite:,.0f} $ ou moins"

                else:

                    tranche = f"{precedent:,.0f} $ à {limite:,.0f} $"

                if limite is not None:

                    precedent = limite

                gauche = QLabel(tranche.replace(",", " "))

                gauche.setStyleSheet(style_ligne)

                taux = f"{float(palier['taux']):g} %".replace(".", ",")

                droite = QLabel(taux)

                droite.setStyleSheet(style_ligne)

                droite.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

                grille.addWidget(gauche, numero + 1, colonne)

                grille.addWidget(droite, numero + 1, colonne + 1)

                nombre_lignes = max(nombre_lignes, numero + 2)

        ligne = QFrame()

        ligne.setFrameShape(QFrame.VLine)

        ligne.setStyleSheet("color:#bbbbbb;")

        grille.addWidget(ligne, 0, 2, nombre_lignes, 1)

        grille.setColumnStretch(0, 4)
        grille.setColumnMinimumWidth(1, 70)
        grille.setColumnStretch(3, 4)
        grille.setColumnMinimumWidth(4, 70)

        self.zone_paliers.addWidget(self.conteneur_paliers)

    # =========================
    # SOURCE
    # =========================

    def afficher_source(self):

        self.label_source = None

    # =========================
    # CONVERSIONS
    # =========================

    def convertir(self, valeur):

        try:

            return float(
                str(valeur)
                .replace(" ", "")
                .replace(",", ".")
                .replace("$", "")
                .replace("%", "")
            )

        except Exception:

            return 0.0


    def formater(self, valeur):

        try:

            texte = (
                f"{float(valeur):,.2f}"
                .replace(",", " ")
                .replace(".", ",")
            )

            return texte + " $"

        except Exception:

            return "0,00 $"


    def formater_taux(self, valeur):

        try:

            texte = (
                f"{float(valeur):,.2f}"
                .replace(",", " ")
                .replace(".", ",")
            )

            return texte + " %"

        except Exception:

            return "0,00 %"

    # =========================
    # DEDUCTIONS
    # =========================

    def ouvrir_deductions(self):

        dialog = DeductionsDialog(self)

        dialog.exec()

        self.afficher_deductions()

        self.calculer()


    def afficher_deductions(self):

        self.label_deductions.setText(
            self.formater(total_deductions())
        )

    # =========================
    # CALCUL
    # =========================

    def calculer(self):

        emploi = self.convertir(self.champs["emploi"].text())

        autonome = self.convertir(self.champs["autonome"].text())

        autres = self.convertir(self.champs["autres_revenus"].text())

        gains = self.convertir(self.champs["gains_capital"].text())

        reer = self.convertir(self.champs["reer"].text())

        impot_paye = self.convertir(self.champs["impot_paye"].text())

        impot_paye_qc = self.convertir(
            self.champs["impot_paye_qc"].text()
        )

        deductions = total_deductions()

        gains_imposables = gains * 0.5

        revenu_total = emploi + autonome + autres + gains_imposables

        revenu_imposable = max(0.0, revenu_total - reer)

        resultat = impot_donnees.calculer(
            revenu_imposable,
            autonome=self.case_rrq.isChecked(),
            autres_deductions=deductions,
            donnees=self.donnees
        )

        impot_federal = resultat["impot_federal"]
        impot_provincial = resultat["impot_quebec"]
        cotisations = resultat["cotisations"]
        impot_total = resultat["impot_total"]

        deja_paye = impot_paye + impot_paye_qc

        reste = deja_paye - impot_total - cotisations

        revenu_net = revenu_total - impot_total - cotisations

        # --- Montant estimé ---

        self.montant_estime.setText(
            self.formater(abs(reste))
        )

        if reste > 0.005:

            self.montant_estime.setStyleSheet(
                "font-size:42px;font-weight:bold;color:#1b7f2e;"
            )

            self.legende_montant.setText(
                "Remboursement estimé"
            )

        elif reste < -0.005:

            self.montant_estime.setStyleSheet(
                "font-size:42px;font-weight:bold;color:#c02020;"
            )

            self.legende_montant.setText(
                "Solde à payer estimé"
            )

        else:

            self.montant_estime.setStyleSheet(
                "font-size:42px;font-weight:bold;color:#333333;"
            )

            self.legende_montant.setText(
                "Équilibre"
            )

        # --- Résultats ---

        self.resultats["revenu_total"].setText(
            self.formater(revenu_total)
        )

        self.resultats["deductions"].setText(
            self.formater(deductions)
        )

        self.resultats["revenu_imposable"].setText(
            self.formater(resultat["revenu_imposable"])
        )

        self.resultats["impot_federal"].setText(
            self.formater(impot_federal)
        )

        self.resultats["impot_provincial"].setText(
            self.formater(impot_provincial)
        )

        self.resultats["cotisations"].setText(
            self.formater(cotisations)
        )

        self.resultats["impot_total"].setText(
            self.formater(impot_total)
        )

        self.resultats["revenu_net"].setText(
            self.formater(revenu_net)
        )

        # --- Taux ---

        self.taux_ligne["taux_moyen"].setText(
            self.formater_taux(resultat["taux_moyen"])
        )

        self.taux_ligne["marginal_federal"].setText(
            self.formater_taux(resultat["taux_marginal_federal"])
        )

        self.taux_ligne["marginal_quebec"].setText(
            self.formater_taux(resultat["taux_marginal_quebec"])
        )

    # =========================
    # SAUVEGARDE DES CHAMPS
    # =========================

    def sauvegarder_champs(self):

        champs = {}

        for cle, champ in self.champs.items():

            champs[cle] = champ.text()

        impot_parametres.sauvegarder(
            champs,
            self.case_rrq.isChecked()
        )



    def charger_champs(self):

        champs, case_rrq = impot_parametres.charger()

        for cle, champ in self.champs.items():

            if cle in champs:

                champ.blockSignals(True)

                champ.setText(
                    str(champs[cle])
                )

                champ.blockSignals(False)

        self.case_rrq.blockSignals(True)

        self.case_rrq.setChecked(case_rrq)

        self.case_rrq.blockSignals(False)

        self.afficher_deductions()

    # =========================
    # EFFACER
    # =========================

    def effacer_tout(self):

        confirmation = QMessageBox.question(
            self,
            "Effacer",
            "Effacer toutes les informations du simulateur ?"
        )

        if confirmation != QMessageBox.Yes:

            return

        for champ in self.champs.values():

            champ.blockSignals(True)

            champ.clear()

            champ.blockSignals(False)

        self.case_rrq.blockSignals(True)

        self.case_rrq.setChecked(False)

        self.case_rrq.blockSignals(False)

        impot_parametres.effacer()

        self.calculer()

    # =========================
    # MISE A JOUR DES PALIERS
    # =========================

    def mettre_a_jour(self, annee):

        if impot_donnees.est_telechargee(annee):

            confirmation = QMessageBox.question(
                self,
                "Paliers déjà téléchargés",
                f"Les paliers {annee} sont déjà enregistrés.\n\n"
                "Voulez-vous les télécharger de nouveau ?"
            )

            if confirmation != QMessageBox.Yes:

                return

        succes, message, donnees = impot_donnees.telecharger(annee)

        if succes:

            self.donnees = donnees

            impot_donnees.sauvegarder(donnees)

            self.afficher_paliers()

            self.calculer()

            QMessageBox.information(
                self,
                "Paliers mis à jour",
                f"Les paliers d'imposition {annee} ont été enregistrés."
            )

            return

        QMessageBox.warning(
            self,
            "Téléchargement impossible",
            message + "\n\n"
            "Les valeurs intégrées au programme sont utilisées."
        )
