import os
import sqlite3


# Chemin stable pour la base de donnees (dossier Documents de l'utilisateur)
DOSSIER_DONNEES = os.path.join(
    os.path.expanduser("~"),
    "Documents",
    "Mon bas de laine"
)


# Creer le dossier s'il n'existe pas
if not os.path.exists(
    DOSSIER_DONNEES
):

    try:

        os.makedirs(
            DOSSIER_DONNEES
        )

    except OSError:

        pass


DATABASE_NAME = os.path.join(
    DOSSIER_DONNEES,
    "mon_financier.db"
)


def get_connection():

    return sqlite3.connect(
        DATABASE_NAME
    )


def create_database():

    conn = get_connection()

    cursor = conn.cursor()



    # =========================
    # UTILISATEUR UNIQUE
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT NOT NULL,

            password TEXT NOT NULL

        )
        """
    )


    cursor.execute(
        """
        INSERT OR IGNORE INTO users

        (
        id,
        username,
        password
        )

        VALUES

        (
        1,
        'admin',
        '1234'
        )

        """
    )



    # =========================
    # ENTREES ARGENT
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS entrees_argent (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nom TEXT NOT NULL,

            montant REAL NOT NULL DEFAULT 0,

            position INTEGER NOT NULL DEFAULT 0,

            est_separateur INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # SORTIES ARGENT
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sorties_argent (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nom TEXT NOT NULL,

            montant REAL NOT NULL DEFAULT 0,

            position INTEGER NOT NULL DEFAULT 0,

            est_separateur INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # PLACEMENTS (REER / CELI / AUTRE)
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS placements (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            type_ligne TEXT DEFAULT 'Autre',

            date_inscription TEXT,

            date_fin TEXT,

            institution TEXT,

            nom TEXT,

            montant_initial REAL NOT NULL DEFAULT 0,

            valeur_actuelle REAL NOT NULL DEFAULT 0,

            maximum REAL NOT NULL DEFAULT 0,

            position INTEGER NOT NULL DEFAULT 0,

            est_separateur INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # PLAFONDS REER / CELI
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS plafonds (

            id INTEGER PRIMARY KEY,

            reer_possible REAL NOT NULL DEFAULT 0,

            celi_possible REAL NOT NULL DEFAULT 0

        )
        """
    )


    cursor.execute(
        """
        INSERT OR IGNORE INTO plafonds

        (
        id,
        reer_possible,
        celi_possible
        )

        VALUES

        (
        1,
        0,
        0
        )

        """
    )



    # =========================
    # PRETS
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prets (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            institution TEXT,

            nom TEXT,

            date_debut TEXT,

            date_fin TEXT,

            paiement_mensuel REAL DEFAULT 0,

            montant_initial REAL DEFAULT 0,

            solde_actuel REAL DEFAULT 0,

            taux REAL DEFAULT 0,

            mois INTEGER NOT NULL DEFAULT 0,

            position INTEGER DEFAULT 0,

            est_separateur INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # HYPOTHEQUES
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS hypotheques (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nom TEXT,

            institution TEXT,

            valeur_propriete REAL NOT NULL DEFAULT 0,

            montant_initial REAL NOT NULL DEFAULT 0,

            montant_paye REAL NOT NULL DEFAULT 0,

            taux REAL NOT NULL DEFAULT 0,

            mois INTEGER NOT NULL DEFAULT 0,

            position INTEGER NOT NULL DEFAULT 0,

            est_separateur INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # BOURSE
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bourse (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            date_achat TEXT,

            institution TEXT,

            nom TEXT,

            symbole TEXT,

            nombre_actions REAL NOT NULL DEFAULT 0,

            prix_achat REAL NOT NULL DEFAULT 0,

            prix_actuel REAL NOT NULL DEFAULT 0,

            valeur_actuelle REAL NOT NULL DEFAULT 0,

            position INTEGER NOT NULL DEFAULT 0,

            est_separateur INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # REER / CELI (ancienne table, conservée)
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reer_celi (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            type_ligne TEXT,

            nom TEXT,

            montant REAL NOT NULL DEFAULT 0,

            position INTEGER NOT NULL DEFAULT 0,

            est_separateur INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # ASSURANCES
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS assurances (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            compagnie TEXT,

            nom TEXT,

            type_assurance TEXT,

            prime REAL NOT NULL DEFAULT 0,

            position INTEGER NOT NULL DEFAULT 0,

            est_separateur INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # COUVERTURES
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS couvertures (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            assurance_id INTEGER,

            nom TEXT,

            type_montant TEXT DEFAULT "Prix ($)",

            montant_assure REAL NOT NULL DEFAULT 0,

            prime REAL NOT NULL DEFAULT 0,

            franchise REAL NOT NULL DEFAULT 0,

            autres_infos TEXT,

            position INTEGER NOT NULL DEFAULT 0,

            FOREIGN KEY (assurance_id)

            REFERENCES assurances(id)

        )
        """
    )



    # =========================
    # BUDGETS
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS budgets (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nom TEXT,

            position INTEGER NOT NULL DEFAULT 0,

            est_separateur INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # BUDGET LIGNES
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS budget_lignes (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            budget_id INTEGER,

            nom TEXT,

            prix REAL NOT NULL DEFAULT 0,

            autres_infos TEXT,

            position INTEGER NOT NULL DEFAULT 0,

            FOREIGN KEY (budget_id)

            REFERENCES budgets(id)

        )
        """
    )



    # =========================
    # PATRIMOINE
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS patrimoine (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nom TEXT NOT NULL,

            montant REAL NOT NULL DEFAULT 0,

            position INTEGER NOT NULL DEFAULT 0,

            est_separateur INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # CUMULATIFS
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cumulatifs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nom TEXT,

            entrees INTEGER NOT NULL DEFAULT 0,

            sorties INTEGER NOT NULL DEFAULT 0,

            taxes_provinciales INTEGER NOT NULL DEFAULT 0,

            taxes_federales INTEGER NOT NULL DEFAULT 0,

            impots INTEGER NOT NULL DEFAULT 0,

            prets INTEGER NOT NULL DEFAULT 0,

            hypotheques INTEGER NOT NULL DEFAULT 0,

            placements INTEGER NOT NULL DEFAULT 0,

            reer INTEGER NOT NULL DEFAULT 0,

            celi INTEGER NOT NULL DEFAULT 0,

            patrimoine INTEGER NOT NULL DEFAULT 0,

            position INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # BUDGET MENSUEL
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS budget_mensuel (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            type_ligne TEXT NOT NULL,

            nom TEXT NOT NULL,

            montant REAL NOT NULL DEFAULT 0,

            position INTEGER NOT NULL DEFAULT 0,

            est_separateur INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # AMORTISSEMENTS
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS amortissements (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nom TEXT,

            date_depart TEXT,

            montant_initial REAL NOT NULL DEFAULT 0,

            mise_fond REAL NOT NULL DEFAULT 0,

            taux REAL NOT NULL DEFAULT 0,

            mois INTEGER NOT NULL DEFAULT 0,

            paiement_additionnel REAL NOT NULL DEFAULT 0,

            position INTEGER NOT NULL DEFAULT 0,

            est_separateur INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # RENDEMENTS (interet compose)
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS rendements (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nom TEXT,

            montant_initial REAL NOT NULL DEFAULT 0,

            taux REAL NOT NULL DEFAULT 0,

            mois INTEGER NOT NULL DEFAULT 0,

            cotisation_mensuelle REAL NOT NULL DEFAULT 0,

            position INTEGER NOT NULL DEFAULT 0,

            est_separateur INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # RETRAITE
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS retraites (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nom TEXT,

            placement_actuel REAL NOT NULL DEFAULT 0,

            annees INTEGER NOT NULL DEFAULT 0,

            taux REAL NOT NULL DEFAULT 0,

            cotisation_annuelle REAL NOT NULL DEFAULT 0,

            position INTEGER NOT NULL DEFAULT 0,

            est_separateur INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # HISTORIQUE VALEUR PLACEMENTS
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS placements_valeurs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            placement_id INTEGER,

            date TEXT,

            valeur REAL NOT NULL DEFAULT 0,

            FOREIGN KEY (placement_id)

            REFERENCES placements(id)

        )
        """
    )



    # =========================
    # ANCIENNE HYPOTHEQUE (compatibilité)
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS hypotheque (

            id INTEGER PRIMARY KEY,

            valeur_condo REAL NOT NULL DEFAULT 0,

            dette_actuelle REAL NOT NULL DEFAULT 0,

            paiement_annuel REAL NOT NULL DEFAULT 0

        )
        """
    )


    cursor.execute(
        """
        INSERT OR IGNORE INTO hypotheque

        (
        id,
        valeur_condo,
        dette_actuelle,
        paiement_annuel
        )

        VALUES

        (
        1,
        0,
        0,
        0
        )

        """
    )



    # =========================
    # TRAVAIL AUTONOME (TAXES)
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS travail_autonome (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            annee INTEGER,

            contrat TEXT,

            montant_facture REAL NOT NULL DEFAULT 0,

            sans_taxes INTEGER NOT NULL DEFAULT 0,

            sans_impot INTEGER NOT NULL DEFAULT 0,

            impot_a_payer REAL NOT NULL DEFAULT 0,

            position INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # ACOMPTES PROVISIONNELS
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS acomptes (

            id INTEGER PRIMARY KEY,

            provincial_paye REAL NOT NULL DEFAULT 0,

            federal_paye REAL NOT NULL DEFAULT 0

        )
        """
    )


    cursor.execute(
        """
        INSERT OR IGNORE INTO acomptes

        (
        id,
        provincial_paye,
        federal_paye
        )

        VALUES

        (
        1,
        0,
        0
        )

        """
    )



    # =========================
    # DEDUCTIONS D'IMPOT
    # =========================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS deductions_impot (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nom TEXT,

            montant REAL NOT NULL DEFAULT 0,

            position INTEGER NOT NULL DEFAULT 0

        )
        """
    )



    # =========================
    # AJOUT DE COLONNES SI BASE EXISTANTE
    # =========================

    colonnes_a_ajouter = [

        (
            "entrees_argent",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "sorties_argent",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "placements",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "placements",
            "type_ligne",
            "TEXT DEFAULT 'Autre'"
        ),

        (
            "prets",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "prets",
            "mois",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "hypotheques",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "bourse",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "bourse",
            "type_ligne",
            "TEXT DEFAULT 'Bourse'"
        ),

        (
            "bourse",
            "symbole",
            "TEXT"
        ),

        (
            "assurances",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "assurances",
            "type_assurance",
            "TEXT"
        ),

        (
            "budgets",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "budget_lignes",
            "autres_infos",
            "TEXT"
        ),

        (
            "patrimoine",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "budget_mensuel",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "amortissements",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "amortissements",
            "paiement_additionnel",
            "REAL NOT NULL DEFAULT 0"
        ),

        (
            "rendements",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "rendements",
            "cotisation_mensuelle",
            "REAL NOT NULL DEFAULT 0"
        ),

        (
            "retraites",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "users",
            "indice1",
            "TEXT"
        ),

        (
            "users",
            "indice2",
            "TEXT"
        )

    ]


    for table, colonne, definition in colonnes_a_ajouter:

        try:

            cursor.execute(
                f"ALTER TABLE {table} ADD COLUMN {colonne} {definition}"
            )

        except sqlite3.OperationalError:

            pass


    conn.commit()

    conn.close()



def reset_database():

    """
    Efface toutes les donnees de l'application.

    - Vide toutes les tables de donnees
    - Remet a zero les compteurs d'identifiants
    - Reinitialise le NIP a 1234 et vide les indices
    - Supprime le fichier des champs du simulateur d'impot
    - Conserve la copie de securite .backup
    """

    conn = get_connection()

    cursor = conn.cursor()


    # =========================
    # TABLES A VIDER
    # =========================

    tables_a_vider = [

        "entrees_argent",

        "sorties_argent",

        "placements_valeurs",

        "placements",

        "plafonds",

        "prets",

        "hypotheques",

        "bourse",

        "reer_celi",

        "budget_mensuel",

        "amortissements",

        "rendements",

        "retraites",

        "travail_autonome",

        "assurances",

        "couvertures",

        "budgets",

        "budget_lignes",

        "patrimoine",

        "cumulatifs",

        "deductions_impot"

    ]


    for table in tables_a_vider:

        try:

            cursor.execute(
                f"DELETE FROM {table}"
            )

        except sqlite3.OperationalError:

            pass


    # =========================
    # COMPTEURS D'IDENTIFIANTS
    # =========================

    # Remet les AUTOINCREMENT a 1.
    # La table sqlite_sequence n'existe que si une table
    # AUTOINCREMENT a deja recu une ligne.

    try:

        cursor.execute(
            "DELETE FROM sqlite_sequence"
        )

    except sqlite3.OperationalError:

        pass


    # =========================
    # TABLES A LIGNE UNIQUE
    # =========================

    cursor.execute(
        """
        DELETE FROM hypotheque
        """
    )


    cursor.execute(
        """
        INSERT INTO hypotheque

        (
        id,
        valeur_condo,
        dette_actuelle,
        paiement_annuel
        )

        VALUES

        (
        1,
        0,
        0,
        0
        )
        """
    )


    cursor.execute(
        """
        DELETE FROM acomptes
        """
    )


    cursor.execute(
        """
        INSERT INTO acomptes

        (
        id,
        provincial_paye,
        federal_paye
        )

        VALUES

        (
        1,
        0,
        0
        )
        """
    )


    cursor.execute(
        """
        DELETE FROM plafonds
        """
    )


    cursor.execute(
        """
        INSERT INTO plafonds

        (
        id,
        reer_possible,
        celi_possible
        )

        VALUES

        (
        1,
        0,
        0
        )
        """
    )


    # =========================
    # UTILISATEUR
    # =========================

    cursor.execute(
        """
        DELETE FROM users
        """
    )


    cursor.execute(
        """
        INSERT INTO users

        (
        id,
        username,
        password,
        indice1,
        indice2
        )

        VALUES

        (
        1,
        'admin',
        '1234',
        '',
        ''
        )
        """
    )


    conn.commit()

    conn.close()


    # =========================
    # FICHIER DU SIMULATEUR D'IMPOT
    # =========================

    # Les montants saisis dans le simulateur sont enregistres
    # dans un fichier JSON, hors de la base.

    try:

        from pages.impot_parametres import effacer

        effacer()

    except Exception:

        pass
