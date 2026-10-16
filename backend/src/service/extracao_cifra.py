import re
from collections import defaultdict
from dataclasses import dataclass, field
from src.service.normalizacao_acorde import normalizar_acorde

@dataclass
class ResultadoExtracao:
    acordes: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)
    interrupcoes: list[int] = field(default_factory=list)
    acordes_posicionados: list[tuple[int, str]] = field(default_factory=list)

def parece_cifra(elemento: str) -> bool:
    """
    Verifica se o elemento tem aparência de cifra,
    mesmo que sua qualidade não seja suportada.
    """
    return bool(
        re.fullmatch(
            r"[A-G](?:#|b)?"
            r"(?:(?:maj|min|m|dim|aug|sus|add|M|°|º|ø|"
            r"\d+|#|b|\(|/|\+|-).*)?",
            elemento,
            flags=re.IGNORECASE,
        )
    )

def eh_tablatura(linha: str) -> bool:
    """
    Identifica linhas de tablatura, como:
    E|-----0-----|
    B|---1---1---|
    """
    return bool(
        re.match(
            r"^[eBGDAE]\s*\|",
            linha,
            flags=re.IGNORECASE,
        )
    )

def remover_anotacoes(linha: str) -> str:
    """
    Remove observações entre parênteses que não sejam
    cifras ou extensões de cifras.
    """

    def tratar_parenteses(match: re.Match) -> str:
        conteudo = match.group(1).strip()

        # Preserva extensões como (b5), (#9), (13-), (5-).
        if re.fullmatch(
            r"(?:b|#)?\d+[+-]?",
            conteudo,
            flags=re.IGNORECASE,
        ):
            return match.group(0)

        # Preserva grupos que parecem conter somente cifras.
        elementos = conteudo.split()

        if elementos and all(
            parece_cifra(elemento) for elemento in elementos
        ):
            return match.group(0)

        return " "

    return re.sub(r"\(([^)]*)\)", tratar_parenteses, linha)


def extrair_acordes(texto: str) -> ResultadoExtracao:
    resultado = ResultadoExtracao()
    ocorrencias_invalidas = defaultdict(list)

    posicao = 0
    pular_proxima_linha = False

    for numero_linha, linha_original in enumerate(
        texto.splitlines(),
        start=1,
    ):
        linha = linha_original.strip()

        if not linha:
            continue

        # Identifica linhas que iniciam blocos de tablatura,
        # como "Parte 1 de 4".
        if re.fullmatch(
            r"Parte\s+\d+\s+de\s+\d+",
            linha,
            flags=re.IGNORECASE,
        ):
            pular_proxima_linha = True
            continue

        # Ignora a linha com os nomes dos acordes que aparece
        # imediatamente após "Parte X de Y".
        if pular_proxima_linha:
            pular_proxima_linha = False
            continue

        # Identifica cabeçalhos de seção.
        cabecalho = re.match(r"^\[([^\]]+)\]", linha)

        if cabecalho:
            nome_secao = cabecalho.group(1).lower()

            # Ignora somente o próprio cabeçalho de tablatura.
            # As linhas seguintes serão analisadas normalmente.
            if any(
                termo in nome_secao
                for termo in ("dedilhado", "tablatura", "tab -")
            ):
                continue

            # Remove o cabeçalho e preserva conteúdo posterior.
            linha = re.sub(
                r"^\[[^\]]+\]\s*",
                "",
                linha,
            ).strip()

        if not linha:
            continue

        # Ignora linhas de tablatura propriamente ditas.
        if eh_tablatura(linha):
            continue

        # Expande repetições como (2x).
        repeticoes = 1

        repeticao = re.search(
            r"\(\s*(\d+)\s*x\s*\)\s*$",
            linha,
            flags=re.IGNORECASE,
        )

        if repeticao:
            repeticoes = int(repeticao.group(1))
            linha = linha[:repeticao.start()].strip()

            if not 1 <= repeticoes <= 16:
                resultado.avisos.append(
                    f"Linha {numero_linha}: repetição fora do limite."
                )
                continue

        # Remove parênteses externos que envolvem uma sequência inteira
        # de cifras, como: ( Em7(5-) A7(13-) ).
        linha_sem_parenteses = linha.strip()

        if (
            linha_sem_parenteses.startswith("(")
            and linha_sem_parenteses.endswith(")")
        ):
            conteudo = linha_sem_parenteses[1:-1].strip()

            elementos_internos = conteudo.split()

            if elementos_internos and all(
                parece_cifra(elemento)
                for elemento in elementos_internos
            ):
                linha = conteudo

        # Remove observações sem descartar extensões de cifras.
        linha = remover_anotacoes(linha)

        # Remove separadores de compassos e normaliza espaços.
        linha = re.sub(
            r"\|:|:\||\|\|?|\s+",
            " ",
            linha,
        ).strip()

        if not linha:
            continue

        elementos = linha.split()
        
        # Só processa linhas formadas inteiramente por cifras.
        # Isso evita interpretar letras da música como acordes.
        if not all(parece_cifra(elemento) for elemento in elementos):
            continue

        elementos_normalizados = [
            (elemento, normalizar_acorde(elemento))
            for elemento in elementos
        ]

        for repeticao_atual in range(repeticoes):
            for elemento, acorde in elementos_normalizados:
                posicao += 1

                if acorde is None:
                    if repeticao_atual == 0:
                        ocorrencias_invalidas[elemento].append(
                            numero_linha
                        )

                    resultado.interrupcoes.append(posicao)
                    continue

                resultado.acordes.append(acorde)
                resultado.acordes_posicionados.append(
                    (posicao, acorde)
                )

    # Gera avisos para cifras não suportadas.
    for cifra, linhas in sorted(ocorrencias_invalidas.items()):
        linhas_unicas = sorted(set(linhas))

        resultado.avisos.append(
            f"{cifra}: {len(linhas)} ocorrência(s); "
            f"linha(s): {', '.join(map(str, linhas_unicas))}."
        )

    return resultado
