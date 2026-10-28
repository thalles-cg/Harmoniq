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
    "4": "sus4",
    "2": "sus2",
    "5": "5",
    "9": "9",
    "m9": "m9"
}

def remover_baixo_inversao(cifra: str) -> str:
    """Remove o baixo de uma inversão, sem cortar barras dentro de parênteses."""
    profundidade = 0

    for indice, caractere in enumerate(cifra):
        if caractere == "(":
            profundidade += 1
        elif caractere == ")":
            profundidade = max(0, profundidade - 1)
        elif caractere == "/" and profundidade == 0:
            return cifra[:indice]

    return cifra


def normalizar_acorde(cifra: str) -> str | None:
    cifra = cifra.strip()
    cifra = cifra.strip(" \t\r\n|,;[]")

    # Exemplos: Fm/C -> Fm; G7(13)/F -> G7(13).
    cifra = remover_baixo_inversao(cifra)

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

    # Padroniza algumas variações de escrita.
    sufixo = sufixo.replace("−", "-")
    sufixo = sufixo.replace("º", "°")

    # Meio diminuto: F#m7(5-) -> F#m7(b5).
    meio_diminuto = re.fullmatch(
        r"m7\s*\(\s*5\s*-\s*\)",
        sufixo,
        flags=re.IGNORECASE,
    )
    if meio_diminuto:
        return nota + "m7(b5)"

    # Acordes dominantes com extensões:
    # D7(9), G7(13), A7(13-), C7(4/9) -> acorde-base 7.
    dominante_estendido = re.fullmatch(
        r"7\s*\([^()]*\)",
        sufixo,
    )
    if dominante_estendido:
        return nota + "7"

    # Acordes menores com extensões:
    # Em7(9) -> Em7; Am7(11) -> Am7.
    menor_estendido = re.fullmatch(
        r"m7\s*\([^()]*\)",
        sufixo,
    )
    if menor_estendido:
        return nota + "m7"

    # Acorde de sétima com quarta suspensa:
    # E4(7) -> Esus4, a aproximação disponível no catálogo.
    if re.fullmatch(r"4\s*\(\s*7\s*\)", sufixo):
        return nota + "sus4"

    if re.fullmatch(r"7\s*\(\s*4\s*\)", sufixo):
        return nota + "7sus4"
    # Outras cifras com extensões entre parênteses não são
    # simplificadas automaticamente.
    # Acordes com sus4 ou extensões tipo 7(4):

    qualidade = SUFIXOS.get(sufixo)

    if qualidade is None:
        return None

    return nota + qualidade
