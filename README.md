# Conway's Game of Life avec PyQt

## Table des Matières
- [Description](#description)
- [Fonctionnalités Principales](#fonctionnalités-principales)
- [Découpage du Code, Contraintes et Choix Techniques](#découpage-du-code-contraintes-et-choix-techniques)
  - [1. Architecture Générale](#1-architecture-générale)
  - [2. Grille et Interface Graphique](#2-grille-et-interface-graphique)
  - [3. Calcul de l’Évolution (Règles et Voisinage)](#3-calcul-de-lévolution-règles-et-voisinage)
  - [4. Historique (Undo/Redo)](#4-historique-undoredo)
  - [5. Contraintes et Avertissements](#5-contraintes-et-avertissements)
- [Gestion des Configurations et Motifs](#gestion-des-configurations-et-motifs)
- [Fonctionnalités Graphiques en Détail](#fonctionnalités-graphiques-en-détail)
  - [Barre de Menus (Fichier, Configuration, Édition)](#barre-de-menus-fichier-configuration-édition)
  - [Barre d’Outils (Toolbar)](#barre-doutils-toolbar)
  - [Zone de Contrôles (Panel de Droite)](#zone-de-contrôles-panel-de-droite)
  - [Gestion du Timer et Interactions (Play / Pause / Stop)](#gestion-du-timer-et-interactions-play--pause--stop)
- [Exemple de Flux d’Utilisation](#exemple-de-flux-dutilisation)
- [Prérequis](#prérequis)

---

## Description

Ce projet propose **une implémentation du Jeu de la Vie de Conway** sous la forme d’une application **graphique** développée en **Python** avec **PyQt5**.  

Pensé à l’origine en 1970 par **John Horton Conway**, le Jeu de la Vie est un **automate cellulaire** simple à énoncer mais riche en comportements émergents. Chaque cellule d’une grille  bidimensionnelle est soit vivante, soit morte. Son évolution dépend du nombre de cellules voisines vivantes, d’où émergent toute une variété de patterns fascinants (oscillateurs, vaisseaux glisseurs, structures stables, etc.).

L'état de chaque cellule évolue au fil des générations, selon les règles suivantes :  

1. Une cellule morte devient vivante si elle a **exactement 3** voisines vivantes.  
2. Une cellule vivante reste vivante si elle a **2 ou 3** voisines vivantes.  
3. Dans les autres cas, la cellule meurt (pour cause d’isolement ou de surpopulation).

Ce programme illustre la richesse de comportements pouvant émerger de ces règles (motifs stables, oscillateurs, vaisseaux qui se déplacent, etc.) à travers une **interface ergonomique** et un **panel de contrôle** complet.
Le programme met en valeur cette **richesse** de configurations et vous permet, grâce à une **interface ergonomique**, d’expérimenter ces règles, de charger des motifs célèbres et de contrôler le cycle de vie cellulaire via un **panel de contrôle** complet (Évoluer / Play / Pause / Stop).

---

## Fonctionnalités Principales

- **Interface Graphique PyQt5 :**  
  - Grille de cellules colorées (rouge = vivante, blanc = morte).
  - Menus, barres d’outils, pour le contrôle (boutons pour lancer, arrêter ou réinitialiser la simulation).
 
  - Affichage d’une grille de cellules vivantes (rouge) ou mortes (blanc), avec indices sur la première ligne/colonne.
  - Panel de droite pour paramétrer la simulation.
  - Barre de menus et barre d’outils (icônes) pour gérer la simulation.

- **Grille Personnalisable :**  
  - Réglage du nombre de **lignes** et de **colonnes** via des champs de saisie (limité entre 4 et 50).  
  - Édition Interactive avec la possibilité d’activer ou de désactiver une cellule par simple **clic** (hors mode Play).  
  - Menus pour reconfigurer la grille (générer un motif, créer une grille vide, réinitialiser, etc.).

- **Gestion du Cycle de Vie :**  
  - Bouton **Évoluer** : applique les règles sur un **pas unique**.
  - Mode **Play** :  exécute automatiquement un pas d’évolution toutes les X secondes (avec timer et X défini via un **QSpinBox**).
  - Mode **Pause** : suspend temporairement la simulation.
  - Mode **Stop** : stoppe la simulation et réinitialise la grille.
 
- **Configurations Prédéfinies :**
  - Plusieurs motifs connus (Blinker, Glider, Gosper Glider Gun, R-pentomino, etc.).  
  - Sélection directe depuis un **menu** ou une **combo box**.  

- **Gestion d’Historique (Undo / Redo) :**
  - Gestion de versions successives de la grille.  
  - Revenir en arrière (Undo) ou rétablir un état précédemment annulé (Redo) sur plusieurs générations.  
  - S’appuie sur deux piles d’historique pour naviguer facilement dans les différentes générations.
    
---

## Découpage du Code, Contraintes et Choix Techniques

### 1. Architecture Générale

Le fichier principal est un unique script Python (`jeu_de_la_vie.py`) contenant l’ensemble de la logique et de l’interface et qui regroupe:
- La **classe principale**  `Fenetre(QMainWindow)`, cœur de l’application, hérite de `QMainWindow`.
- Les **fonctions utilitaires** (création de tableau, motifs prédéfinis, etc.).

### 2. Grille et Interface Graphique

- **Grille** : stockée dans une **liste de listes** d’entiers (0 pour mort, 1 pour vivant).  
- **Indices** : la première ligne et la première colonne affichent les coordonnées (i, j).  
- **QGridLayout** : chaque cellule est un `QLabel` coloré selon son état, avec gestion d’un événement de clic pour basculer l’état lorsqu’on est en mode manuel.  
- **QStackedLayout** : permet de jongler entre plusieurs configurations (chaque configuration est un widget).
- **QVBoxLayout** : gère des widgets dédiés au paramétrage de la grille (choisir une configuration, lancer l’évolution manuellement, etc.).

### 3. Calcul de l’Évolution (Règles et Voisinage)

- **nombre_voisins(i, j)** :  
  - Parcourt jusqu’à 8 cellules voisines autour de la cellule (i, j), en prenant garde aux bordures.  
  - Renvoie le nombre total de cellules vivantes autour de (i, j).
    
- **evolution()** :  
  - Calcule un nouveau tableau à partir de l’état actuel, copie chaque cellule en appliquant les règles de Conway.  
  - Évite la modification “en place” en utilisant un `copy.deepcopy` pour ne pas biaiser le décompte des voisins.

  
### 4. Historique (Undo/Redo)

- **Deux Piles d’États** :   
  - `history_stack` : conserve les états passés, pour **Undo**. 
  - `future_stack` : stocke les états annulés, pour **Redo**.  
- **Sauvegarde** : avant chaque évolution manuelle (bouton « Évoluer »), on enregistre l’état actuel dans `history_stack`.  
- **Navigation** : Undo prend la grille courante pour l'empiler dans `future_stack`, puis restaure l’état le plus récent en dépilant `history_stack`. Redo fait l’inverse.

### 5. Contraintes et Avertissements

- **Dimensions min et max** : 4 ≤ lignes, colonnes ≤ 50.  
- **Incompatibilité Cliques / Play / Pause** : le clic sur la grille est désactivé quand la simulation est en mode Play et en mode Pause pour éviter des modifications concurrentes.  
- **Message d’Alerte** : si l’utilisateur fournit des dimensions hors limite, la valeur est automatiquement ajustée et une boîte de dialogue l’avertit.

---

## Gestion des Configurations et Motifs

Plusieurs **motifs** classiques du Jeu de la Vie sont intégrés :  
- **Clignotant (Blinker)**, **R-pentomino**, **Toad**, **Pentadecathlon**, **Glider**, **LWSS**, **Gosper Glider Gun**, **Beacon** et **Pulsar**.  
Chaque fonction renvoie un tableau 2D de taille adaptée et de cellules positionnées pour former le motif.  

**Choix par Menus ou ComboBox** :  
- Menu "Fichier" > "Configuration" pour charger directement un motif.  
- ComboBox "Configuration" (à droite) pour basculer entre Clignotant, R-pentomino, etc.  
- L’option **« Vide »** remet toutes les cellules à 0 pour la taille courante.

---

## Fonctionnalités Graphiques en Détail

### Barre de Menus (Fichier, Configuration, Édition)

- **Menu "Fichier" :**  
  - **Nouveau** : réinitialise la grille selon les dimensions entrées dans la zone de contrôle.  
  - **Configuration (sous-menu)** : charge une configuration prédéfinie (Blinker, Glider, etc.).

- **Menu "Édition" :**  
  - **Play** : lance l’évolution automatique (un QTimer enclenche `evolution()` périodiquement).   
  - **Pause** : suspend temporairement l’évolution sans effacer la grille.
  - **Stop** : arrête définitivement l’évolution et réinitialise la grille.

### Barre d’Outils (Toolbar)

On retrouve 6 icônes principales :

1. **Icône Reset** : réinitialise la grille (équivaut à « Nouveau »).  
2. **Icône Play** : lance l’évolution automatique.  
3. **Icône Pause** : suspend la simulation. 
4. **Icône Stop** : arrête définitivement l'évolution et vide la grille.  
5. **Icône Undo** : annule la dernière évolution.  
6. **Icône Redo** : rétablit un état annulé.

**Raccourcis Clavier** : Ctrl+N, Ctrl+P, Ctrl+Shift+P, Ctrl+S, Ctrl+Z, Ctrl+Y sont également configurés pour un accès rapide.

### Zone de Contrôles (Panel de Droite)

- **ComboBox** : sélection du motif prédéfini souhaité ou « Vide ».
- **QSpinBox** : définit le **délai** (en secondes) entre chaque itération en mode Play. 
- **QLineEdit** : indique le nombre de lignes et de colonnes de la grille souhaité. 
- **Bouton “Évoluer”** : applique un **pas unique** d'évolution (sans timer).
- **Bouton “Reset”** : réinitialise la grille aux dimensions demandées.

### Gestion du Timer et Interactions (Play / Pause / Stop)

- **Play** :
  - Instancie un `QTimer` et exécute `evolution()` toutes les `X` secondes.  
  - Désactive certains contrôles, afin d'éviter des conflits.  
- **Pause** :
  - Arrête temporairement le `QTimer`.
  - L’utilisateur peut faire des Undo/Redo, ou des pas unique supplémentaire via le bouton “Évoluer”.  
- **Stop** :
  - Stoppe définitivement le timer.
  - Vide la grille en recréant un tableau 2D rempli de 0.
  - Réinitialise l’historique.
  - Les contrôles sont réactivés.

---

## Exemple de Flux d’Utilisation

1. **Ouverture de l’application**  
   - Affiche par défaut une grille 15×15 vide, la barre d’outils, la barre de menus et le panel de droite.  
2. **Changement de dimensions**  
   - Vous tapez « 20 » lignes et « 30 » colonnes, puis cliquez sur **Reset** : la grille devient 20×30, vide.
3. **Chargement d’un motif**  
   - Dans la combo box, vous choisissez “Gosper Glider Gun”. Les cellules correspondantes au motif s’affichent automatiquement.  
4. **Évolution manuelle**  
   - Un clic sur le bouton **Évoluer** applique un unique pas d'évolution. L’état précédent est stocké dans l’historique (`history_stack`).
5. **Play / Pause / Undo**  
   - En appuyant sur **Play**, la simulation se déroule automatiquement toutes les X secondes.  
   - Vous pouvez appuyer sur **Pause** pour suspendre l'évolution, puis sur **Undo** pour revenir à un état antérieur si besoin.
6. **Stop**  
   - En appuyant sur **Stop**, la simulation s’interrompt définitivement et la grille est réinitialisée, prête pour expérimenter un nouveau motif ou de nouvelles dimensions.
     
---

## Prérequis

- **Python 3.x** (recommandé : ≥ 3.7).  
- **PyQt5** :  
  ```bash
  pip install PyQt5
