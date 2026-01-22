# Reinforcement Learning Snake

## Description

Projet Python implémentant le jeu classique du **Snake**, dans lequel le serpent est contrôlé par un **agent apprenant par renforcement** (*Reinforcement Learning*).

L'agent évolue dans un environnement simple et apprend à optimiser son comportement grâce à un système de récompenses :

- Récompense de +10 points chaque fois que l'agent mange de la nourriture
- Fin de l'épisode si :
  - le serpent entre en collision avec lui-même
  - ou si l'agent n'a pas mangé de nourriture après un certain nombre d'itérations

L'objectif est d'apprendre une politique efficace permettant de maximiser le score et la durée de survie.

Le projet utilise **Python 3.13 ou supérieur** ainsi que les bibliothèques suivantes :

- [pygame](https://www.pygame.org/docs/)
- [numpy](https://numpy.org/doc/)
- [torch / torchvision](https://pytorch.org/docs/stable/index.html)

---

## Installation et démarrage

### Créer un environnement virtuel

À la racine du projet :

```bash
python3 -m venv ./rl_snake
```

### Activer l'environnement virtuel

Sur macOS / Linux :

```bash
source rl_snake/bin/activate
```

Sur Windows :

```bash
rl_snake\\Scripts\\activate
```

### 4️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### Lancer le projet

Pour démarrer l'agent et le jeu Snake :

```bash
python agent.py
```

Une fenêtre `pygame` s'ouvrira et affichera l'agent en train d'apprendre à jouer.

---

## Auteur

Créé par **[William Pasquier](https://github.com/WilliamPasquier)**\
README rédigé par ChatGPT (Un peu la flemme de tout taper et formater)


