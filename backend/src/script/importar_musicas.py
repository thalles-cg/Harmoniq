from src.database import SessionLocal
from src.service.importacao_musica import importar_musica
from src.service.extracao_cifra import extrair_acordes
from src.service.normalizacao_acorde import normalizar_acorde

def ler_cifra():
  print("\nCole a cifra completa abaixo.")
  print("Digite FIM em uma linha separada para terminar.\n")

  linhas = []

  while True:
    linha = input()

    if linha.strip().upper() == "FIM":
      break

    linhas.append(linha)

  return "\n".join(linhas)

def revisar_acordes(acordes_posicionados, interrupcoes):
  acordes = [acorde for _, acorde in acordes_posicionados]

  while True:
    print("\n=== Progressão identificada ===")
    print(" ".join(acordes))
    print(f"\nTotal: {len(acordes)} acordes")

    if interrupcoes:
      print(
        "\nAtenção: existem posições de acordes não reconhecidos: "
        + ", ".join(map(str, interrupcoes))
      )

    print("\n1 - Confirmar progressão")
    print("2 - Editar progressão")
    print("3 - Cancelar importação")

    opcao = input("\nEscolha: ").strip()

    if opcao == "1":
      return acordes_posicionados, interrupcoes

    elif opcao == "2":
      entrada = input(
        "\nDigite a sequência corrigida, separando os acordes por espaços: "
      ).strip()

      novos_acordes = []
      invalidos = []

      for cifra in entrada.split():
        acorde = normalizar_acorde(cifra)

        if acorde is None:
          invalidos.append(cifra)
        else:
          novos_acordes.append(acorde)

      if invalidos:
        print(
          "\nAcordes não reconhecidos: "
          + ", ".join(invalidos)
        )
        continue

      if not novos_acordes:
        print("\nA progressão não pode ficar vazia.")
        continue

      acordes_posicionados = [
        (posicao, acorde)
        for posicao, acorde in enumerate(
          novos_acordes,
          start=1,
        )
      ]

      acordes = novos_acordes
      interrupcoes = []

    elif opcao == "3":
      return None

    else:
      print("\nOpção inválida.")

def main():
  print("=== Importador de músicas HarmoniQ ===")

  titulo = input("Título: ").strip()
  artista = input("Artista: ").strip()

  if not titulo or not artista:
    print("\nTítulo e artista são obrigatórios.")
    return

  print("\n1 - Informar acordes manualmente")
  print("2 - Colar cifra completa")

  opcao = input("\nEscolha: ").strip()
  tom = None

  if opcao == "1":
    entrada = input("\nAcordes separados por espaços: ")

    acordes = []
    invalidos = []

    for token in entrada.split():
      acorde = normalizar_acorde(token)

      if acorde is None:
        invalidos.append(token)
      else:
        acordes.append(acorde)

    if invalidos:
      print(
        "\nAcordes não reconhecidos: "
        + ", ".join(invalidos)
      )
      return

    if not acordes:
      print("\nInforme pelo menos um acorde.")
      return

    acordes_posicionados = [
      (posicao, acorde)
      for posicao, acorde in enumerate(acordes, start=1)
    ]
    interrupcoes = []

  elif opcao == "2":
    texto = ler_cifra()
    resultado = extrair_acordes(texto)
    tom = resultado.tom

    print(f"Tom identificado: {tom or 'Não informado'}")

    acordes = resultado.acordes
    acordes_posicionados = resultado.acordes_posicionados
    interrupcoes = resultado.interrupcoes

    if resultado.avisos:
      print("\n=== Avisos da extração ===")

      for aviso in resultado.avisos:
        print(f"- {aviso}")

      print(
        "\nRevise a progressão antes de confirmar, "
        "pois alguns elementos não foram reconhecidos."
      )

    if not acordes:
      print("\nNenhum acorde foi identificado.")
      return

  else:
    print("\nOpção inválida.")
    return

  revisao = revisar_acordes(
    acordes_posicionados,
    interrupcoes,
  )

  if revisao is None:
    print("\nImportação cancelada.")
    return

  acordes_posicionados, interrupcoes = revisao
  acordes = [acorde for _, acorde in acordes_posicionados]

  db = SessionLocal()

  try:
    musica = importar_musica(
      db=db,
      titulo=titulo,
      artista_nome=artista,
      acordes_posicionados=acordes_posicionados,
      interrupcoes=interrupcoes,
      tom=tom,
      letra=texto
    )

    print("\nMúsica cadastrada com sucesso!")
    print(f"ID: {musica.id}")
    print(f"Título: {musica.titulo}")
    print(f"Artista: {artista}")
    print(f"Total de acordes: {len(acordes)}")
    print(f"Total de interrupções: {len(interrupcoes)}")

  except ValueError as erro:
    print(f"\nErro: {erro}")

  except Exception as erro:
    print(f"\nErro inesperado: {erro}")

  finally:
    db.close()

if __name__ == "__main__":
  main()
