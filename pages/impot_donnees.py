import json
import re
import os
import urllib.request
import urllib.error
from datetime import datetime

from database import DOSSIER_DONNEES


FICHIER_PARAMETRES = "parametres_impot.json"

ENTETES = {
    "User-Agent": "MBDL/1.3",
    "Accept": "application/json"
}


# =========================
# VALEURS OFFICIELLES INTÉGRÉES
# =========================

CONNU = {

    2027: {
        "federal": {
            "paliers": [
                {"limite": 59700,  "taux": 14.0},
                {"limite": 119400, "taux": 20.5},
                {"limite": 185000, "taux": 26.0},
                {"limite": 263000, "taux": 29.0},
                {"limite": None,   "taux": 33.0}
            ],
            "montant_personnel": 16780,
            "abattement_quebec": 0.165
        },
        "quebec": {
            "paliers": [
                {"limite": 55400,  "taux": 14.0},
                {"limite": 110800, "taux": 19.0},
                {"limite": 134800, "taux": 24.0},
                {"limite": None,   "taux": 25.75}
            ],
            "montant_personnel": 19320
        },
        "cotisations": {
            "rrq_taux": 6.40,
            "rrq_exemption": 3500,
            "rrq_maximum": 76000,
            "rqap_taux": 0.764,
            "rqap_maximum": 102000
        }
    },

    2026: {
        "federal": {
            "paliers": [
                {"limite": 58523,  "taux": 14.0},
                {"limite": 117045, "taux": 20.5},
                {"limite": 181440, "taux": 26.0},
                {"limite": 258482, "taux": 29.0},
                {"limite": None,   "taux": 33.0}
            ],
            "montant_personnel": 16452,
            "abattement_quebec": 0.165
        },
        "quebec": {
            "paliers": [
                {"limite": 54345,  "taux": 14.0},
                {"limite": 108680, "taux": 19.0},
                {"limite": 132245, "taux": 24.0},
                {"limite": None,   "taux": 25.75}
            ],
            "montant_personnel": 18947
        },
        "cotisations": {
            "rrq_taux": 6.40,
            "rrq_exemption": 3500,
            "rrq_maximum": 74600,
            "rqap_taux": 0.764,
            "rqap_maximum": 100000
        }
    },

    2025: {
        "federal": {
            "paliers": [
                {"limite": 57375,  "taux": 14.5},
                {"limite": 114750, "taux": 20.5},
                {"limite": 177882, "taux": 26.0},
                {"limite": 253414, "taux": 29.0},
                {"limite": None,   "taux": 33.0}
            ],
            "montant_personnel": 16129,
            "abattement_quebec": 0.165
        },
        "quebec": {
            "paliers": [
                {"limite": 53255,  "taux": 14.0},
                {"limite": 106495, "taux": 19.0},
                {"limite": 129590, "taux": 24.0},
                {"limite": None,   "taux": 25.75}
            ],
            "montant_personnel": 18571
        },
        "cotisations": {
            "rrq_taux": 6.40,
            "rrq_exemption": 3500,
            "rrq_maximum": 71300,
            "rqap_taux": 0.878,
            "rqap_maximum": 98000
        }
    },

    2024: {
        "federal": {
            "paliers": [
                {"limite": 55867,  "taux": 15.0},
                {"limite": 111733, "taux": 20.5},
                {"limite": 173205, "taux": 26.0},
                {"limite": 246752, "taux": 29.0},
                {"limite": None,   "taux": 33.0}
            ],
            "montant_personnel": 15705,
            "abattement_quebec": 0.165
        },
        "quebec": {
            "paliers": [
                {"limite": 51780,  "taux": 14.0},
                {"limite": 103545, "taux": 19.0},
                {"limite": 126000, "taux": 24.0},
                {"limite": None,   "taux": 25.75}
            ],
            "montant_personnel": 18056
        },
        "cotisations": {
            "rrq_taux": 6.40,
            "rrq_exemption": 3500,
            "rrq_maximum": 68500,
            "rqap_taux": 0.494,
            "rqap_maximum": 94000
        }
    }
}

ANNEE_DEFAUT = 2026


def donnees_par_defaut(annee=None):

    if annee is None:

        annee = ANNEE_DEFAUT

    modele = CONNU.get(annee) or CONNU[ANNEE_DEFAUT]

    copie = json.loads(json.dumps(modele))

    copie["annee"] = annee
    copie["source"] = f"valeurs officielles intégrées ({annee})"
    copie["date_telechargement"] = None

    return copie


DEFAUT = donnees_par_defaut(ANNEE_DEFAUT)


# =========================
# FICHIER LOCAL
# =========================

def chemin_parametres():

    return os.path.join(
        DOSSIER_DONNEES,
        FICHIER_PARAMETRES
    )


def charger():

    try:

        with open(chemin_parametres(), "r", encoding="utf-8") as f:

            donnees = json.load(f)

        if donnees_valides(donnees):

            return donnees

    except Exception:

        pass

    return donnees_par_defaut()


def sauvegarder(donnees):

    try:

        os.makedirs(DOSSIER_DONNEES, exist_ok=True)

        with open(chemin_parametres(), "w", encoding="utf-8") as f:

            json.dump(donnees, f, indent=2, ensure_ascii=False)

        return True

    except Exception:

        return False


def annee_telechargee():

    chemin = chemin_parametres()

    if not os.path.exists(chemin):

        return None

    try:

        with open(chemin, "r", encoding="utf-8") as f:

            donnees = json.load(f)

        if donnees.get("date_telechargement"):

            return donnees.get("annee")

        return None

    except Exception:

        return None


def est_telechargee(annee):

    """
    Vrai si les barèmes de cette année ont déjà été
    téléchargés et enregistrés.
    """

    chemin = chemin_parametres()

    if not os.path.exists(chemin):

        return False

    try:

        with open(chemin, "r", encoding="utf-8") as f:

            donnees = json.load(f)

        return (
            int(donnees.get("annee", 0)) == int(annee)
            and bool(donnees.get("date_telechargement"))
        )

    except Exception:

        return False


def date_telechargement():

    chemin = chemin_parametres()

    if not os.path.exists(chemin):

        return ""

    try:

        with open(chemin, "r", encoding="utf-8") as f:

            donnees = json.load(f)

        brut = donnees.get("date_telechargement")

        if not brut:

            return ""

        moment = datetime.fromisoformat(brut)

        return moment.strftime("%Y-%m-%d à %H:%M")

    except Exception:

        return ""


# =========================
# TÉLÉCHARGEMENT
# =========================
#
# La page lue liste les paliers federaux dans un tableau
# "58 523 $ ou moins | 14 %", puis les provinces sous la forme
# "14 % sur les premiers 54 345 $ ...". On lit chaque tableau
# separement et on verifie le resultat avant de l'utiliser.

import html as _html

PAGE_PALIERS = (
    "https://www.wealthsimple.com/fr-ca/learn/tax-brackets-canada"
)

ENTETES_PAGE = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "fr-CA,fr;q=0.9"
}

_NB = r"(\d{1,3}(?:[ .]\d{3})+|\d{4,7})"
_TX = r"(\d{1,2}(?:[,.]\d{1,2})?)"


def _lire_page(url):

    requete = urllib.request.Request(url)

    for cle, valeur in ENTETES_PAGE.items():

        requete.add_header(cle, valeur)

    with urllib.request.urlopen(requete, timeout=20) as reponse:

        return reponse.read().decode("utf-8", errors="ignore")


def _normaliser(texte):

    texte = _html.unescape(texte)

    for car in ("\u00a0", "\u202f", "\u2009"):

        texte = texte.replace(car, " ")

    texte = texte.replace("\u2019", "'")

    return re.sub(r"\s+", " ", texte)


def _texte_visible(page):

    page = re.sub(r"<script.*?</script>", " ", page, flags=re.S | re.I)
    page = re.sub(r"<style.*?</style>", " ", page, flags=re.S | re.I)
    page = re.sub(r"<[^>]+>", " ", page)

    return _normaliser(page)


def _texte_complet(page):

    # Secours : certains sites placent le contenu dans du JSON
    page = page.replace("\\u00a0", " ").replace("\\u202f", " ")
    page = re.sub(
        r"\\u([0-9a-fA-F]{4})",
        lambda m: chr(int(m.group(1), 16)),
        page
    )
    page = re.sub(r"<[^>]+>", " ", page)

    return _normaliser(page)


def _nombre(txt):

    return int(re.sub(r"[ .]", "", txt))


def _taux(txt):

    return float(txt.replace(",", "."))


def _lire_federal(texte):

    debut = texte.find("fédéraux pour")

    if debut == -1:

        return None, []

    fin = texte.find("provinciaux", debut)

    zone = texte[debut: fin if fin != -1 else debut + 3000]

    annee = None

    m = re.search(r"fédéraux pour (\d{4})", zone)

    if m:

        annee = int(m.group(1))

    lignes = []

    for m in re.finditer(_NB + r"\s*\$\s*ou moins\s*\|?\s*" + _TX + r"\s*%", zone):

        lignes.append((m.start(), _nombre(m.group(1)), _taux(m.group(2))))

    for m in re.finditer(r"jusqu'à\s*" + _NB + r"\s*\$\s*\|?\s*" + _TX + r"\s*%", zone):

        lignes.append((m.start(), _nombre(m.group(1)), _taux(m.group(2))))

    for m in re.finditer(r"Plus de\s*" + _NB + r"\s*\$\s*\|?\s*" + _TX + r"\s*%", zone):

        lignes.append((m.start(), None, _taux(m.group(2))))

    lignes.sort(key=lambda x: x[0])

    return annee, [{"limite": l, "taux": t} for _, l, t in lignes]


def _lire_quebec(texte):

    m = re.search(
        r"Québec\s*\|?\s*" + _TX + r"\s*%\s*sur les premiers",
        texte
    )

    if not m:

        return []

    debut = m.start()

    suivant = texte.find("sur les premiers", m.end())

    zone = texte[debut: suivant if suivant != -1 else debut + 2000]

    lignes = []

    for r in re.finditer(_TX + r"\s*%\s*sur les premiers\s*" + _NB + r"\s*\$", zone):

        lignes.append((r.start(), _nombre(r.group(2)), _taux(r.group(1))))

    for r in re.finditer(
        _TX + r"\s*%\s*sur la partie[^%|]*?dépassant\s*" + _NB
        + r"\s*\$\s*jusqu'à\s*" + _NB + r"\s*\$",
        zone
    ):

        lignes.append((r.start(), _nombre(r.group(3)), _taux(r.group(1))))

    for r in re.finditer(
        _TX + r"\s*%\s*sur la partie[^%|]*?dépassant\s*" + _NB
        + r"\s*\$(?!\s*jusqu)",
        zone
    ):

        lignes.append((r.start(), None, _taux(r.group(1))))

    lignes.sort(key=lambda x: x[0])

    return [{"limite": l, "taux": t} for _, l, t in lignes]


def paliers_valides(paliers, minimum, maximum):

    """
    Verifie qu'une liste de paliers est coherente :
    bon nombre de lignes, seuils croissants, dernier "et plus".
    """

    if not isinstance(paliers, list):

        return False

    if not (minimum <= len(paliers) <= maximum):

        return False

    precedent = 0

    for index, palier in enumerate(paliers):

        try:

            limite = palier["limite"]
            taux = float(palier["taux"])

        except Exception:

            return False

        if not (5 <= taux <= 40):

            return False

        dernier = index == len(paliers) - 1

        if dernier:

            if limite is not None:

                return False

        else:

            if limite is None or limite <= precedent:

                return False

            precedent = limite

    return True


def donnees_valides(donnees):

    try:

        return (
            paliers_valides(donnees["federal"]["paliers"], 4, 7)
            and paliers_valides(donnees["quebec"]["paliers"], 3, 7)
        )

    except Exception:

        return False


def analyser_page(page):

    """
    Retourne (annee, paliers_federal, paliers_quebec) ou
    (None, [], []) si rien de fiable n'a ete trouve.
    """

    for texte in (_texte_visible(page), _texte_complet(page)):

        annee, federal = _lire_federal(texte)
        quebec = _lire_quebec(texte)

        if paliers_valides(federal, 4, 7) and paliers_valides(quebec, 3, 7):

            return annee, federal, quebec

    return None, [], []


def telecharger(annee=None):

    """
    Retourne (succes, message, donnees).
    En cas d'echec, donnees vaut None et l'appelant
    utilise les valeurs integrees.
    """

    if annee is None:

        annee = ANNEE_DEFAUT

    annee = int(annee)

    try:

        page = _lire_page(PAGE_PALIERS)

    except urllib.error.URLError:

        return (False, "Connexion Internet impossible.", None)

    except Exception:

        return (False, "Le téléchargement a échoué.", None)

    try:

        annee_page, federal, quebec = analyser_page(page)

    except Exception:

        annee_page, federal, quebec = None, [], []

    if not federal or not quebec:

        return (False, "Les paliers n'ont pas pu être lus.", None)

    if annee_page is not None and annee_page != annee:

        if annee > annee_page:

            raison = f"Les paliers {annee} ne sont pas encore publiés."

        else:

            raison = f"Les paliers {annee} ne sont plus disponibles en ligne."

        return (False, raison, None)

    modele = donnees_par_defaut(annee)

    modele["federal"]["paliers"] = federal
    modele["quebec"]["paliers"] = quebec

    modele["date_telechargement"] = datetime.now().isoformat(
        timespec="minutes"
    )

    return (True, "", modele)


# =========================
# CALCUL
# =========================

def _impot_par_paliers(revenu, paliers):

    impot = 0.0
    precedent = 0.0

    for palier in paliers:

        limite = palier["limite"]
        taux = palier["taux"] / 100.0

        if limite is None:

            if revenu > precedent:

                impot += (revenu - precedent) * taux

            break

        tranche = min(revenu, limite) - precedent

        if tranche > 0:

            impot += tranche * taux

        precedent = limite

        if revenu <= limite:

            break

    return impot


def _taux_marginal(revenu, paliers):

    for palier in paliers:

        limite = palier["limite"]

        if limite is None or revenu <= limite:

            return palier["taux"]

    return paliers[-1]["taux"]


def calculer(
    revenu,
    autonome=False,
    autres_deductions=0.0,
    donnees=None
):

    if donnees is None:

        donnees = charger()

    revenu = max(0.0, float(revenu))
    autres_deductions = max(0.0, float(autres_deductions))

    cot = donnees["cotisations"]

    if autonome:

        rrq_base = max(
            0.0,
            min(revenu, cot["rrq_maximum"]) - cot["rrq_exemption"]
        )

        rrq = rrq_base * (cot["rrq_taux"] / 100.0)

        rqap = (
            min(revenu, cot["rqap_maximum"])
            * (cot["rqap_taux"] / 100.0)
        )

    else:

        rrq = 0.0
        rqap = 0.0

    cotisations = rrq + rqap

    revenu_imposable = max(0.0, revenu - autres_deductions)

    fed = donnees["federal"]

    impot_federal_brut = _impot_par_paliers(
        revenu_imposable,
        fed["paliers"]
    )

    impot_federal = max(
        0.0,
        impot_federal_brut - fed["montant_personnel"] * 0.145
    )

    impot_federal -= impot_federal * fed["abattement_quebec"]

    qc = donnees["quebec"]

    impot_quebec_brut = _impot_par_paliers(
        revenu_imposable,
        qc["paliers"]
    )

    impot_quebec = max(
        0.0,
        impot_quebec_brut - qc["montant_personnel"] * 0.14
    )

    impot_total = impot_federal + impot_quebec

    taux_moyen = (impot_total / revenu * 100.0) if revenu > 0 else 0.0

    marginal_federal = _taux_marginal(
        revenu_imposable,
        fed["paliers"]
    )

    marginal_quebec = _taux_marginal(
        revenu_imposable,
        qc["paliers"]
    )

    return {

        "revenu": revenu,
        "revenu_imposable": revenu_imposable,
        "impot_federal": impot_federal,
        "impot_quebec": impot_quebec,
        "impot_total": impot_total,
        "rrq": rrq,
        "rqap": rqap,
        "cotisations": cotisations,
        "revenu_net": revenu - impot_total - cotisations,
        "taux_moyen": taux_moyen,
        "taux_marginal_federal": marginal_federal,
        "taux_marginal_quebec": marginal_quebec,
        "taux_marginal_combine": marginal_federal + marginal_quebec
    }
