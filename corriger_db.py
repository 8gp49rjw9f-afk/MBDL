from database import get_connection


conn = get_connection()

cursor = conn.cursor()


cursor.execute(
    """
    UPDATE placements
    SET maximum = 0
    WHERE maximum IS NULL
    """
)


cursor.execute(
    """
    UPDATE placements
    SET montant_initial = 0
    WHERE montant_initial IS NULL
    """
)


cursor.execute(
    """
    UPDATE placements
    SET valeur_actuelle = 0
    WHERE valeur_actuelle IS NULL
    """
)


conn.commit()

conn.close()


print("Base corrigée")