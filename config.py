# config.py — Définition de l'univers ESIEE Bug dans la Matrice

from item import Item
from character import Character

DEBUG = False

# --- Définition des salles ---
rooms_config = {
    "rue": {
        "name": "La Rue",
        "description": "dans La Rue, le grand couloir de l’ESIEE, qui semble s’étendre à l’infini entre plusieurs réalités.",
        "exits": {
            "n": "amphi_md",
            "s": "bde",
            "e": "salle_blanche",
            "o": "bu"
        },
        "items": [],
        "pnj": []
    },

    "amphi_md": {
        "name": "Amphi MD",
        "description": "dans l’Amphi MD où un prof répète la même diapo quantum… mais avec des résultats différents.",
        "exits": {
            "s": "rue",
            "e": "3142"
        },
        "items": ["slide_quantique"],
        "pnj": ["prof_glitch"]
    },

    "salle_blanche": {
        "name": "Salle Blanche",
        "description": "dans la salle blanche, baignée d’une lumière irréelle. Les machines bourdonnent comme si elles parlaient.",
        "exits": {
            "o": "rue",
            "n": "b_de_courivaud"
        },
        "items": ["gants_antisurvol"],
        "pnj": ["technicien_multivers"]
    },

    "3142": {
        "name": "Salle 3142",
        "description": "dans la salle 3142, où les étudiants de tous les univers rendent un projet différent du même sujet.",
        "exits": {
            "o": "amphi_md",
            "s": "je"
        },
        "items": ["rapport_bugge"],
        "pnj": ["etudiant_panique"]
    },

    "bde": {
        "name": "BDE Multivers",
        "description": "dans le BDE, où trois versions parallèles du bureau se disputent la cafetière unique.",
        "exits": {
            "n": "rue"
        },
        "items": ["cafe_douteux"],
        "pnj": ["bde_alpha", "bde_omega"]
    },

    "je": {
        "name": "Junior Entreprise",
        "description": "dans la Junior Entreprise, fragmentée en 12 dimensions, chaque version réclame sa facture.",
        "exits": {
            "n": "3142",
            "o": "assistetud"
        },
        "items": ["cle_usb_patch"],
        "pnj": ["consultant_quantique"]
    },

    "b_de_courivaud": {
        "name": "Bureau de Courivaud",
        "description": "devant le bureau de M. Courivaud, verrouillé par un paradoxe pédagogique.",
        "exits": {
            "s": "salle_blanche",
            "e": "self"
        },
        "items": [],
        "pnj": ["courivaud_illusoire"]
    },

    "bu": {
        "name": "BU",
        "description": "à la BU, où les livres lévitent selon leur taux de retard.",
        "exits": {
            "e": "rue"
        },
        "items": ["manuel_vivant"],
        "pnj": ["bibliothecaire_spectral"]
    },

    "assistetud": {
        "name": "AssistEtud",
        "description": "dans le bureau AssistEtud, où un formulaire A38 flotte dans un vortex administratif.",
        "exits": {
            "e": "je"
        },
        "items": ["formulaire_A38"],
        "pnj": ["agent_multivers"]
    },

    "self": {
        "name": "Self",
        "description": "au self, où les plateaux se déplacent seuls comme des robots vaguement conscients.",
        "exits": {
            "o": "b_de_courivaud"
        },
        "items": ["sandwich_glitch"],
        "pnj": ["chef_autonome"]
    }
}

# --- ITEMS ESIEE ---
items_config = {
    "cafe_douteux": Item("café douteux", "Un café qui transcende l’espace-temps. +10 énergie, +2 stress.", 1),
    "cle_usb_patch": Item("clé USB patchée", "Une clé indispensable pour recoder le Super-Planning.", 1),
    "slide_quantique": Item("slide quantique", "Une diapo qui change à chaque lecture.", 1),
    "gants_antisurvol": Item("gants antisurvol", "Empêchent les objets de léviter quand ils ne devraient pas.", 1),
    "rapport_bugge": Item("rapport buggé", "Il est marqué 'version finale V1.0.4b PROJET DEFINITIF', barré 8 fois.", 1),
    "manuel_vivant": Item("manuel vivant", "Le livre respire. Littéralement.", 2),
    "formulaire_A38": Item("formulaire A38", "Un document maudit issu du chaos administratif.", 0),
    "sandwich_glitch": Item("sandwich glitch", "Il change de goût selon l'univers.", 1),
}

# --- PNJ ---
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
    "courivaud_illusoire": Character("Courivaud Illusoire", "projection pédagogique fluctuante.",
                                     ["'Est-ce que tu as PENSÉ à lire l'énoncé… dans toutes les réalités parallèles ?'"]),
    "bibliothecaire_spectral": Character("Bibliothécaire Spectral", "gardienne des livres conscients.",
                                         ["'Silence. Les livres dorment.'"]),
    "agent_multivers": Character("Agent AssistEtud", "maître absolu des formulaires.",
                                 ["'Il manque le justificatif *inter-univers*.'"]),
    "chef_autonome": Character("Chef Autonome", "robot cuisinier libre depuis le 12e big bang.",
                               ["'Nouvelle recette : pâtes quantiques aux fractales comestibles.'"])
}


