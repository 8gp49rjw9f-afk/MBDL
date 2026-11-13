import json
import os

from database import DOSSIER_DONNEES


FICHIER = "parametres_impot_champs.json"


def chemin():

    return os.path.join(DOSSIER_DONNEES, FICHIER)


def charger():

    """
    Retourne (champs, case_rrq).
    champs : dictionnaire cle -> texte du champ.
    """

    try:

        with open(chemin(), "r", encoding="utf-8") as f:

            donnees = json.load(f)

        champs = donnees.get("champs") or {}

        if not isinstance(champs, dict):

            champs = {}

        return champs, bool(donnees.get("case_rrq", False))

    except Exception:

        return {}, False


def sauvegarder(champs, case_rrq):

    """
    Enregistre les champs et la case RRQ/RQAP.
    """

    try:

        os.makedirs(DOSSIER_DONNEES, exist_ok=True)

        with open(chemin(), "w", encoding="utf-8") as f:

            json.dump(
                {
                    "champs": dict(champs),
                    "case_rrq": bool(case_rrq)
                },
                f,
                indent=2,
                ensure_ascii=False
            )

        return True

    except Exception:

        return False


def effacer():

    """
    Retire le fichier : les champs reviennent vides.
    """

    try:

        if os.path.exists(chemin()):

            os.remove(chemin())

        return True

    except Exception:

        return False
