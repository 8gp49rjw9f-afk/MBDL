import sqlite3


DATABASE_NAME = "mon_financier.db"


def ajouter_colonne_si_absente(
    cursor,
    table,
    colonne,
    definition
):
    try:
        cursor.execute(
            f"ALTER TABLE {table} ADD COLUMN {colonne} {definition}"
        )
        print(f"Colonne ajoutée : {table}.{colonne}")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print(f"Colonne déjà présente : {table}.{colonne}")
        else:
            raise


def main():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()

    # =========================
    # TRAVAIL AUTONOME
    # =========================

    ajouter_colonne_si_absente(
        cursor,
        "travail_autonome",
        "sans_tps",
        "INTEGER NOT NULL DEFAULT 0"
    )

    ajouter_colonne_si_absente(
        cursor,
        "travail_autonome",
        "sans_tvq",
        "INTEGER NOT NULL DEFAULT 0"
    )

    ajouter_colonne_si_absente(
        cursor,
        "travail_autonome",
        "pourcentage_impot",
        "REAL NOT NULL DEFAULT 33"
    )

    # =========================
    # SEPARATEURS
    # =========================

    ajouter_colonne_si_absente(
        cursor,
        "entrees_argent",
        "est_separateur",
        "INTEGER NOT NULL DEFAULT 0"
    )

    ajouter_colonne_si_absente(
        cursor,
        "sorties_argent",
        "est_separateur",
        "INTEGER NOT NULL DEFAULT 0"
    )

    ajouter_colonne_si_absente(
        cursor,
        "placements",
        "est_separateur",
        "INTEGER NOT NULL DEFAULT 0"
    )

    ajouter_colonne_si_absente(
        cursor,
        "prets",
        "est_separateur",
        "INTEGER NOT NULL DEFAULT 0"
    )

    ajouter_colonne_si_absente(
        cursor,
        "bourse",
        "est_separateur",
        "INTEGER NOT NULL DEFAULT 0"
    )

    conn.commit()
    conn.close()

    print("Migration terminée.")


if __name__ == "__main__":
    main()
