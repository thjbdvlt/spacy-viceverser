import spacy.parts_of_speech
from spacy import Language


POS_DEFAULT_PRIORITY = [
    "pron",
    "det",
    "cconj",
    "sconj",
    "aux",
    "verb",
    "noun",
]

POS_SIMILARITIES = {
    "aux": ["verb"],
    "verb": ["aux", "adj", "noun"],
    "noun": ["adj", "verb"],
    "adj": ["noun", "verb"],
    "det": ["cconj", "sconj", "pron", "adp"],
    "pron": ["det", "cconj", "sconj", "adp"],
}


def default_list(nlp: Language) -> dict:
    """Récupère la liste des upos possibles."""

    postags = list(
        set([v.lower() for v in spacy.parts_of_speech.NAMES.values()])
    )
    priorities = list_pos_priorities(
        postags=postags,
        similarities=POS_SIMILARITIES,
        default_priority=POS_DEFAULT_PRIORITY,
    )
    return priorities


def list_pos_priorities(
    postags: list, similarities: dict, default_priority: list
) -> dict:
    """Construit un dictionnaire de proximitié des POS tags.

    Args:
        similarities (dict):  un dictionnaire qui attribue, à chaque pos-tag une liste de pos-tags proches.
        default_priority (list):  une liste de priorités par défault qui sera utilisée pour compléter `similarities`.

    Exemple:
        similarities={"verb": ["aux"], "cconj": ["sconj", "det"]}
        default_priority=["noun", "verb", "pron"]

    Aucune des deux liste n'a besoin d'être exhaustive. elle sera complétée par les tags possibles (récupérée dans les labels du morphologizer).
    """
    default_priority.extend(
        [i for i in postags if i not in default_priority]
    )
    for tag in default_priority:
        if tag in similarities.keys():
            prio = similarities[tag]
            missing = [i for i in default_priority if i not in prio]
            prio.extend(missing)
        else:
            prio = default_priority
        # Chaque tag est le premier de sa propre liste.
        prio.remove(tag)
        prio.insert(0, tag)
        # Combinaison ('adp', [tag]), utilisée pour les mots composés.
        # 'adp' est le premier de la liste, suivi de la liste associée au tag.
        similarities[("adp", tag)] = ["adp"] + [
            i for i in prio if i != "adp"
        ]
        similarities[tag] = prio
    return similarities
