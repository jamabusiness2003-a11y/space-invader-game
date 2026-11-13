# Space Invader

## Présentation

**Space Invader** est un jeu vidéo de type *shoot 'em up* développé en Python avec la bibliothèque **Pygame**. Le joueur contrôle un vaisseau spatial placé dans la partie inférieure de l'écran et doit éliminer les envahisseurs qui se déplacent au-dessus de lui.

Le projet comprend notamment :
- un menu principal;
- une partie jouable avec des vagues d'envahisseurs;
- des tirs du joueur et des envahisseurs;
- un système de points et de santé;
- des animations d'explosion;
- une pause;
- un écran de paramètres permettant de régler le volume de la musique;
- une progression par niveaux.

## Technologies et ressources

| Élément | Utilisation |
|---|---|
| Python | Langage de programmation |
| Pygame | Fenêtre, événements, clavier, sprites, collisions, sons et affichage |
| `pygame.sprite` | Organisation et mise à jour des sprites |
| `pygame.mask` | Détection des collisions précises par masque |
| `enum.Enum` | Représentation des états du jeu |
| Images PNG | Vaisseau, envahisseurs, lasers, explosions, arrière-plans et boutons |
| Fichiers MP3 / OGG | Musique et effets sonores |
| Polices TTF | Affichage du texte du jeu |

La fenêtre est configurée à **1000 × 600 pixels** et la fréquence cible est de **60 images par seconde**.

## Structure du projet

```text
SpacesInvader/
├── font/
│   ├── kenvector_future.ttf
│   └── kenvector_future_thin.ttf
├── images/
│   ├── Backgrounds/
│   ├── BlueExplosion/
│   ├── BlueLaser/
│   ├── Button/
│   ├── Invader/
│   ├── Player/
│   └── RedExplosion/
├── sounds/
│   ├── explosion-fx.mp3
│   ├── music.mp3
│   ├── sfx_laser1.ogg
│   └── sfx_laser2.ogg
└── scripts/
    ├── main.py
    ├── sprites.py
    ├── settings/
    │   ├── constants.py
    │   ├── gametimer.py
    │   ├── imports.py
    │   └── support.py
    └── utility/
        ├── button.py
        └── gamestate.py
```

### Responsabilités des modules

#### `scripts/main.py`

Point d'entrée et contrôleur principal du jeu. La classe `Game` :
- initialise Pygame, la fenêtre, l'horloge et les ressources;
- crée les groupes de sprites, le joueur et les envahisseurs;
- charge les animations;
- gère le score, le niveau et le volume;
- traite les événements et les changements d'état;
- met à jour et dessine les éléments du jeu;
- exécute la boucle principale avec `run()`.

#### `scripts/sprites.py`

Contient les objets visuels et leur comportement :

| Classe | Responsabilité |
|---|---|
| `AnimatedSprite` | Classe de base pour animer une suite d'images |
| `AllSprites` | Groupe chargé de dessiner les sprites principaux |
| `Player` | Déplacement du vaisseau, tirs, santé et barre de vie |
| `Invader` | Comportement individuel d'un envahisseur et déclenchement de ses tirs |
| `InvaderSprites` | Création, déplacement collectif et accélération des envahisseurs |
| `Player_Laser` | Projectile du joueur, animation et collision |
| `Invader_Laser` | Projectile des envahisseurs et dégâts infligés au joueur |
| `Explosion` | Animation et rotation d'une explosion |

#### `scripts/settings/`

- **`constants.py`** : dimensions de la fenêtre, fréquence d'affichage et couleurs.
- **`imports.py`** : regroupe les imports utilisés dans plusieurs modules, dont Pygame, les constantes clavier, `random`, `math` et `Enum`.
- **`support.py`** : fonctions utilitaires pour redimensionner les images, importer des séquences d'images et charger les sons.
- **`gametimer.py`** : classe `GameTimer`, utilisée pour déclencher des actions après un délai.

#### `scripts/utility/`

- **`button.py`** : classe `Button`, qui affiche un bouton, gère son survol et détecte un clic gauche.
- **`gamestate.py`** : énumération `GameState`, qui définit les différents écrans du jeu.

## Installation et lancement

### Prérequis

- Python installé;
- Pygame Community Edition installé;
- l'ensemble du dossier du projet, notamment les dossiers `images`, `font` et `sounds`.

Installer Pygame :

```bash
python -m pip install pygame-ce
```

### Lancer le jeu

Depuis le dossier racine `SpacesInvader`, exécuter :

```bash
python scripts/main.py
```

Le répertoire courant doit rester le dossier racine du projet, car le programme charge les images, les polices et les sons avec des chemins relatifs tels que `images/`, `font/` et `sounds/`.

## Commandes du jeu

| Commande | Action |
|---|---|
| Flèche gauche | Déplacer le vaisseau vers la gauche |
| Flèche droite | Déplacer le vaisseau vers la droite |
| Espace | Tirer un laser |
| `P` | Mettre le jeu en pause ou reprendre la partie |
| Flèche gauche / droite dans les paramètres | Diminuer / augmenter le volume |
| `N` | Réessayer après une défaite |
| Clic gauche | Activer les boutons des menus |

Le vaisseau ne peut pas sortir des limites horizontales de la fenêtre.

## Déroulement d'une partie

### 1. Menu principal

Au lancement, le jeu affiche le menu principal avec les options :
- **Play** : commencer la partie;
- **Settings** : ouvrir les paramètres;
- **Quit** : quitter le jeu.

### 2. Partie

Le joueur commence avec **100 points de santé**. Une formation initiale de **3 rangées et 5 colonnes** d'envahisseurs est créée.

Les envahisseurs se déplacent horizontalement. Lorsqu'ils atteignent un bord de la fenêtre, leur direction s'inverse et ils descendent de 10 pixels.

Le joueur peut tirer avec la barre d'espace. Un délai de 600 millisecondes est appliqué entre les tirs du joueur. Les envahisseurs disposent également de tirs, après un délai initial de 3 secondes et avec un délai de tir de 8 secondes.

### 3. Score et collisions

- Un envahisseur touché par un laser du joueur est éliminé.
- Chaque envahisseur éliminé ajoute **30 points** au score.
- La vitesse des envahisseurs augmente de **2,5** après une élimination.
- Un laser ennemi qui touche le joueur lui retire **30 points de santé**.
- Une explosion et un effet sonore sont déclenchés lors des collisions concernées.

Les collisions entre lasers et sprites utilisent les masques Pygame (`pygame.sprite.collide_mask`).

### 4. Pause

La touche `P` ouvre l'écran de pause. Le bouton **Resume**, ou une nouvelle pression sur `P`, permet de reprendre la partie.

### 5. Fin de partie et niveaux

L'écran de fin apparaît dans deux situations :
- tous les envahisseurs ont été éliminés : le jeu affiche **You Win !!!** et propose **Next Level**;
- la santé du joueur atteint zéro : le jeu affiche **Game Over !!!** et propose **Retry**.

Lors du passage au niveau suivant, le nombre de rangées augmente. Le nombre de colonnes augmente également à certains niveaux. La vitesse des envahisseurs est augmentée selon le niveau.

Le bouton **Main Menu** permet de revenir au menu principal. Après une défaite, `N` permet aussi de recommencer.

### 6. Paramètres audio

L'écran **Settings** permet de modifier le volume de la musique avec les flèches gauche et droite. Le volume est limité entre 0 % et 100 %. La valeur initiale est de 30 %.

## États du jeu

Les états sont définis dans `GameState` :

| État | Description |
|---|---|
| `MAIN_MENU` | Menu principal |
| `GAMEPLAY` | Partie en cours |
| `PAUSE` | Partie suspendue |
| `GAME_OVER` | Victoire ou défaite |
| `SETTINGS` | Paramètres audio |

La méthode `handle_event()` traite les événements selon l'état actif. La méthode `handle_states(dt)` détermine ensuite les mises à jour et les éléments à afficher pour cet état.

## Principes techniques importants

### Boucle principale et temps

La méthode `run()` constitue la boucle principale. À chaque itération, elle :
1. calcule le temps écoulé depuis l'image précédente (`dt`);
2. récupère les événements Pygame;
3. traite les événements;
4. met à jour et dessine l'état courant;
5. actualise l'affichage.

Le temps `dt` est utilisé dans les déplacements et les animations afin de rendre leur vitesse moins dépendante du nombre d'images par seconde.

### Groupes de sprites

Le projet utilise plusieurs groupes Pygame pour organiser les objets :
- `all_sprites`;
- `player_group`;
- `invader_sprites`;
- `player_lasers`;
- `invader_lasers`.

Ces groupes facilitent les mises à jour, l'affichage et les vérifications de collisions.

### Minuteurs

`GameTimer` mesure le temps à partir de `pygame.time.get_ticks()`. Il est notamment utilisé pour limiter la fréquence des tirs et imposer un délai initial aux tirs des envahisseurs.

### Importation des ressources

Les fonctions de `support.py` centralisent le chargement :
- `aspect_ratio()` redimensionne une image en conservant ses proportions;
- `import_frames()` importe une séquence d'images numérotées;
- `audio_importer()` charge les fichiers audio d'un dossier dans un dictionnaire.

## Améliorations possibles

Ces idées ne sont pas encore implémentées dans le code analysé :
- ajouter un fichier `requirements.txt` pour documenter les dépendances;
- ajouter un écran de commandes ou une aide accessible depuis le menu;
- sauvegarder le meilleur score;
- ajouter des sons et des animations supplémentaires;
- séparer davantage la logique de jeu, l'interface et la gestion des ressources;
- ajouter des tests pour les règles de score, les dégâts et la progression des niveaux.

## Résumé

Space Invader est un projet Python/Pygame organisé autour d'une classe principale `Game`, de classes de sprites et de modules utilitaires. Il met en pratique la boucle de jeu, la gestion des événements, les états, les groupes de sprites, les collisions, les animations, les minuteries et l'audio. Le joueur doit éliminer les envahisseurs, accumuler des points et progresser à travers des niveaux de difficulté croissante.
