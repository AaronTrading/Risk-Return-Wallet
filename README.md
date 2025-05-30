# Optimiseur de Portefeuille

Ce projet implémente un modèle d'optimisation de portefeuille basé sur la théorie de Markowitz (mean-variance optimization). Il permet d'optimiser la répartition d'actifs dans un portefeuille en maximisant le rendement pour un niveau de risque donné ou en minimisant le risque pour un rendement cible.

## Fonctionnalités

- Téléchargement de données boursières via yfinance
- Calcul des rendements espérés et de la matrice de covariance
- Optimisation du portefeuille selon différents critères :
  - Maximisation du ratio de Sharpe
  - Optimisation pour un rendement cible
- Visualisation des résultats :
  - Frontière efficiente
  - Répartition des poids (pie chart et bar chart)
  - Matrice de corrélation
  - Distribution des rendements

## Screens

![Screen1](https://media.discordapp.net/attachments/1280431720679870475/1378035231776313466/image.png?ex=683b22d1&is=6839d151&hm=7783bf019ba086d4178347416b05479d2d67b42819082464808421e4b344e9c1&=&format=webp&quality=lossless&width=1104&height=893)
![Screen2](https://media.discordapp.net/attachments/1280431720679870475/1378035230547513444/image.png?ex=683b22d1&is=6839d151&hm=3640ae8b97d6475ffd566ea4e57d5de2c5a905636679c52c1b11e45633be7a50&=&format=webp&quality=lossless&width=1104&height=695)
![Screen3](https://media.discordapp.net/attachments/1280431720679870475/1378035230790910045/image.png?ex=683b22d1&is=6839d151&hm=83c4c5a3211b721a459d80344dc7a80d9e9ebb0200e13b4e548f411aac9d273e&=&format=webp&quality=lossless&width=1104&height=696)
![Screen4](https://media.discordapp.net/attachments/1280431720679870475/1378035231105355947/image.png?ex=683b22d1&is=6839d151&hm=ddb176e6dcd79e5f029f87b0c8f60b82be8ce49f9b770a0f67c66b8b8003d6b8&=&format=webp&quality=lossless&width=1104&height=578)
![Screen5](https://media.discordapp.net/attachments/1280431720679870475/1378035231403147364/image.png?ex=683b22d1&is=6839d151&hm=544d6610db871169a88b0f1c5c373faaada9faa5b7a57413d1418a1e84802b2d&=&format=webp&quality=lossless&width=1104&height=919)

## Installation

1. Clonez le repository :

```bash
git clone [URL_DU_REPO]
cd risk_return_optimizer
```

2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation

1. Lancez l'application :

```bash
python app.py
```

2. Dans l'interface graphique :
   - Entrez les tickers des actifs (séparés par des virgules)
   - Choisissez la période et l'intervalle
   - Sélectionnez le type d'optimisation
   - Cliquez sur "Optimiser"

## Structure du Projet

- `app.py` : Interface graphique principale
- `data_loader.py` : Gestion des données boursières
- `optimizer.py` : Implémentation de l'optimisation
- `plots.py` : Visualisation des résultats
- `requirements.txt` : Dépendances du projet

## Dépendances

- numpy : Calculs numériques
- pandas : Manipulation des données
- matplotlib : Visualisation de base
- seaborn : Amélioration des visualisations
- cvxopt : Optimisation quadratique
- yfinance : Données boursières
- tkinter : Interface graphique
- seaborn : Visualisation avancée

## Exemple d'Utilisation

1. Lancez l'application
2. Sélectionner les tickers (ex: "AAPL,MSFT,GOOGL")
3. Choisissez la période (ex: "1 an")
4. Sélectionnez l'intervalle (ex: "1 jour")
5. Choisissez le type d'optimisation
6. Cliquez sur "Optimiser"

Les résultats seront affichés sous forme de graphiques et de statistiques.

## Notes

- Les données sont récupérées en temps réel via yfinance
- L'optimisation utilise la programmation quadratique via cvxopt
- Les visualisations sont générées avec matplotlib et seaborn

## Auteur

Aaron Z.

## Licence

MIT
