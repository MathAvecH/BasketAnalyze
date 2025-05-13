# Analyse des Performances de Joueurs de Basketball

Ce projet contient un script Python qui récupère, analyse et génère des statistiques détaillées à partir des données de matchs de basketball. Il permet d'extraire des informations sur les performances individuelles des joueurs et des statistiques d'équipe à partir de données disponibles sur une plateforme de sport (par exemple, via un scraping de sites web ou d'APIs).

[Démo Google Colab](https://colab.research.google.com/drive/1CQU5uI0m92-XrhGjQSlFDePjJZbGQzeN?usp=sharing)

## Fonctionnalités

* **Scraping des données** : Récupération des informations de performances individuelles des joueurs de basketball lors de chaque match.
* **Calcul des statistiques** : Calcul des moyennes de points, rebonds, passes décisives, pourcentages de tirs réussis, etc.
* **Analyse des performances** : Agrégation des données pour déterminer les performances des joueurs en fonction des matchs gagnés ou perdus.
* **Génération de fichiers CSV** : Exportation des statistiques dans des fichiers CSV pour une analyse approfondie.
* **Moyennes par joueur et équipe** : Moyennes détaillées pour chaque joueur et équipe, avec une distinction entre les matchs gagnés et les matchs perdus.
* **Analyse avancée** : Calcul des pourcentages de réussite aux tirs (2 points, 3 points, lancer franc) et autres statistiques avancées.

## Prérequis

* Python 3.x
* Les bibliothèques suivantes sont requises :

  * `requests`
  * `beautifulsoup4`
  * `pandas`

Tu peux installer ces dépendances en exécutant la commande suivante :

```bash
pip install -r requirements.txt
```

## Utilisation

### 1. Récupérer les données

Le script commence par récupérer les données de chaque match et de chaque joueur en utilisant un processus de **scraping**. Il récupère les informations suivantes pour chaque joueur :

* Points marqués
* Rebonds
* Passes décisives
* Interceptions
* Contres
* Fautes
* Minutes jouées

### 2. Calcul des statistiques individuelles et d'équipe

Une fois les données récupérées, le script effectue plusieurs calculs :

* Moyenne des points par match pour chaque joueur.
* Moyenne des rebonds, passes, et autres statistiques.
* Pourcentages de réussite pour chaque joueur (2 points, 3 points, lancer franc).
* Calcul des moyennes globales de l'équipe pour chaque critère.

### 3. Analyse des performances par victoire et défaite

Le script compare les performances des joueurs entre les matchs gagnés et perdus et génère des moyennes spécifiques pour chaque cas.

### 4. Exportation des résultats

Les résultats sont enregistrés dans des fichiers CSV. Tu peux ensuite ouvrir ces fichiers dans un tableur (comme Excel) ou les utiliser pour des analyses ultérieures.

#### Exemple de génération du fichier CSV :

```bash
python match_scraper.py
```

Cela génère des fichiers CSV qui contient les performances détaillées.

## Auteurs

* **MathAvecH** - *Auteur principal* - [MathAvecH](https://github.com/MathAvecH)

## Licence

Ce projet est sous licence **MIT** - consulte le fichier [LICENSE](LICENSE) pour plus de détails.
