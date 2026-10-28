# src/service/progressao_graus.py
from sqlalchemy.orm import Session
from src.model import Acorde, Nota

GRAUS_MAIOR = {
    0: "I", 1: "bII", 2: "II", 3: "bIII", 4: "III", 5: "IV",
    6: "#IV", 7: "V", 8: "bVI", 9: "VI", 10: "bVII", 11: "VII"
}
GRAUS_MENOR = {0: "i", 2: "ii", 3: "III", 5: "iv", 7: "v", 8: "VI", 10: "VII"}

def converter_para_grau(db: Session, nome_cifra: str, tom: str) -> str:
    """Converte um acorde para seu grau relativo em romano consultando o pitch_class no banco."""
    if not tom:
        return nome_cifra

    tom_limpo = tom.strip()
    eh_menor_tom = tom_limpo.endswith("m")
    nome_tonica_tom = tom_limpo[:-1] if eh_menor_tom else tom_limpo

    equivalencias_bemol = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}
    nome_tonica_tom = equivalencias_bemol.get(nome_tonica_tom, nome_tonica_tom)

    nota_tom = db.query(Nota).filter(Nota.nome == nome_tonica_tom).first()
    if not nota_tom:
        return nome_cifra

    acorde = db.query(Acorde).filter(Acorde.nome_cifra == nome_cifra).first()
    if not acorde or not acorde.nota_fundamental:
        return nome_cifra

    pitch_tom = nota_tom.pitch_class
    pitch_acorde = acorde.nota_fundamental.pitch_class

    intervalo = (pitch_acorde - pitch_tom) % 12

    tabela_graus = GRAUS_MENOR if eh_menor_tom else GRAUS_MAIOR
    grau_base = tabela_graus.get(intervalo, nome_cifra)

    # Preserva o sufixo de sétima se houver (ex: V7, VIm7)
    if "7" in acorde.nome_cifra and "7" not in grau_base:
        grau_base += "7"
    elif "maj7" in acorde.nome_cifra:
        grau_base += "maj7"

    return grau_base

def gerar_progressao_relativa(db: Session, acordes: list[str], tom: str | None) -> str:
    """Gera a string da progressão relativa em graus romanos."""
    if not tom:
        return " ".join(acordes)
    
    graus = [converter_para_grau(db, acorde, tom) for acorde in acordes]
    return " ".join(graus)