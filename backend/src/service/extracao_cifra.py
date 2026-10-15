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
    Verifica se o elemento tem aparência de símbolo de acorde,
    mesmo que a qualidade ainda não seja suportada.
    """
    return bool(
        re.fullmatch(
            r"[A-G](?:#|b)?"
            r"(?:(?:maj|min|m|dim|aug|sus|add|M|°|ø|"
            r"\d+|#|b|\(|/|\+).*)?",
            elemento,
            flags=re.IGNORECASE,
        )
    )

def extrair_acordes(texto: str) -> ResultadoExtracao:
    resultado = ResultadoExtracao()
    ocorrencias_invalidas = defaultdict(list)
    ignorar_secao = False
    posicao = 0

    for numero_linha, linha_original in enumerate(texto.splitlines(), start=1):
        linha = linha_original.strip()

        if not linha:
            continue

        
        # Detecta o início de uma nova seção.
        cabecalho = re.match(r"^\[([^\]]+)\]", linha)

        if cabecalho:
            nome_secao = cabecalho.group(1).lower()

            ignorar_secao = any(
                termo in nome_secao
                for termo in ("dedilhado", "tablatura", "tab -")
            )

            if ignorar_secao:
                continue

            # Preserva os acordes que aparecem após o cabeçalho.
            linha = re.sub(r"^\[[^\]]+\]\s*", "", linha).strip()

        elif ignorar_secao:
            continue

        if not linha:
            continue


        # Ignora linhas de tablatura.
        if re.match(
            r"^[eBGDAE]\s*\|[-0-9xhXpPbBrRsS/\\|~^().]*",
            linha,
        ):
            continue

        # Reconhece repetições como (2x).
        repeticoes = 1
        repeticao = re.search(
            r"\(\s*(\d+)\s*x\s*\)$",
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

        # Remove separadores de compassos e normaliza espaços.
        linha = re.sub(r"\|:|:\||\|\|?|\s+", " ", linha).strip()
        linha = linha.strip("() ")

        if not linha:
            continue

        elementos = linha.split()

        # Evita extrair palavras comuns das letras das músicas.
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
                        ocorrencias_invalidas[elemento].append(numero_linha)

                    resultado.interrupcoes.append(posicao)
                else:
                    resultado.acordes.append(acorde)
                    resultado.acordes_posicionados.append((posicao, acorde))

    # Agrupa cifras não suportadas.
    for cifra, linhas in sorted(ocorrencias_invalidas.items()):
        linhas_unicas = sorted(set(linhas))

        resultado.avisos.append(
            f"{cifra}: {len(linhas)} ocorrência(s); "
            f"linha(s): {', '.join(map(str, linhas_unicas))}."
        )

    return resultado
