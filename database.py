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
            "TEXT DEFAULT ''"
        ),

        (
            "assurances",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "assurances",
            "prime",
            "REAL NOT NULL DEFAULT 0"
        ),

        (
            "budgets",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "cumulatifs",
            "entrees",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "cumulatifs",
            "sorties",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "cumulatifs",
            "taxes_provinciales",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "cumulatifs",
            "taxes_federales",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "cumulatifs",
            "impots",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "cumulatifs",
            "prets",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "cumulatifs",
            "hypotheques",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "cumulatifs",
            "placements",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "cumulatifs",
            "reer",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "cumulatifs",
            "celi",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "cumulatifs",
            "patrimoine",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "cumulatifs",
            "position",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "patrimoine",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "couvertures",
            "nom",
            "TEXT DEFAULT ''"
        ),

        (
            "couvertures",
            "type_montant",
            "TEXT DEFAULT 'Prix ($)'"
        ),

        (
            "users",
            "indice1",
            "TEXT DEFAULT ''"
        ),

        (
            "users",
            "indice2",
            "TEXT DEFAULT ''"
        ),

        (
            "bourse",
            "nombre_actions",
            "REAL NOT NULL DEFAULT 0"
        ),

        (
            "bourse",
            "prix_actuel",
            "REAL NOT NULL DEFAULT 0"
        ),

        (
            "reer_celi",
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
            "rendements",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "retraites",
            "est_separateur",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "travail_autonome",
            "sans_tps",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "travail_autonome",
            "sans_tvq",
            "INTEGER NOT NULL DEFAULT 0"
        ),

        (
            "travail_autonome",
            "pourcentage_impot",
            "REAL NOT NULL DEFAULT 33"
        )

    ]


    for table, colonne, type_sql in colonnes_a_ajouter:

        try:

            cursor.execute(
                f"ALTER TABLE {table} ADD COLUMN {colonne} {type_sql}"
            )

        except sqlite3.OperationalError:

            pass



    # =========================
    # MIGRATION BOURSE (nombre d'actions)
    # =========================

    try:

        cursor.execute(
            """
            UPDATE bourse

            SET nombre_actions = 1

            WHERE est_separateur = 0

            AND (nombre_actions IS NULL OR nombre_actions = 0)
            """
        )


        cursor.execute(
            """
            UPDATE bourse

            SET prix_actuel = valeur_actuelle

            WHERE est_separateur = 0

            AND (prix_actuel IS NULL OR prix_actuel = 0)
            """
        )

    except sqlite3.OperationalError:

        pass


    conn.commit()

    conn.close()



def reset_database():

    conn = get_connection()

    cursor = conn.cursor()


    tables_a_vider = [

        "entrees_argent",
        "sorties_argent",
        "placements_valeurs",
        "placements",
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
        "cumulatifs"

    ]


    for table in tables_a_vider:

        try:

            cursor.execute(
                f"DELETE FROM {table}"
            )

        except sqlite3.OperationalError:

            pass


    cursor.execute(
        """
        UPDATE hypotheque

        SET

        valeur_condo = 0,

        dette_actuelle = 0,

        paiement_annuel = 0

        WHERE id = 1

        """
    )


    cursor.execute(
        """
        UPDATE acomptes

        SET

        provincial_paye = 0,

        federal_paye = 0

        WHERE id = 1

        """
    )


    cursor.execute(
        """
        UPDATE plafonds

        SET

        reer_possible = 0,

        celi_possible = 0

        WHERE id = 1

        """
    )


    cursor.execute(
        """
        UPDATE users

        SET password = '1234',
        indice1 = '',
        indice2 = ''

        WHERE id = 1

        """
    )


    conn.commit()

    conn.close()
