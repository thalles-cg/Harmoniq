from src.database import SessionLocal
from src.service.importacao_musica import importar_musica

def main():
  print("=== Importador de músicas HarmoniQ ===")

  titulo = input("Título: ").strip()
  artista = input("Artista: ").strip()

  print("\nInforme os acordes separados por espaços.")
  print("Exemplo: C Am F G C G Am F")

  entrada = input("\nAcordes: ").strip()
  acordes = entrada.split()

  db = SessionLocal()

  try:
    musica = importar_musica(
      db=db,
      titulo=titulo,
      artista_nome=artista,
      acordes=acordes,
    )

    print(f"\nMúsica cadastrada com sucesso!")
    print(f"ID: {musica.id}")
    print(f"Título: {musica.titulo}")
    print(f"Artista: {artista}")
    print(f"Total de acordes: {len(acordes)}")

  except ValueError as erro:
    print(f"\nErro: {erro}")

  finally:
    db.close()


if __name__ == "__main__":
  main()
