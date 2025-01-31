import sys
import copy
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QPushButton, QHBoxLayout, \
    QVBoxLayout, QStackedLayout, QComboBox, QSpinBox, QLineEdit, QMenuBar, QAction, QMessageBox, QToolBar, QStatusBar, QFrame
from PyQt5.QtCore import QCoreApplication, QTimer, Qt, QSize
from PyQt5.QtGui import QIntValidator, QIcon


# 1) FONCTIONS DE BASE ET CONFIGURATIONS 

def creer_tableau(n, p):
    """
    Crée et retourne un tableau bidimensionnel (liste de listes)
    de dimensions n x p, initialisé avec des zéros.
    """
    tab = []

    for i in range(n):
        ligne = []

        for j in range(p):
            ligne.append(0)

        tab.append(ligne)

    return tab

def affiche(tab):
    """
    Affiche le tableau passé en paramètre
    (utilisé surtout pour du debug en console).
    """
    for i in range(len(tab)):
        for j in range(len(tab[0])):        

            print(tab[i][j], end="")

        print(end="\n")


# CONFIGURATIONS PRÉDÉFINIES

def clignotant():
    """
    'Blinker' : oscillateur de période 2.
    Taille : 12x12.
    """
    tab = creer_tableau(12, 12)
    for j in range(5, 8):
        tab[6][j] = 1

    return tab

def r_pentomino():
    """
    R-pentomino : motif qui se développe de façon chaotique, puis finit par se stabiliser. 
    Taille : 16x16.
    """
    tab = creer_tableau(16, 16)
    positions = [
        (7, 8),
        (7, 9),
        (8, 7),
        (8, 8),
        (9, 8)
    ]

    for i, j in positions:
        tab[i][j] = 1

    return tab

def toad():
    """
    'Toad' : oscillateur de période 2.
    Taille : 15x15.
    """
    tab = creer_tableau(15, 15)
    positions = [
        (7, 7), (7, 8), (7, 9),
        (8, 6), (8, 7), (8, 8)
    ]

    for i, j in positions:
        tab[i][j] = 1

    return tab

def pentadecathlon():
    """
    Oscillateur de période 15.
    Taille : 20x19.
    """
    tab = creer_tableau(20, 19)
    positions = [
        (9, 7), (9, 12),
        (10, 5), (10, 6), (10, 8), (10, 9), (10, 10), (10, 11), (10, 13), (10, 14),  
        (11, 7), (11, 12)
    ]

    for i, j in positions:
        tab[i][j] = 1

    return tab

def gosper_glider_gun():   
    """
    Gosper Glider Gun : génère des Gliders (période 30).
    Taille : 20x40.
    """
    tab = creer_tableau(20, 40)
    positions = [
        (10, 2), (10, 3), (11, 2), (11, 3),  
        (10, 12), (11, 12), (12, 12),        
        (9, 13), (13, 13),                   
        (8, 14), (14, 14),                   
        (8, 15), (14, 15),                   
        (11, 16),                            
        (9, 17), (13, 17),                   
        (10, 18), (11, 18), (12, 18),        
        (11, 19),                            
        (8, 22), (9, 22), (10, 22),          
        (8, 23), (9, 23), (10, 23),          
        (7, 24), (11, 24),                   
        (6, 26), (7, 26), (11, 26), (12, 26),
        (8, 36), (9, 36), (8, 37), (9, 37)   
    ]

    for i, j in positions:
        tab[i][j] = 1

    return tab

def glider():
    """
    'Glider' : Petit vaisseau se déplaçant en diagonale (période 4).
    Taille : 15x15.
    """
    tab = creer_tableau(15, 15)
    positions = [(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
    for i, j in positions:
        tab[i][j] = 1

    return tab

def lwss():
    """
    LWSS (Lightweight Spaceship): Vaisseau se déplaçant orthogonalement (période 4).
    Taille : 16x18.
    """
    tab = creer_tableau(16, 18)
    positions = [
        (2, 2), (2, 5),
        (3, 6),
        (4, 2), (4, 6),
        (5, 3), (5, 4), (5, 5), (5, 6)
    ]
    
    for i, j in positions:
        tab[i][j] = 1
        
    return tab

def beacon():
    """
    'Beacon' : deux blocs en miroir, oscillateur de période 2.
    Taille : 13x13.
    """
    tab = creer_tableau(13, 13)
    positions = [
        (5, 5), (5, 6),
        (6, 5), (6, 6),
        (7, 7), (7, 8),
        (8, 7), (8, 8)
    ]

    for i, j in positions:
        tab[i][j] = 1

    return tab

def pulsar():
    """
    'Pulsar' : oscillateur de période 3 (12 bras, composés chacun de 3 cellules).
    Taille : 22x22.
    """
    tab = creer_tableau(22, 22)
    positions = [
        # Quadrant supérieur gauche
        (5, 7), (5, 8), (5, 9),
        (7, 5), (7, 10),
        (8, 5), (8, 10),
        (9, 5), (9, 10),
        (10, 7), (10, 8), (10, 9),
        
        # Quadrant supérieur droit
        (5, 13), (5, 14), (5, 15),
        (7, 12), (7, 17),
        (8, 12), (8, 17),
        (9, 12), (9, 17),
        (10, 13), (10, 14), (10, 15),
        
        # Quadrant inférieur gauche
        (12, 7), (12, 8), (12, 9),
        (13, 5), (13, 10),
        (14, 5), (14, 10),
        (15, 5), (15, 10),
        (17, 7), (17, 8), (17, 9),
        
        # Quadrant inférieur droit
        (12, 13), (12, 14), (12, 15),
        (13, 12), (13, 17),
        (14, 12), (14, 17),
        (15, 12), (15, 17),
        (17, 13), (17, 14), (17, 15)
    ]

    for i, j in positions:
        tab[i][j] = 1

    return tab



# 2) CLASSE PRINCIPALE FENETRE (INTERFACE)

class Fenetre(QMainWindow):
    """
    Classe Fenetre : gère l'interface du Jeu de la vie de Conway,
    la logique, les menus, la configuration, etc.
    """
    def __init__(self, tableau):
        super().__init__()

        # ---------- Paramètres de la fenêtre ----------
        self.setWindowTitle("Conway's Game of Life")
        self.setWindowIcon(QIcon("icons/game_icon.png"))
        self.resize(1200, 600)


        # ---------- Attributs de base ----------

        # On récupère un tableau initial (15x15 vide)
        self.tableau = tableau
        self.tableau_init = tableau

        # Pré-création des tableaux de configurations
        self.tableau_clig = clignotant()
        self.tableau_r_pentomino = r_pentomino()
        self.tableau_penta = pentadecathlon()
        self.tableau_gosper_glider_gun = gosper_glider_gun()
        self.tableau_glider = glider()
        self.tableau_lwss = lwss()
        self.tableau_beacon = beacon()
        self.tableau_toad = toad()
        self.tableau_pulsar = pulsar()

        # Pour la saisie du nombre de lignes/colonnes dans les QLineEdit
        self.val_lig = None
        self.val_col = None

        # Booléen pour activer/désactiver les clics
        self.clic_active = True

        # Piles d'historique et de futur
        self.history_stack = []
        self.future_stack = []

        # Initialisation de l'état "Play"
        self.play_bool = False


        # ---------- Layouts principaux (page, combo, etc.) ----------
        self.pageLayout = QHBoxLayout()
        self.pageLayout.setContentsMargins(20, 20, 20, 20)
        self.pageLayout.setSpacing(20)

        self.stackedLayout = QStackedLayout()       # Pour alterner entre différentes grilles
        self.options = QVBoxLayout()
        self.options.setContentsMargins(10, 10, 10, 10)
        self.options.setSpacing(10)
        
        # ---------- Widgets divers (combo, spinbox, lineEdits) ----------
        self.combo = QComboBox()
        self.combo.setToolTip("Sélectionnez une configuration prédéfinie ou videz la grille.")
        self.combo.setStyleSheet("font-size: 14px; border: 1px solid #aaa; border-radius: 5px; padding: 5px; background-color: white;")
        self.combo.setFixedHeight(30)


        self.temps = QSpinBox()
        self.temps.setToolTip("Définissez l'intervalle entre chaque évolution en secondes.")
        self.temps.setMinimum(1)
        self.temps.setMaximum(30)
        self.temps.setSingleStep(1)
        self.temps.setFixedHeight(30)
        self.temps.setStyleSheet("font-size: 14px; border: 1px solid #aaa; border-radius: 5px; padding: 5px; background-color: white; ")


        self.dimensions = QHBoxLayout()
        self.dimensions.setSpacing(5)


        # ---------- Label principal ----------
        self.description = QLabel("Le Jeu de la Vie de Conway")
        self.description.setStyleSheet("font-size: 26px; font-weight: bold; color: #222; padding: 10px;")
        self.description.setAlignment(Qt.AlignCenter)


        # ---------- Barre de menu ----------
        self.menu = self.menuBar()

        # Menu Fichier
        self.nouv_action = QAction(QIcon("icons/nouveau.png"), "Nouveau", self)
        self.nouv_action.triggered.connect(self.nouveau)
        self.nouv_action.setShortcut('Ctrl+N')

        self.menuFichier = self.menu.addMenu("&Fichier")
        self.menuFichier.addAction(self.nouv_action)
        self.menuFichier.addSeparator()

        # Sous-menu Configuration
        self.clig_action = QAction(QIcon("icons/clig.png"), "Clignotant", self)
        self.clig_action.triggered.connect(self.aff_clig)
        self.r_pentomino_action = QAction(QIcon("icons/r_pent.png"), "R-pentomino", self)
        self.r_pentomino_action.triggered.connect(self.aff_r_pentomino)
        self.penta_action = QAction(QIcon("icons/penta.png"), "Pentadecathlon", self)
        self.penta_action.triggered.connect(self.aff_penta)
        self.gosper_glider_gun_action = QAction(QIcon("icons/gosper.png"), "Gosper Glider Gun", self)
        self.gosper_glider_gun_action.triggered.connect(self.aff_gosper_glider_gun)
        self.glider_action = QAction(QIcon("icons/glider.png"),"Glider", self)
        self.glider_action.triggered.connect(self.aff_glider)
        self.lwss_action = QAction(QIcon("icons/lwss.png"), "LWSS", self)
        self.lwss_action.triggered.connect(self.aff_lwss)
        self.beacon_action = QAction(QIcon("icons/beacon.png"), "Beacon", self)
        self.beacon_action.triggered.connect(self.aff_beacon)
        self.toad_action = QAction(QIcon("icons/toad.png"), "Toad", self)
        self.toad_action.triggered.connect(self.aff_toad)
        self.pulsar_action = QAction(QIcon("icons/pulsar.png"), "Pulsar", self)
        self.pulsar_action.triggered.connect(self.aff_pulsar)

        self.Config = self.menuFichier.addMenu(QIcon("icons/configuration.png"), "&Configuration")
        self.Config.addAction(self.clig_action)
        self.Config.addSeparator()
        self.Config.addAction(self.r_pentomino_action)
        self.Config.addSeparator()
        self.Config.addAction(self.penta_action)
        self.Config.addSeparator()
        self.Config.addAction(self.gosper_glider_gun_action)
        self.Config.addSeparator()
        self.Config.addAction(self.glider_action)
        self.Config.addSeparator()
        self.Config.addAction(self.lwss_action)
        self.Config.addSeparator()
        self.Config.addAction(self.beacon_action)
        self.Config.addSeparator()
        self.Config.addAction(self.toad_action)
        self.Config.addSeparator()
        self.Config.addAction(self.pulsar_action)

        # Menu Édition
        self.play_action = QAction(QIcon("icons/play.png"), "Play", self)
        self.play_action.triggered.connect(self.play)
        self.play_action.setShortcut('Ctrl+P')
        self.pause_action = QAction(QIcon("icons/pause.png"), "Pause", self)
        self.pause_action.triggered.connect(self.pause)
        self.pause_action.setShortcut('Ctrl+Shift+P')
        self.stop_action = QAction(QIcon("icons/stop.png"), "Stop", self)
        self.stop_action.triggered.connect(self.stop)
        self.stop_action.setShortcut('Ctrl+S')

        self.menuEdition = self.menu.addMenu("&Édition")
        self.menuEdition.addAction(self.play_action)
        self.menuEdition.addSeparator()
        self.menuEdition.addAction(self.pause_action)
        self.menuEdition.addSeparator()
        self.menuEdition.addAction(self.stop_action)


        # ---------- Barre d’outils ----------
        self.toolbar = QToolBar("Ma toolbar")
        self.toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(self.toolbar)

        self.reset_icon_act = QAction(QIcon("icons/reset.png"), "Reset", self)
        self.reset_icon_act.triggered.connect(self.reset)
        self.reset_icon_act.setToolTip("Reset la Grille.")
        self.toolbar.addAction(self.reset_icon_act)
        self.toolbar.addSeparator()

        self.play_icon_act = QAction(QIcon("icons/play.png"), "Play", self)
        self.play_icon_act.triggered.connect(self.play)
        self.play_icon_act.setToolTip("Lance l'évolution.")                          
        self.toolbar.addAction(self.play_icon_act)
        self.toolbar.addSeparator()

        self.pause_icon_act = QAction(QIcon("icons/pause.png"), "Pause", self)
        self.pause_icon_act.triggered.connect(self.pause)
        self.pause_icon_act.setToolTip("Stoppe temporairement l'évolution.")           
        self.toolbar.addAction(self.pause_icon_act)
        self.toolbar.addSeparator()

        self.stop_icon_act = QAction(QIcon("icons/stop.png"), "Stop", self)
        self.stop_icon_act.triggered.connect(self.stop)
        self.stop_icon_act.setToolTip("Stoppe définitivement l'évolution.")          
        self.toolbar.addAction(self.stop_icon_act)
        self.toolbar.addSeparator()

        self.undo_icon_act = QAction(QIcon("icons/undo.png"), "Undo", self)
        self.undo_icon_act.triggered.connect(self.undo)
        self.undo_icon_act.setToolTip("Annuler la dernière étape.")
        self.undo_icon_act.setShortcut("Ctrl+Z")
        self.undo_icon_act.setEnabled(False)        #Désactivé tant qu’il n’y a pas d’historique
        self.toolbar.addAction(self.undo_icon_act)
        self.toolbar.addSeparator()

        self.redo_icon_act = QAction(QIcon("icons/redo.png"), "Redo", self)
        self.redo_icon_act.triggered.connect(self.redo)
        self.redo_icon_act.setToolTip("Rétablir l'étape annulée.")
        self.redo_icon_act.setShortcut("Ctrl+Y")
        self.redo_icon_act.setEnabled(False)        #Désactivé tant qu’il n’y a pas d’état futur
        self.toolbar.addAction(self.redo_icon_act)
        self.toolbar.addSeparator()


        # ---------- Status Bar ----------
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("✅ Prêt pour l'évolution.")        


        # ---------- Paramètres de la grille et de l’évolution ----------
        self.label1 = QLabel("Configuration de la Grille")
        self.label1.setStyleSheet("font-size: 18px; color: #333;")
        self.label2 = QLabel("Intervalle d'Évolution (en s)")
        self.label2.setStyleSheet("font-size: 18px; color: #333;")
        self.nb_lig = QLabel("Nombre de lignes: ")
        self.nb_lig.setStyleSheet("font-size: 18px; color: #333;")
        self.nb_colon = QLabel("Nombre de colonnes: ")
        self.nb_colon.setStyleSheet("font-size: 18px; color: #333;")

        self.nb_lig_edit = QLineEdit()
        self.nb_lig_edit.setToolTip("Entrez le nombre de lignes de la grille (4-50).")
        self.nb_lig_edit.setMaxLength(2)
        self.nb_lig_edit.setFixedWidth(90)
        self.nb_lig_edit.setFixedHeight(25)
        self.nb_lig_edit.setStyleSheet("font-size: 14px; border: 1px solid #aaa; border-radius: 5px; padding: 5px; background-color: white;")
        self.nb_lig_edit.setValidator(QIntValidator(4, 50))
        self.nb_lig_edit.textChanged.connect(self.text_changed)

        self.nb_col_edit = QLineEdit()
        self.nb_col_edit.setToolTip("Entrez le nombre de colonnes de la grille (4-50).")
        self.nb_col_edit.setMaxLength(2)
        self.nb_col_edit.setFixedWidth(90)
        self.nb_col_edit.setFixedHeight(25)
        self.nb_col_edit.setStyleSheet("font-size: 14px; border: 1px solid #aaa; border-radius: 5px; padding: 5px; background-color: white;")
        self.nb_col_edit.setValidator(QIntValidator(4, 50)) 
        self.nb_col_edit.textChanged.connect(self.text_changed)

        self.dimensions.addWidget(self.nb_lig)
        self.dimensions.addSpacing(3)
        self.dimensions.addWidget(self.nb_lig_edit)
        self.dimensions.addSpacing(60)
        self.dimensions.addWidget(self.nb_colon)
        self.dimensions.addSpacing(3)
        self.dimensions.addWidget(self.nb_col_edit)

        self.lig_col_widget = QWidget()
        self.lig_col_widget.setLayout(self.dimensions)


        # ---------- Boutons Évoluer et Reset ----------
        self.hbox_buttons = QHBoxLayout()
        self.evoluer_btn = QPushButton("Évoluer")
        self.evoluer_btn.setToolTip("Fait évoluer la grille d’un seul pas.")
        self.evoluer_btn.setStyleSheet("font-size: 16px; font-weight: bold; padding: 14px; background-color: #008CBA; color: white; border-radius: 10px;")
        self.evoluer_btn.clicked.connect(self.afficher_evol)  

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setToolTip("Réinitialise la grille selon les dimensions saisies.")
        self.reset_btn.setStyleSheet("font-size: 16px; font-weight: bold; padding: 14px; background-color: #f44336; color: white; border-radius: 10px;")
        self.reset_btn.clicked.connect(self.reset)            

        self.hbox_buttons.addWidget(self.evoluer_btn)
        self.hbox_buttons.addSpacing(20)
        self.hbox_buttons.addWidget(self.reset_btn)
        self.btn_widget = QWidget()
        self.btn_widget.setLayout(self.hbox_buttons)


        # ---------- Ajout des widgets dans "options" ----------
        self.options.addWidget(self.description)
        self.options.addSpacing(35)         
        self.options.addWidget(self.label1)
        self.options.addSpacing(5)
        self.options.addWidget(self.combo)

        self.options.addSpacing(30)
        self.options.addWidget(self.label2)
        self.options.addSpacing(5)
        self.options.addWidget(self.temps)

        self.options.addSpacing(30)
        self.options.addWidget(self.lig_col_widget)

        self.options.addSpacing(30)
        self.options.addWidget(self.btn_widget)
        self.options.addStretch()
        

        # ---------- Configuration de la combo box ----------
        self.combo.addItem("Clignotant")
        self.combo.setItemData(0, "Oscillateur (période 2) appelé aussi «Blinker».", Qt.ToolTipRole)

        self.combo.addItem("R-pentomino")
        self.combo.setItemData(1, "Motif qui évolue de manière chaotique, puis se stabilise.", Qt.ToolTipRole)

        self.combo.addItem("Pentadecathlon")
        self.combo.setItemData(2, "Oscillateur de période 15 (long et fin).", Qt.ToolTipRole)

        self.combo.addItem("Gosper Glider Gun")
        self.combo.setItemData(3, "Canon à Gliders générant des vaisseaux (période 30).", Qt.ToolTipRole)

        self.combo.addItem("Glider")
        self.combo.setItemData(4, "Petit vaisseau se déplaçant en diagonale (période 4).", Qt.ToolTipRole)

        self.combo.addItem("LWSS")
        self.combo.setItemData(5, "Lightweight Spaceship, vaisseau se déplaçant orthogonalement (période 4).", Qt.ToolTipRole)

        self.combo.addItem("Beacon")
        self.combo.setItemData(6, "Oscillateur de période 2 (deux blocs en miroir).", Qt.ToolTipRole)

        self.combo.addItem("Toad")
        self.combo.setItemData(7, "Oscillateur de période 2.", Qt.ToolTipRole)

        self.combo.addItem("Pulsar")
        self.combo.setItemData(8, "Oscillateur de période 3, formant 12 bras composés chacun de 3 cellules.", Qt.ToolTipRole)
        
        self.combo.addItem("Vide")
        self.combo.setItemData(9, "Vide la configuration courante (garde les dimensions).", Qt.ToolTipRole)

        self.combo.activated[str].connect(self.onActivated)


        # ---------- Création des grilles pour chaque config ----------
        #Liste de configurations sous forme de tuples (nom, méthode d'affichage)
        self.configurations = [
            ("Clignotant", self.aff_clig),
            ("R-pentomino", self.aff_r_pentomino),
            ("Pentadecathlon", self.aff_penta),
            ("Gosper Glider Gun", self.aff_gosper_glider_gun),
            ("Glider", self.aff_glider),
            ("LWSS", self.aff_lwss),
            ("Beacon", self.aff_beacon),
            ("Toad", self.aff_toad),
            ("Pulsar", self.aff_pulsar)
        ]

        #Liste des tableaux de configurations
        self.tbs = [
            self.tableau_init,
            self.tableau_clig,
            self.tableau_r_pentomino,
            self.tableau_penta,
            self.tableau_gosper_glider_gun,
            self.tableau_glider,
            self.tableau_lwss,
            self.tableau_beacon,
            self.tableau_toad,
            self.tableau_pulsar
        ]


        #Création et ajout des grilles (pour chaque tableau) à QStackedLayout
        for tab in self.tbs:
            self.tableau = tab
            self.grid = QGridLayout()       #Chaque grille est représentée par un QGridLayout contenu dans un QWidget
            self.grid_widget = QWidget()
            self.grid_widget.setLayout(self.grid)
            self.grid.setSpacing(0)             #supprime l'espace entre chaque case de la grille

            # Remplir la grille : la première ligne/colonne sert d’index
            for i in range(len(self.tableau)):
                for j in range(len(self.tableau[0])):

                    if i == 0:
                        self.coord = QLabel(str(j))
                        self.coord.setStyleSheet("border: 1px solid black")
                        self.grid.addWidget(self.coord, i, j)

                    elif j == 0:
                        self.coord = QLabel(str(i))
                        self.coord.setStyleSheet("border: 1px solid black")
                        self.grid.addWidget(self.coord, i, j)


                    else:
                        self.coord = QLabel("")
                        self.coord.setStyleSheet("border: 1px solid black")
                        self.grid.addWidget(self.coord, i, j)

            self.afficherTableau()      # Coloration initiale
            self.stackedLayout.addWidget(self.grid_widget)      # Ajout au StackedLayout


        # ---------- Disposition globale ----------
        self.pageLayout.addLayout(self.stackedLayout, stretch = 4)

        # Séparateur vertical
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.VLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setStyleSheet("border: 2px solid #CCC;")     

        self.pageLayout.addWidget(self.separator)   
        self.pageLayout.addLayout(self.options, stretch = 1)

        self.widget = QWidget()
        self.widget.setLayout(self.pageLayout)
        self.setCentralWidget(self.widget)


    # 2.1) MÉTHODES D'AFFICHAGE GRILLE
    def afficherTableau(self):     
        """
        Met à jour visuellement la grille (self.grid) en coloriant
        les cellules selon leur état (0 ou 1).
        """
        for i in range(1, len(self.tableau)):
            for j in range(1, len(self.tableau[0])):

                if self.tableau[i][j] == 1:
                    self.coord = QLabel("")
                    self.coord.setStyleSheet("border: 1px solid black; background-color: red")
                    self.coord.mousePressEvent = lambda event, ligne=i, colonne=j: self.clic(ligne, colonne)
                    self.grid.addWidget(self.coord, i, j)

                else:
                    self.coord = QLabel("")
                    self.coord.setStyleSheet("border: 1px solid black; background-color: white")
                    self.coord.mousePressEvent = lambda event, ligne=i, colonne=j: self.clic(ligne, colonne)
                    self.grid.addWidget(self.coord, i, j)

    def nouvel_affichage(self):
        """
        Met à jour la grille en recréant un nouveau QGridLayout
        (self.nouv_grid) puis en l'insérant dans le stackedLayout.
        """
        self.nouv_grid = QGridLayout()
        self.nouv_widget = QWidget()
        self.nouv_widget.setLayout(self.nouv_grid)
        self.nouv_grid.setSpacing(0)        #supprime l'espace entre chaque case de la grille

        # Affichage des indices (ligne 0 et colonne 0) + cellules
        for i in range(len(self.tableau)):
            for j in range(len(self.tableau[0])):

                if i == 0:
                    self.coord = QLabel(str(j))
                    self.coord.setStyleSheet("border: 1px solid black")
                    self.nouv_grid.addWidget(self.coord, i, j)

                elif j == 0:
                    self.coord = QLabel(str(i))
                    self.coord.setStyleSheet("border: 1px solid black")
                    self.nouv_grid.addWidget(self.coord, i, j)

                else:
                    # On convertit la valeur en int pour l'affichage (debug)
                    self.coord = QLabel(str(int(self.tableau[i][j])))
                    self.coord.setStyleSheet("border: 1px solid black")
                    self.nouv_grid.addWidget(self.coord, i, j)


        # Coloration des cellules
        for i in range(1, len(self.tableau)):
            for j in range(1, len(self.tableau[0])):

                if self.tableau[i][j] == 1:
                    self.coord = QLabel("")
                    self.coord.setStyleSheet("border: 1px solid black; background-color: red")
                    self.coord.mousePressEvent = lambda event, ligne=i, colonne=j: self.clic(ligne, colonne)
                    self.nouv_grid.addWidget(self.coord, i, j)

                else:
                    self.coord = QLabel("")
                    self.coord.setStyleSheet("border: 1px solid black; background-color: white")
                    self.coord.mousePressEvent = lambda event, ligne=i, colonne=j: self.clic(ligne, colonne)
                    self.nouv_grid.addWidget(self.coord, i, j)


        # Remplacement de l'ancienne grille par la nouvelle
        old_widget = self.stackedLayout.currentWidget()
        self.stackedLayout.insertWidget(self.index, self.nouv_widget)
        self.stackedLayout.removeWidget(old_widget)
        self.stackedLayout.setCurrentWidget(self.nouv_widget)
        self.grid = self.nouv_grid


    # 2.2) MÉTHODES LIÉES AUX CHAMPS TEXTE ET AU CLIC
    def text_changed(self):
        """
        Récupère le texte des champs lineEdit pour les lignes et colonnes.
        """
        self.val_lig = self.nb_lig_edit.text() 
        self.val_col = self.nb_col_edit.text()  

    def clic(self, ligne, colonne):         
        """
        Gère le clic sur une cellule (inversion de l'état 0->1 ou 1->0).
        """
        if not self.clic_active:
            return

        self.index = self.stackedLayout.currentIndex()
        self.tableau = self.tbs[self.index]

        # Inversion de l’état de la cellule
        self.tableau[ligne][colonne] = 1 - self.tableau[ligne][colonne]

        # Mise à jour de l’affichage
        self.nouvel_affichage()        


    # 2.3) NOMBRE_VOISINS AVANT EVOLUTION
    def nombre_voisins(self, i, j):
        """
        Calcule et retourne le nombre de voisins vivants (état = 1)
        pour la cellule en position (i, j).
        Gère les bords / coins.
        """
        somme = 0

        # Cas général (8 voisins potentiels, n'est collé à aucun bord)
        if 1 < i < len(self.tableau) - 1 and 1 < j < len(self.tableau[0]) - 1: 
            somme += self.tableau[i - 1][j] + self.tableau[i - 1][j + 1] + self.tableau[i - 1][j - 1] + self.tableau[i][j - 1] + \
                     self.tableau[i][j + 1] + self.tableau[i + 1][j] + self.tableau[i + 1][j + 1] + self.tableau[i + 1][j - 1]

        # Bord supérieur (i=1)
        elif i == 1 and 1 < j < len(self.tableau[0]) - 1:
            somme += self.tableau[i][j - 1] + self.tableau[i][j + 1] + self.tableau[i + 1][j - 1] + self.tableau[i + 1][j + 1] + self.tableau[i + 1][j]

        # Bord inférieur (i = len(self.tableau) - 1)
        elif i == len(self.tableau) - 1 and 1 < j < len(self.tableau[0]) - 1:  
            somme += self.tableau[i][j - 1] + self.tableau[i][j + 1] + self.tableau[i - 1][j - 1] + self.tableau[i - 1][j + 1] + self.tableau[i - 1][j]

        # Bord gauche (j=1)
        elif j == 1 and 1 < i < len(self.tableau) - 1:  
            somme += self.tableau[i][j + 1] + self.tableau[i + 1][j + 1] + self.tableau[i - 1][j + 1] + \
                     self.tableau[i - 1][j] + self.tableau[i + 1][j]

        # Bord droit (j = len(self.tableau[0]) - 1)
        elif j == len(self.tableau[0]) - 1 and 1 < i < len(self.tableau) - 1:  
            somme += self.tableau[i][j - 1] + self.tableau[i + 1][j - 1] + self.tableau[i - 1][j - 1] + \
                     self.tableau[i - 1][j] + self.tableau[i + 1][j]

        # Coin haut-gauche
        elif i == 1 and j == 1: 
            somme += self.tableau[i][j + 1] + self.tableau[i + 1][j] + self.tableau[i + 1][j + 1]

        # Coin bas-gauche
        elif i == len(self.tableau) - 1 and j == 1:  
            somme += self.tableau[i][j + 1] + self.tableau[i - 1][j + 1] + self.tableau[i - 1][j]

        # Coin haut-droit
        elif i == 1 and j == len(self.tableau[0]) - 1:  
            somme += self.tableau[i][j - 1] + self.tableau[i + 1][j - 1] + self.tableau[i + 1][j]

        # Coin bas-droit
        elif i == len(self.tableau) - 1 and j == len(self.tableau[0]) - 1:  
            somme += self.tableau[i][j - 1] + self.tableau[i - 1][j - 1] + self.tableau[i - 1][j]

        return somme


    # 2.4) EVOLUTION DU JEU
    def evolution(self):
        """
        Génère le tableau de l’évolution suivante (tableau_evol)
        en appliquant les règles du Jeu de la Vie.
        """
        self.tableau_evol = copy.deepcopy(self.tableau)     #Copie sans que la modification de l'un entraîne la modification de l'autre

        for i in range(1, len(self.tableau)):
            for j in range(1, len(self.tableau[0])):

                self.voisins = self.nombre_voisins(i, j)        

                # Règles de Conway
                if self.tableau[i][j] == 0 and self.voisins == 3:       
                    self.tableau_evol[i][j] = 1

                elif self.tableau[i][j] == 1 and (self.voisins == 2 or self.voisins == 3):
                    pass        # Reste vivante

                else:
                    self.tableau_evol[i][j] = 0


        self.tbs[self.index] = self.tableau_evol

    def afficher_evol(self):        
        """
        Fait évoluer la grille d’un seul pas et réaffiche.
        """
        # Empiler l'état actuel dans l'historique
        self.history_stack.append(copy.deepcopy(self.tableau))

        # Si on empile un état, on peut faire un Undo, mais seulement si on n'est pas en mode "Play"
        if not self.play_bool:
            self.undo_icon_act.setEnabled(True)     # Sinon, laisser Undo désactivé
        

        # Toute nouvelle évolution annule le "futur" (pile de redo)
        self.future_stack.clear()
        self.redo_icon_act.setEnabled(False)

        # On récupère l’index, puis on fait l’évolution
        self.index = self.stackedLayout.currentIndex()     
        self.tableau = self.tbs[self.index]
        self.evolution()
        self.tableau = self.tbs[self.index]
        self.nouvel_affichage()


    # 2.5) MÉTHODES DE CONTRÔLE DU JEU
    def play(self):
        """
        Lance l'évolution automatique (timer) et désactive certains widgets.
        """
        self.play_bool = True
        self.temps.setDisabled(True)
        self.combo.setDisabled(True)
        self.evoluer_btn.setDisabled(True)
        self.reset_btn.setDisabled(True)
        self.menuFichier.setDisabled(True)
        self.play_action.setDisabled(True)
        self.nb_col_edit.setDisabled(True)
        self.nb_lig_edit.setDisabled(True)
        self.clic_active = False        

        self.play_icon_act.setDisabled(True)
        self.reset_icon_act.setDisabled(True)
        self.undo_icon_act.setDisabled(True)
        self.redo_icon_act.setDisabled(True)

        self.timer = QTimer()
        self.interv = self.temps.value()*1000
        self.timer.timeout.connect(self.afficher_evol)
        self.timer.start(self.interv)
        self.statusBar.showMessage("🚀 En cours d'évolution.")

    def pause(self):
        """
        Met l'évolution en pause (arrête le timer).
        """
        self.timer.stop()
        self.play_action.setDisabled(False)
        self.evoluer_btn.setDisabled(False)     # Bouton "Évoluer" réactivé pour faire un step manuel
        self.reset_btn.setDisabled(True)
        self.clic_active = False  
        self.play_icon_act.setDisabled(False)

        # Autoriser Undo/Redo si la pile correspondante n'est pas vide
        self.undo_icon_act.setEnabled(bool(self.history_stack))
        self.redo_icon_act.setEnabled(bool(self.future_stack))

        self.statusBar.showMessage("⏳ Évolution en pause.")

    def stop(self):
        """
        Stoppe définitivement l'évolution (arrête le timer) et
        réinitialise la grille courante avec un tableau vide.
        """
        self.timer.stop()
        self.play_bool = False
        self.temps.setDisabled(False)
        self.combo.setDisabled(False)
        self.evoluer_btn.setDisabled(False)     
        self.reset_btn.setDisabled(False)
        self.menuFichier.setDisabled(False)
        self.play_action.setDisabled(False)
        self.nb_col_edit.setDisabled(False)
        self.nb_lig_edit.setDisabled(False)
        self.play_icon_act.setDisabled(False)
        self.reset_icon_act.setDisabled(False)
        self.clic_active = True 

        # Réinitialiser le tableau de l’index courant
        self.tableau_init = creer_tableau(len(self.tableau), len(self.tableau[0]))  
        self.tableau = self.tableau_init
        self.tbs[0] = self.tableau_init

        # Vider les piles d’historique/futur
        self.history_stack.clear()
        self.future_stack.clear()
        self.undo_icon_act.setEnabled(False)
        self.redo_icon_act.setEnabled(False)

        self.stackedLayout.setCurrentIndex(0)
        self.index = 0
        self.nouvel_affichage()
        self.statusBar.showMessage("🛑 Évolution arrêtée définitivement.")

    def reset(self):
        """
        Reset la grille : si l’utilisateur a saisi des dimensions,
        on crée un tableau de cette taille (en imposant un minimum); sinon on utilise 10x10.
        """
        if self.val_lig and self.val_col:
            lig = int(self.val_lig)
            col = int(self.val_col)
            ajuste = False

            # Imposer les limites minimum et maximum
            if lig < 4:
                lig = 4
                ajuste = True

            elif lig > 50:
                lig = 50
                ajuste = True

            if col < 4:
                col = 4
                ajuste = True

            elif col > 50:
                col = 50
                ajuste = True

            # Création du tableau avec les dimensions ajustées
            self.tableau_init = creer_tableau(lig, col)

            if ajuste:
                QMessageBox.warning(self, "Dimensions Ajustées", "Le nombre de lignes et/ou de colonnes a été ajusté pour être compris entre 4 et 50, afin d'assurer le bon fonctionnement de la grille.")

        else:
            # Si pas de dimensions, définir des valeurs par défaut et avertir l'utilisateur
            self.tableau_init = creer_tableau(10, 10)
            QMessageBox.warning(self, "Valeurs par Défaut", "Aucune valeur entrée pour les dimensions.\nUtilisation des valeurs par défaut : 10 lignes et 10 colonnes.")

        self.tableau = self.tableau_init
        self.tbs[0] = self.tableau_init
        self.stackedLayout.setCurrentIndex(0)
        self.index = 0
        self.nouvel_affichage()

        # On vide l'historique et le futur
        self.history_stack.clear()
        self.future_stack.clear()
        self.undo_icon_act.setEnabled(False)
        self.redo_icon_act.setEnabled(False)

    def nouveau(self):
        """
        Crée une nouvelle grille vierge selon les dimensions saisies (en imposant un minimum),
        sinon 10x10 par défaut.
        """
        self.reset()    # Réutilise la méthode reset pour éviter la duplication de code, car même fonctionnalité

    def undo(self):
        """
        Annule la dernière étape d'évolution.
        """
        if self.history_stack:
            # Déplacer l'état actuel dans la pile "future"
            self.future_stack.append(copy.deepcopy(self.tableau))

            # Récupérer le dernier état historique
            last_state = self.history_stack.pop()

            # Recharger
            self.tableau = last_state
            self.tbs[self.index] = last_state

            # Réafficher
            self.nouvel_affichage()

            # S'il n'y a plus d'états dans l'historique, on désactive Undo
            if not self.history_stack:
                self.undo_icon_act.setEnabled(False)

            # On peut potentiellement faire un Redo, donc on l'active
            self.redo_icon_act.setEnabled(True)

    def redo(self):
        """
        Rétablit un état annulé.
        """
        if self.future_stack:
            # Déplacer l'état actuel dans l'historique
            self.history_stack.append(copy.deepcopy(self.tableau))

            # Reprendre l'état le plus récent de la pile futur
            next_state = self.future_stack.pop()

            # Recharger
            self.tableau = next_state
            self.tbs[self.index] = next_state

            # Réafficher
            self.nouvel_affichage()

            # On peut toujours annuler => Undo activé
            self.undo_icon_act.setEnabled(True)

            # Si plus rien dans futur => on désactive Redo
            if not self.future_stack:
                self.redo_icon_act.setEnabled(False)


    # 2.6) MÉTHODES DE CONFIGURATION
    def charger_config(self, idx, config_func, msg):
        self.tbs[idx] = config_func()
        self.tableau = self.tbs[idx]
        self.stackedLayout.setCurrentIndex(idx)
        self.index = idx
        self.nouvel_affichage()
        self.statusBar.showMessage(msg)

    def aff_clig(self):
        self.charger_config(1, clignotant, "Configuration Clignotant sélectionnée.")

    def aff_r_pentomino(self):
        self.charger_config(2, r_pentomino, "Configuration R-pentomino sélectionnée.")

    def aff_penta(self):
        self.charger_config(3, pentadecathlon, "Configuration Pentadecathlon sélectionnée.")

    def aff_gosper_glider_gun(self):
        self.charger_config(4, gosper_glider_gun, "Configuration Gosper Glider Gun sélectionnée.")

    def aff_glider(self):
        self.charger_config(5, glider, "Configuration Glider sélectionnée.")

    def aff_lwss(self):
        self.charger_config(6, lwss, "Configuration LWSS sélectionnée.")

    def aff_beacon(self):
        self.charger_config(7, beacon, "Configuration Beacon sélectionnée.")

    def aff_toad(self):
        self.charger_config(8, toad, "Configuration Toad sélectionnée.")
    
    def aff_pulsar(self):
        self.charger_config(9, pulsar, "Configuration Pulsar sélectionnée.")


    # 2.7) MÉTHODE onActivated (combo box)
    def onActivated(self, text):                
        """
        Action déclenchée lorsque l'utilisateur choisit un item dans la combo box.
        """
        if text == "Vide":
            # Vide la configuration courante tout en conservant la même taille
            self.index = self.stackedLayout.currentIndex()
            current_tableau = self.tbs[self.index]
            self.tbs[self.index] = creer_tableau(len(current_tableau), len(current_tableau[0]))
            self.tableau = self.tbs[self.index]
            self.nouvel_affichage()

        else:
            # Itérer sur la liste des configurations pour trouver et appeler la méthode appropriée
            for config_text, config_method in self.configurations:
                if text == config_text:
                    config_method()
                    break

        # On vide l'historique et le futur
        self.history_stack.clear()
        self.future_stack.clear()
        self.undo_icon_act.setEnabled(False)
        self.redo_icon_act.setEnabled(False)


# 3) PROGRAMME PRINCIPAL : CRÉATION DE L'APPLICATION
app = QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)

# Grille par défaut au lancement : 15 x 15
tableau_initial = creer_tableau(15, 15)

window = Fenetre(tableau_initial)
window.show()

app.exec_()
