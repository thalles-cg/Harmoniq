import re
from src.service.normalizacao_acorde import normalizar_acorde

def extrair_acordes(texto: str) -> list[str]:
  acordes = []

  for linha in texto.splitlines():
    linha = linha.strip()

    if not linha:
      continue

    # Ignora marcações como [Intro], [Refrão].
    if linha.startswith("[") and linha.endswith("]"):
      continue

    # Remove marcações iniciais como [Intro] C Am F G.
    linha = re.sub(r"^\[[^\]]+\]\s*", "", linha)

    elementos = linha.split()

    if not elementos:
      continue

    encontrados = []
    linha_valida = True

    for elemento in elementos:
      acorde = normalizar_acorde(elemento)

      if acorde is None:
        linha_valida = False
        break

      encontrados.append(acorde)

    # Só considera linhas compostas inteiramente por acordes.
    # Isso reduz a chance de interpretar palavras como cifras.
    if linha_valida:
      acordes.extend(encontrados)

  return acordes
