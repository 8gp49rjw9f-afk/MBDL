#!/bin/bash

# =========================
# COMPILATION + DMG — Mon bas de laine
# =========================

set -e

cd "$(dirname "$0")"

APP_NAME="MBDL"
VOLUME_NAME="Mon bas de laine"

echo "=== 1/4 — Nettoyage ==="
rm -rf build dist "${APP_NAME}.spec"
rm -f "${APP_NAME}.dmg"

echo "=== 2/4 — Activation de l'environnement ==="
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "Attention : aucun .venv trouvé, utilisation du Python système."
fi

echo "=== 3/4 — Compilation (mode dossier, démarrage rapide) ==="
python -m PyInstaller \
    --name "${APP_NAME}" \
    --windowed \
    --onedir \
    --icon "assets/MyIcon.icns" \
    --add-data "assets:assets" \
    --noconfirm \
    main.py

echo "=== 4/4 — Création du DMG ==="

DMG_STAGE="dist/dmg_stage"
rm -rf "${DMG_STAGE}"
mkdir -p "${DMG_STAGE}"

# Copie de l'application
cp -R "dist/${APP_NAME}.app" "${DMG_STAGE}/"

# Lien vers Applications (pour glisser-déposer)
ln -s /Applications "${DMG_STAGE}/Applications"

# Création du DMG
hdiutil create \
    -volname "${VOLUME_NAME}" \
    -srcfolder "${DMG_STAGE}" \
    -ov \
    -format UDZO \
    "dist/${APP_NAME}.dmg"

rm -rf "${DMG_STAGE}"

echo ""
echo "======================================"
echo " Terminé !"
echo " Application : dist/${APP_NAME}.app"
echo " DMG         : dist/${APP_NAME}.dmg"
echo "======================================"
