import re
from dataclasses import dataclass, field
from src.service.normalizacao_acorde import normalizar_acorde

@dataclass
class ResultadoExtracao:
  acordes: list[str] = field(default_factory=list)
  avisos: list[str] = field(default_factory=list)

def extrair_acordes(texto: str) -> ResultadoExtracao:
  resultado = ResultadoExtracao()

  for numero_linha, linha_original in enumerate(
    texto.splitlines(), start=1
  ):
    linha = linha_original.strip()

    if not linha:
      continue

    # Ignora títulos de seção isolados.
    if re.fullmatch(r"\[[^\]]+\]", linha):
      continue

    # Remove títulos de seção no início da linha.
    linha = re.sub(r"^\[[^\]]+\]\s*", "", linha)

    if not linha:
      continue

    # Ignora linhas comuns de tablatura.
    if re.match(r"^[eBGDAE]\s*\|[-0-9xhXpPbBrRsS/\\|~^().]*", linha):
      continue

    # Identifica repetição no final da linha.
    repeticoes = 1

    repeticao = re.search(
      r"\(\s*(\d+)\s*x\s*\)$",
      linha,
      flags=re.IGNORECASE,
    )

    if repeticao:
      repeticoes = int(repeticao.group(1))
      linha = linha[:repeticao.start()].strip()

      if repeticoes < 1 or repeticoes > 16:
        resultado.avisos.append(
          f"Linha {numero_linha}: repetição fora do limite."
        )
        continue

    # Remove separadores de compasso.
    linha = re.sub(r"\|:|:\||\|\|?|\s+", " ", linha).strip()

    if not linha:
      continue

    elementos = linha.split()
    acordes_linha = []
    invalidos = []

    for elemento in elementos:
      acorde = normalizar_acorde(elemento)

      if acorde is None:
        invalidos.append(elemento)
      else:
        acordes_linha.append(acorde)

    if not invalidos:
      resultado.acordes.extend(acordes_linha * repeticoes)

    # Avisa somente quando a linha parece uma sequência
    # de acordes, mas contém elementos desconhecidos.
    elif acordes_linha:
      resultado.avisos.append(
        f"Linha {numero_linha}: não interpretada: "
        f"{linha_original.strip()}"
      )

  return resultado
