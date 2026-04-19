# TP Base Télécom : Numérisation de la Voix (Python)

Ce projet est la partie programmation en Python d'un TP de Base Télécom visant à simuler et analyser le processus de numérisation d'un signal vocal à différentes fréquences d'échantillonnage, conformément aux concepts vus en cours.

## 🛠️ Prérequis et Installation

Ce projet utilise **[`uv`](https://github.com/astral-sh/uv)** comme gestionnaire de dépendances ultrarapide (en remplacement de pip/venv standard).

1. Clonez ce dépôt.
2. Assurez-vous d'avoir `uv` installé sur votre système.
3. Les dépendances incluent : `sounddevice`, `numpy`, `scipy`, `matplotlib` et `python-dotenv`.

## ⚙️ Configuration

Avant de lancer le script, configurez votre environnement pour définir où les fichiers seront enregistrés :
1. Créez un fichier `.env` à la racine (ou copiez le modèle) :
   ```bash
   cp .env.example .env
   ```
2. Modifiez la variable `OUTPUT_DIR` dans le fichier `.env` pour indiquer votre dossier de travail.

## 🚀 Utilisation

Placez-vous dans le répertoire du projet et lancez le script directement avec `uv` :

```bash
uv run main.py
```

Le script va :
1. Vous demander d'enregistrer votre voix pendant 10 secondes à $F_e = 8000\text{ Hz}$.
2. Vous demander d'enregistrer votre voix pendant 10 secondes à $F_e = 44100\text{ Hz}$.
3. Sauvegarder les deux enregistrements au format non compressé `.wav` (quantifiés sur 8 bits ou 256 niveaux, signal mono).
4. Générer une conclusion avec les différences de tailles et afficher une analyse visuelle et spectrale des deux audios.

*Projet réalisé dans le cadre du TP de Base Télécom - DIC1.*
