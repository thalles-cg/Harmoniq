import re

NOTAS = {
    "C": "C",
    "C#": "C#",
    "Db": "C#",
    "D": "D",
    "D#": "D#",
    "Eb": "D#",
    "E": "E",
    "F": "F",
    "F#": "F#",
    "Gb": "F#",
    "G": "G",
    "G#": "G#",
    "Ab": "G#",
    "A": "A",
    "A#": "A#",
    "Bb": "A#",
    "B": "B",
}

SUFIXOS = {
    "": "",
    "m": "m",
    "7": "7",
    "m7": "m7",
    "6": "6",
    "m6": "m6",
    "7M": "maj7",
    "maj7": "maj7",
    "M7": "maj7",
    "m7M": "m(maj7)",
    "mMaj7": "m(maj7)",
    "dim": "dim",
    "°": "dim",
    "dim7": "dim7",
    "°7": "dim7",
    "aug": "aug",
    "+": "aug",
    "m7(b5)": "m7(b5)",
    "m7b5": "m7(b5)",
    "ø": "m7(b5)",
    "ø7": "m7(b5)",
    "sus2": "sus2",
    "sus4": "sus4",

    # Aliases comuns para acordes suspensos.
    "4": "sus4",
    "2": "sus2",
}

def normalizar_acorde(cifra: str) -> str | None:
    cifra = cifra.strip()
    cifra = cifra.strip(" \t\r\n|,;[]()")

    # Remove o baixo da inversão: C/E -> C.
    cifra = cifra.split("/")[0]

    resultado = re.fullmatch(
        r"([A-G](?:#|b)?)(.*)",
        cifra,
    )

    if resultado is None:
        return None

    fundamental, sufixo = resultado.groups()

    nota = NOTAS.get(fundamental)
    if nota is None:
        return None
    
    qualidade = SUFIXOS.get(sufixo)

    if qualidade is None:
        return None

    return nota + qualidade
