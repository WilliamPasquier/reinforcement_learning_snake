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

- Sur macOS / Linux :

```bash
source rl_snake/bin/activate
```

- Sur Windows :

```bash
rl_snake\\Scripts\\activate
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

### Lancer le projet

Pour démarrer l'agent et le jeu Snake :

```bash
python app.py
```

Une fenêtre `pygame` s'ouvrira et affichera l'agent en train d'apprendre à jouer.

---

## Fonctionnement

### Algorithme

L’algorithme utilisé pour rendre l’agent autonome est le Deep Q-Learning, un algorithme d’apprentissage par renforcement. Son principe est d’apprendre par l’expérience, de manière similaire à un essai-erreur.

L’agent interagit avec son environnement en effectuant des actions. Après chaque action, l’environnement lui renvoie un état, c’est-à-dire une description de la situation dans laquelle il se trouve, ainsi qu’une récompense. Cette récompense permet d’évaluer si l’action effectuée rapproche ou non l’agent de l’objectif fixé.

Lorsque l’action contribue à atteindre l’objectif, l’agent reçoit une récompense positive ; dans le cas contraire, il est pénalisé. À partir de ces retours successifs, l’agent ajuste progressivement sa stratégie afin de choisir, à terme, les actions les plus pertinentes pour maximiser la récompense cumulée et accomplir sa tâche de manière autonome.

<p align="center">
  <img src="./images/rl_snake.svg" width="75%">
</p>

L'état de chaque étape est constitué sous la forme d'une liste composée selon le format suivant :
```python
# 11 informations (0: si faux, 1: si vrai)
[
  # Danger en face (point de vue du mouvement de l'agent),
  # Danger à droite (point de vue du mouvement de l'agent),
  # Danger à gauche (point de vue du mouvement de l'agent),
  # Direction haut (point de vue de l'environnement),
  # Direction droite (point de vue de l'environnement),
  # Direction bas (point de vue de l'environnement),
  # Direction gauche (point de vue de l'environnement),
  # Nourriture à gauche,
  # Nourriture à droite,
  # Nourriture en haut,
  # Nourriture en bas
]

# Exemple d'état
state = [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
```

### Personnalisation

Les paramètres du projet se trouvent dans le module **rlsnake**, il est possible de les modifier afin de changer l'application ainsi que son fonctionnement.

Cependant **attention** à l'ordre des listes ! Elles sont importantes dans la logique et le fonctionnement du projet.

### Résultat

---

<p style="font-size:25px">
<pre>              <b>Départ ~ 0-10ème epoch</b>                                           <b>Après ~ 800 epoch</pre>
</p>
<p >
  <img src="./images/RLSNAKE_0th_epoch.gif" width="50%" align="left">
  <img src="./images/RLSNAKE_800th_epoch.gif" width="50%" align="right">
</p>

## Auteur

Créé par **[William Pasquier](https://github.com/WilliamPasquier)**\
README rédigé par ChatGPT (Un peu la flemme de tout taper et formater)
