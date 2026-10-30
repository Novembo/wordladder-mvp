"""Dictionary downloading, filtering, and frequency processing."""
from __future__ import annotations

import logging
import unicodedata
import httpx

logger = logging.getLogger(__name__)

DICTIONARY_SOURCES = {
    "en": "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt",
    "fr": "https://raw.githubusercontent.com/chrplr/openlexicon/master/datasets-info/Liste-de-mots-francais-Gutenberg/liste.de.mots.francais.frgut.txt",
    "es": "https://raw.githubusercontent.com/javierarce/palabras/master/listado-general.txt",
}

STARTER_VOCABULARY = {
    "en": [
        "cold", "cord", "card", "ward", "warm", "worm", "word", "wood", "wool",
        "fool", "food", "foot", "fort", "form", "farm", "firm", "fire", "five",
        "live", "line", "lone", "bone", "bane", "bank", "bark", "dark", "dart",
        "part", "past", "post", "host", "most", "cost", "cast", "case", "cave",
        "gave", "gate", "hate", "date", "data", "head", "lead", "load", "boat",
        "coat", "chat", "that", "what", "wait", "bait", "ball", "fall", "tall",
        "tell", "hell", "bell", "belt", "best", "rest", "rust", "dust", "dusk",
        "cat", "bat", "rat", "hat", "hot", "pot", "dot", "dog", "log", "leg",
        "play", "plan", "plat", "plot", "slot", "slow", "show", "shoe", "shop",
        "star", "stay", "step", "stop", "stem", "seen", "seed", "feed",
        "teach", "peach", "reach", "beach", "bench", "bunch", "punch", "pinch",
        "ladder", "leader", "loader", "louder", "folder", "holder", "golden",
        "game", "came", "fame", "name", "same", "tame", "time", "lime", "dime",
        "ride", "side", "tide", "wide", "hide", "hire", "wire", "tire", "sire",
        "sing", "ring", "wing", "king", "ping", "pink", "sink", "link", "wink",
        "walk", "talk", "balk", "bulk", "bull", "bill", "pill", "will", "well",
        "road", "toad", "load", "loud", "lord", "cord", "cork", "pork", "fork"
    ],
    "fr": [
        "chat", "char", "cher", "chez", "chef", "clef", "bleu", "bloc", "troc",
        "bras", "gris", "gros", "gras", "gens", "dent", "vent", "vert", "vers",
        "pere", "mere", "mare", "gare", "page", "sage", "cage", "nage", "nageur",
        "pain", "bain", "main", "marin", "matin", "latin", "lapin", "ravin",
        "jour", "four", "tour", "cour", "pour", "peur", "leur", "loup", "coup",
        "lire", "rire", "dire", "cire", "pire", "pore", "port", "fort", "sort",
        "arbre", "ambre", "ombre", "timbre", "tombe", "bombe", "bonne", "donne",
        "mot", "mots", "mets", "mers", "vers", "vins", "pins", "pont", "font",
        "soleil", "sommeil", "plante", "plat", "plan", "elan", "clan", "clos",
        "porte", "poste", "piste", "liste", "juste", "buste", "balle", "bulle",
        "belle", "selle", "telle", "ville", "mille", "fille", "grille", "brille",
        "aime", "rame", "dame", "lame", "game", "gare", "gare", "rare", "tare",
        "bras", "banc", "blanc", "franc", "flanc", "flamme", "femme", "pomme"
    ],
    "es": [
        "casa", "cama", "cana", "cara", "cero", "pero", "pera", "pata", "pala",
        "hola", "hora", "hoja", "roja", "ropa", "copa", "sopa", "sol", "sal",
        "mar", "mas", "mes", "pez", "paz", "pan", "van", "ven", "ver", "dar",
        "gato", "pato", "paso", "vaso", "voto", "moto", "mono", "mano", "rayo",
        "vino", "pino", "fino", "filo", "kilo", "hilo", "hielo", "cielo", "suelo",
        "libro", "libre", "nieve", "nueve", "nuevo", "huevo", "fuego", "juego",
        "vida", "viva", "onda", "moda", "boda", "boca", "roca", "foca", "loca",
        "mesa", "misa", "risa", "tasa", "masa", "mapa", "capa", "papa", "pipa",
        "rojo", "ojo", "oso", "oro", "ola", "ala", "amo", "año", "aro", "era"
    ],
}


def strip_accents(text: str) -> str:
    """Normalize unicode and strip diacritical marks."""
    normalized = unicodedata.normalize("NFD", text.strip().lower())
    return "".join(c for c in normalized if unicodedata.category(c) != "Mn")


def clean_word(raw: str, min_len: int = 3, max_len: int = 8) -> str | None:
    """Validate and clean word: ascii alphabetic only, matching length limits."""
    w = strip_accents(raw)
    if not w.isalpha() or not w.isascii():
        return None
    if len(w) < min_len or len(w) > max_len:
        return None
    return w


def download_dictionary(lang: str, max_words: int = 8000, timeout: float = 8.0) -> list[str]:
    """Download dictionary with fallback to starter vocab, capped for lightning-fast graph generation."""
    url = DICTIONARY_SOURCES.get(lang)
    words_set: set[str] = set()

    # Always include starter vocabulary for guaranteed rich ladders
    for w in STARTER_VOCABULARY.get(lang, []):
        cleaned = clean_word(w)
        if cleaned:
            words_set.add(cleaned)

    if url:
        try:
            logger.info("Fetching dictionary for %s from %s", lang, url)
            response = httpx.get(url, timeout=timeout, follow_redirects=True)
            if response.status_code == 200:
                count = 0
                for line in response.text.splitlines():
                    cleaned = clean_word(line.strip().partition(",")[0].partition("\t")[0])
                    if cleaned:
                        words_set.add(cleaned)
                        count += 1
                        if count >= max_words:
                            break
                logger.info("Loaded %d words for %s", len(words_set), lang)
        except Exception as exc:
            logger.warning("Could not download %s dictionary: %s. Using starter set.", lang, exc)

    return sorted(words_set)


def partition_levels(words: list[str]) -> dict[str, list[str]]:
    basic: list[str] = []
    intermediate: list[str] = []
    advanced: list[str] = []

    for w in words:
        length = len(w)
        if length <= 4:
            basic.append(w)
        elif length == 5:
            intermediate.append(w)
        else:
            advanced.append(w)

    if not basic:
        basic = list(words)
    if not intermediate:
        intermediate = list(words)
    if not advanced:
        advanced = list(words)

    return {
        "basic": sorted(basic),
        "intermediate": sorted(intermediate),
        "advanced": sorted(advanced),
    }
