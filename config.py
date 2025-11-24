# config.py — Définition de l'univers ESIEE Bug dans la Matrice

from item import Item
from character import Character

DEBUG = False

rooms_config = {

    "rue": {
        "name": "La Rue",
        "description": "dans le grand couloir glitché où toutes les timelines se croisent.",
        "exits": {
            "self": "self",
            "amphi_md": "amphi_md",
            "bde": "bde",
            "junior": "junior",
            "salle_blanche": "salle_blanche",
            "salle_3142": "salle_3142",
            "bu": "bu",
            "assistetud": "assistetud",
            "bureau_courivaud": "bureau_courivaud",
            "toit": "toit"
        },
        "items": [],
        "pnj": ["etudiant_panique"]
    },

    "self": {
        "name": "Self",
        "description": "le self où un chef autonome prépare des plats instables.",
        "exits": {
            "rue": "rue"
        },
        "items": ["plateau_glitch"],
        "pnj": ["chef_autonome"]
    },

    "amphi_md": {
        "name": "Amphi MD",
        "description": "dans l'Amphi MD, un prof glitch boucle une démonstration infinie.",
        "exits": {
            "rue": "rue"
        },
        "items": ["slide_quantique"],
        "pnj": ["prof_glitch"]
    },

    "bde": {
        "name": "BDE",
        "description": "au BDE, deux versions parallèles se disputent une cafetière.",
        "exits": {
            "rue": "rue"
        },
        "items": ["cafe_douteux"],
        "pnj": ["bde_alpha", "bde_omega"]
    },

    "junior": {
        "name": "Junior Entreprise",
        "description": "à la Junior Entreprise, un consultant multidimensionnel t’observe.",
        "exits": {
            "rue": "rue"
        },
        "items": ["cle_usb_bug"],
        "pnj": ["consultant_multivers"]
    },

    "salle_blanche": {
        "name": "Salle Blanche",
        "description": "la salle blanche où les composants semblent vivants.",
        "exits": {
            "rue": "rue"
        },
        "items": ["gants_antisurvol"],
        "pnj": ["carte_vivante"]
    },

    "salle_3142": {
        "name": "Salle 3142",
        "description": "salle instable, parfois décalée d'une timeline.",
        "exits": {
            "rue": "rue"
        },
        "items": ["rapport_bugge"],
        "pnj": ["ton_double"]
    },

    "bu": {
        "name": "BU",
        "description": "à la BU, les livres changent de contenu d'une timeline à l'autre.",
        "exits": {
            "rue": "rue"
        },
        "items": ["livre_timeline"],
        "pnj": ["bibliothecaire_quantique"]
    },

    "assistetud": {
        "name": "AssistEtud",
        "description": "le bureau où les formulaires apparaissent et disparaissent.",
        "exits": {
            "rue": "rue"
        },
        "items": ["formulaire_a38"],
        "pnj": ["agent_multivers"]
    },

    "bureau_courivaud": {
        "name": "Bureau de Courivaud",
        "description": "le cœur logique de l'ESIEE multivers.",
        "exits": {
            "rue": "rue",
            "toit": "toit"
        },
        "items": [],
        "pnj": ["courivaud_illusoire"]
    },

    "toit": {
        "name": "Toit",
        "description": "le toit de l'ESIEE, face au Super-Planning quantique.",
        "exits": {
            "bureau_courivaud": "bureau_courivaud"
        },
        "items": [],
        "pnj": ["super_planning"]
    }
}




    """ OBJETS """
items_config = {
    "cafe_douteux": Item("café douteux", "Un café qui transcende l’espace-temps. +10 énergie, +2 stress.", 1),
    "cle_usb_patch": Item("clé USB patchée", "Une clé indispensable pour recoder le Super-Planning.", 1),
    "cle_usb_bug": Item("clé USB bugée", "Une clé USB récupérée sur une timeline instable.", 1),
    "slide_quantique": Item("slide quantique", "Une diapo qui change à chaque lecture.", 1),
    "gants_antisurvol": Item("gants antisurvol", "Empêchent les objets de léviter quand ils ne devraient pas.", 1),
    "rapport_bugge": Item("rapport buggé", "Il est marqué 'version finale V1.0.4b PROJET DEFINITIF', barré 8 fois.", 1),
    "plateau_glitch": Item("plateau glitch", "Un plateau de self qui ne tient pas la même forme partout.", 1),
    "manuel_vivant": Item("manuel vivant", "Le livre respire. Littéralement.", 2),
    "formulaire_a38": Item("formulaire A38", "Un document maudit issu du chaos administratif.", 0),
    "livre_timeline": Item("livre des timelines", "Un livre qui contient plusieurs versions d'un même chapitre.", 1),
    "sandwich_glitch": Item("sandwich glitch", "Il change de goût selon l'univers.", 1),
}

    """ PNJ """
pnj_config = {
    "prof_glitch": Character("Prof Glitch", "prof de physique quantique en boucle temporelle.",
                             ["'Revenons… DHJIWOEFJ… comme je disais…'", "La fonction d’onde… s’effondre…", "Erreur 404 dans la démonstration…"]),
    "technicien_multivers": Character("Technicien Multivers", "réparateur de machines interdimensionnelles.",
                                      ["'Touche à rien, ça pourrait exploser dans une autre réalité.'"]),
    "etudiant_panique": Character("Étudiant Panique", "complètement dépassé.",
                                  ["'Mon projet a été rendu dans un univers où je n’existe même pas.'"]),
    "bde_alpha": Character("Membre BDE α", "chef du BDE dimension Alpha.",
                           ["'La cafetière nous revient de droit !'"]),
    "bde_omega": Character("Membre BDE Ω", "chef du BDE dimension Omega.",
                           ["'Jamais ! Notre soirée en dépend !'"]),
    "consultant_quantique": Character("Consultant Quantique", "facture tout, même les instabilités dimensionnelles.",
                                      ["'Je peux normaliser votre réalité… pour 599€ HT.'"]),
    "consultant_multivers": Character("Consultant Multivers", "consultant multidimensionnel qui facture même les instabilités.",
                                      ["'Je peux normaliser votre réalité… pour 599€ HT.'"]),
    "courivaud_illusoire": Character("Courivaud Illusoire", "projection pédagogique fluctuante.",
                                     ["'Est-ce que tu as PENSÉ à lire l'énoncé… dans toutes les réalités parallèles ?'"]),
    "bibliothecaire_spectral": Character("Bibliothécaire Spectral", "gardienne des livres conscients.",
                                         ["'Silence. Les livres dorment.'"]),
    "bibliothecaire_quantique": Character("Bibliothécaire Quantique", "gardienne des livres conscients et instables.",
                                          ["'Les chapitres migrent, faites attention.'"]),
    "carte_vivante": Character("Carte Vivante", "une carte qui prend vie et se promène.",
                                 ["'Je connais un raccourci… ou pas.'"]),
    "ton_double": Character("Ton Double", "un double de toi-même, légèrement en colère.",
                              ["'Pourquoi as-tu pris mon siège ?'"]),
    "super_planning": Character("Super Planning", "entité omnisciente du planning.",
                                  ["'Toutes les plages horaires sont relatives.'"]),
    "agent_multivers": Character("Agent AssistEtud", "maître absolu des formulaires.",
                                 ["'Il manque le justificatif *inter-univers*.'"]),
    "chef_autonome": Character("Chef Autonome", "robot cuisinier libre depuis le 12e big bang.",
                               ["'Nouvelle recette : pâtes quantiques aux fractales comestibles.'"])
}


