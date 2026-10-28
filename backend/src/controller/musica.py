from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.model import Musica
from src.schema.musica import MusicaCreate, MusicaUpdate
from Levenshtein import distance as levenshtein_distance
from src.service.progressao_graus import gerar_progressao_relativa
import re

from src.service.musica import (
  atualizar_musica,
  buscar_musica,
  buscar_por_repertorio,
  buscar_por_sequencia,
  criar_musica,
  excluir_musica,
  listar_musicas,
)

def criar(db: Session, dados: MusicaCreate) -> Musica:
  musica = criar_musica(db, dados)

  if musica is None:
    raise HTTPException(
      status_code=400,
      detail="Não foi possível criar a música."
    )

  return musica

def listar(db: Session) -> list[Musica]:
  return listar_musicas(db)

def buscar(db: Session, musica_id: int) -> Musica:
  musica = buscar_musica(db, musica_id)

  if musica is None:
    raise HTTPException(
      status_code=404,
      detail="Música não encontrada"
    )

  return musica

def buscar_repertorio(db: Session, nomes_acordes: list[str]) -> list[dict]:
  if not nomes_acordes:
    raise HTTPException(
      status_code=400,
      detail="Informe pelo menos um acorde."
    )

  return buscar_por_repertorio(db, nomes_acordes)

def normalizar_grau(grau: str) -> str:
  """
  Remove extensões de sétimas/extensões temporariamente 
  para permitir correspondência entre V7 e V, se desejado.
  """
  return re.sub(r"(7|maj7|m7|dim|aug|\(b5\))$", "", grau)

def buscar_sequencia(db: Session, graus_busca: list[str], ignorar_setimas: bool = True) -> list[dict]:
  """
  Busca músicas por similaridade local entre progressões relativas (janela deslizante),
  retornando a maior similaridade encontrada e a quantidade de ocorrências do trecho.
  """
  graus_busca_limpos = [grau.strip() for grau in graus_busca if grau.strip()]

  if not graus_busca_limpos:
    raise HTTPException(
      status_code=400,
      detail="Informe pelo menos um grau para pesquisar."
    )

  if ignorar_setimas:
    graus_busca_comparacao = [normalizar_grau(g) for g in graus_busca_limpos]
  else:
    graus_busca_comparacao = graus_busca_limpos

  musicas = (
    db.query(Musica)
    .filter(Musica.progressao_relativa.isnot(None))
    .all()
  )

  resultados = []
  tam_busca = len(graus_busca_comparacao)

  for musica in musicas:
    if not musica.progressao_relativa:
      continue

    progressao_original = musica.progressao_relativa.split()
    
    if ignorar_setimas:
      progressao_musica = [normalizar_grau(g) for g in progressao_original]
    else:
      progressao_musica = progressao_original

    tam_musica = len(progressao_musica)

    if tam_musica == 0:
      continue

    maior_similaridade = 0.0
    ocorrencias_exatas = 0

    # Se a música tem menos acordes que a busca, compara diretamente
    if tam_musica < tam_busca:
      distancia = levenshtein_distance(graus_busca_comparacao, progressao_musica)
      similaridade = (1 - distancia / tam_busca) * 100
      similaridade = max(0.0, similaridade)
      
      if similaridade > 0:
        maior_similaridade = similaridade
        if similaridade >= 100.0:
          ocorrencias_exatas = 1
    else:
      # Percorre a música em janelas do tamanho da busca
      for i in range(tam_musica - tam_busca + 1):
        janela = progressao_musica[i : i + tam_busca]

        distancia = levenshtein_distance(graus_busca_comparacao, janela)
        similaridade_janela = (1 - distancia / tam_busca) * 100

        if similaridade_janela > maior_similaridade:
          maior_similaridade = similaridade_janela

        # Incrementa a contagem APENAS se a sequência for 100% idêntica
        if similaridade_janela >= 100.0:
          ocorrencias_exatas += 1

    if maior_similaridade > 0:
      resultados.append({
        "musica": musica,
        "similaridade": round(maior_similaridade, 2),
        "ocorrencias": ocorrencias_exatas,
      })

  # Ordena primariamente por similaridade (decrescente) e secundariamente por ocorrências (decrescente)
  resultados.sort(
    key=lambda resultado: (resultado["similaridade"], resultado["ocorrencias"]),
    reverse=True
  )

  return resultados

def atualizar(db: Session, musica_id: int, dados: MusicaUpdate) -> Musica:
  musica = atualizar_musica(db, musica_id, dados)

  if musica is None:
    raise HTTPException(
      status_code=404,
      detail="Música não encontrada ou dados inválidos"
    )

  return musica

def excluir(db: Session, musica_id: int) -> None:
  resultado = excluir_musica(db, musica_id)

  if not resultado:
    raise HTTPException(
      status_code=404,
      detail="Música não encontrada"
    )