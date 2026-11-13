#!/bin/bash

# =========================================
# Compilation de "Mon bas de laine" (MBDL)
# =========================================

echo "Nettoyage des anciennes compilations..."

rm -rf build
rm -rf dist
rm -f MBDL.spec


echo "Compilation en cours..."

python3 -m PyInstaller \
    --name MBDL \
    --windowed \
    --onefile \
    --icon "assets/MyIcon.icns" \
    --add-data "assets:assets" \
    main.py


echo ""
echo "========================================="
echo "Termine."
echo ""
echo "Ton application se trouve ici :"
echo "   dist/MBDL.app"
echo ""
echo "Glisse UNIQUEMENT MBDL.app sur ton bureau."
echo "Ignore le fichier dist/MBDL (sans .app)."
echo "========================================="
