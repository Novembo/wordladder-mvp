"""Educational synonym and semantic clue service for guiding learners."""
from __future__ import annotations

import logging
import random

logger = logging.getLogger(__name__)

# Curated semantic clues and synonyms for vocabulary guidance
SYNONYMS_DB: dict[str, dict[str, str]] = {
    "fr": {
        "chat": "Félin domestique qui miaule (ou matou)",
        "char": "Véhicule tiré par des chevaux ou char d'assaut",
        "cher": "Qui coûte beaucoup d'argent (ou personne aimée)",
        "chez": "Au domicile de quelqu'un",
        "chef": "Personne qui dirige une équipe ou cuisinier",
        "clef": "Outil pour ouvrir une serrure",
        "bleu": "Couleur du ciel par temps clair",
        "bloc": "Grosse masse solide de pierre ou de bois",
        "bras": "Membre supérieur reliant l'épaule à la main",
        "gris": "Mélange de noir et de blanc",
        "gros": "De taille ou de volume supérieur à la moyenne",
        "gras": "Riche en matière grasse ou graisseux",
        "gens": "Personnes en général",
        "dent": "Organe blanc dans la bouche pour mâcher",
        "vent": "Mouvement de l'air dans l'atmosphère",
        "vert": "Couleur de l'herbe et des feuilles",
        "vers": "Ligne de poésie ou en direction de",
        "pere": "Papa de la famille",
        "mere": "Maman de la famille",
        "mare": "Petite étendue d'eau calme pour les canards",
        "gare": "Station où s'arrêtent les trains",
        "page": "Côté d'une feuille de livre ou jeune valet",
        "sage": "Prudent, calme et raisonnable",
        "cage": "Enclos à barreaux pour animaux ou oiseaux",
        "nage": "Déplacement dans l'eau",
        "pain": "Aliment cuit à base de farine et d'eau",
        "bain": "Immersion dans l'eau pour se laver ou se détendre",
        "main": "Partie du corps humain avec cinq doigts",
        "jour": "Période éclairée entre le lever et le coucher du soleil",
        "four": "Appareil pour cuire le pain ou les gâteaux",
        "tour": "Construction élevée ou promenade circulaire",
        "cour": "Espace découvert entouré de bâtiments",
        "peur": "Sentiment d'inquiétude ou d'angoisse",
        "loup": "Grand carnivore sauvage de la forêt",
        "coup": "Choc brutal ou impact",
        "lire": "Déchiffrer des mots écrits dans un livre",
        "rire": "Manifester sa joie par des éclats sonores",
        "dire": "Exprimer par la parole",
        "port": "Abri pour les bateaux au bord de la mer",
        "fort": "Qui a beaucoup de puissance ou château fort",
        "pont": "Construction permettant de traverser un fleuve",
        "rame": "Aviron pour faire avancer une barque",
        "dame": "Femme adulte respectée",
        "plante": "Végétal avec des feuilles et des racines",
        "plat": "Sans relief ou assiette de cuisine",
        "plan": "Schéma, dessin ou stratégie",
        "porte": "Ouverture pour entrer dans une pièce",
        "piste": "Chemin tracé pour courir ou skier",
        "liste": "Suite de mots ou d'objets notés par écrit",
        "balle": "Objet sphérique pour jouer au tennis ou foot",
        "ville": "Grande agglomération avec des rues et maisons",
    },
    "en": {
        "cold": "Opposite of hot; chilly or freezing",
        "cord": "Thick string, rope, or electric cable",
        "card": "Rectangular piece of paper, game card",
        "ward": "A room in a hospital or to fend off",
        "warm": "Pleasantly heated, not hot and not cold",
        "worm": "Small, long creature that lives in soil",
        "word": "A single distinct meaningful element of speech",
        "wood": "Hard material that trees are made of",
        "wool": "Warm soft fabric made from sheep hair",
        "fool": "A silly person or a court jester",
        "food": "What people and animals eat to live",
        "foot": "The bottom part of your leg used for walking",
        "fort": "A fortified military building or stronghold",
        "form": "Shape, document to fill in, or configuration",
        "farm": "Area of land used for growing crops and animals",
        "firm": "Solid and steady, or a company business",
        "fire": "Flames producing heat, light, and smoke",
        "live": "To be alive or reside in a house",
        "line": "A long narrow mark or row of people",
        "bone": "Hard white part inside vertebrate bodies",
        "bank": "Place where money is kept, or river edge",
        "bark": "Outer skin of a tree, or the sound a dog makes",
        "dark": "Absence of light; nighttime",
        "dart": "Small pointed missile thrown at a target",
        "part": "A piece or section of a whole",
        "past": "Time that has already happened; history",
        "post": "Mail letter, upright pole, or social media message",
        "host": "Person who entertains guests",
        "most": "Greatest in amount or number",
        "cost": "Price of an object or money required",
        "cast": "Throw something or actors in a play",
        "case": "Instance, container, or suitcase",
        "cave": "Natural underground hollow chamber",
        "gate": "Movable barrier in a fence or wall",
        "hate": "Intense feeling of dislike or hostility",
        "date": "Day of the month, or sweet brown palm fruit",
        "head": "Top part of the body with brain and face",
        "lead": "To guide others or heavy metal",
        "boat": "Small water vessel traveling on lakes/rivers",
        "coat": "Warm garment worn outdoors over clothes",
        "chat": "Friendly informal conversation",
        "that": "Referring to a specific thing previously mentioned",
        "what": "Question word used to ask about things",
        "wait": "Stay in place until an event happens",
        "ball": "Round toy used in football, tennis, and games",
        "fall": "Drop downward, or autumn season",
        "tall": "Of great height; opposite of short",
        "bell": "Hollow metal instrument that rings",
        "best": "Highest quality, better than all others",
        "rest": "Relaxation or sleep to regain energy",
        "rust": "Reddish coating formed on iron by oxidation",
        "dust": "Fine dry powder on surfaces",
        "star": "Luminous celestial body in the night sky",
        "stay": "Remain in the same place without leaving",
        "stop": "Cease movement or action immediately",
        "game": "Playful activity or competitive match",
        "came": "Past tense of come",
        "name": "Word by which a person or thing is known",
        "time": "Continuous progress of existence and events",
    },
    "es": {
        "casa": "Edificio para habitar; hogar o vivienda",
        "cama": "Mueble blando para dormir y descansar",
        "cara": "Parte anterior de la cabeza humana; rostro",
        "cero": "Número que representa la ausencia de cantidad",
        "pero": "Conjunción adversativa que indica oposición",
        "pera": "Fruta dulce de forma alargada y jugosa",
        "pata": "Pie y pierna de los animales",
        "pala": "Herramienta plana para excavar tierra",
        "hola": "Saludo amistoso y cordial",
        "hora": "Medida de tiempo de sesenta minutos",
        "hoja": "Parte verde y plana de las plantas",
        "roja": "Color encarnado vivo como la sangre",
        "ropa": "Prendas que usamos para vestirnos",
        "copa": "Vaso con pie para beber vino",
        "sopa": "Plato caliente con caldo y fideos o verduras",
        "gato": "Animal felino doméstico que maúlla",
        "pato": "Ave acuática con pico aplanado y patas palmeadas",
        "paso": "Movimiento que se hace al caminar",
        "vaso": "Recipiente para beber líquidos",
        "voto": "Expresión de opinión o elección en urnas",
        "moto": "Vehículo de dos ruedas con motor",
        "mono": "Primate inteligente o prenda de vestir entera",
        "mano": "Parte del cuerpo que tiene cinco dedos",
        "vino": "Bebida alcohólica que se obtiene de la uva",
        "pino": "Árbol de madera blanca y hojas aciculares",
        "fino": "Delgado, suave o de gran calidad",
        "hielo": "Agua congelada convertida en sólido por el frío",
        "cielo": "Bóveda azul donde se ven las nubes y estrellas",
        "libro": "Conjunto de páginas escritas encuadernadas",
        "libre": "Que tiene libertad y no está preso",
        "nieve": "Agua helada que cae de las nubes en copos",
        "nuevo": "Recién hecho o estrenado por primera vez",
        "huevo": "Cuerpo redondeado que ponen las aves",
        "fuego": "Calor y luz producidos por la combustión",
        "juego": "Actividad divertida para entretenerse y aprender",
        "vida": "Existencia de los seres vivos",
    }
}


def find_hint(current_word: str, available_words: set[str], lang: str) -> dict[str, str | int]:
    """Find a friendly pedagogical hint for one of the valid neighbor moves."""
    if not available_words:
        return {
            "hint_type": "exhausted",
            "word_length": len(current_word),
            "clue": "Attention, aucune autre transformation n'est disponible depuis ce mot !"
        }

    lang_dict = SYNONYMS_DB.get(lang, {})

    # Prioritize available words that have a rich semantic clue
    with_clues = [w for w in available_words if w in lang_dict]
    if with_clues:
        target = random.choice(with_clues)
        clue_text = lang_dict[target]
        return {
            "hint_type": "synonym",
            "word_length": len(target),
            "clue": f"Pense à : « {clue_text} » !"
        }

    # Fallback to structural phonological guidance
    target = random.choice(sorted(available_words))
    # Determine which letter index changed
    diff_index = 0
    for idx, (c1, c2) in enumerate(zip(current_word, target)):
        if c1 != c2:
            diff_index = idx + 1
            break

    return {
        "hint_type": "letter_position",
        "word_length": len(target),
        "clue": f"Essaie de modifier la lettre n°{diff_index} pour trouver un mot valide !"
    }

