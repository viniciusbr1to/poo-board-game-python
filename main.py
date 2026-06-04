from app.models.jogador import Jogador
from app.models.jogada import Jogada
from app.game.jogo_da_velha import JogoDaVelha
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from app.view.menu_screen import MenuScreen
from app.view.board_screen import BoardScreen
from app.controller.game_controller import GameController


def pedir_jogada(jogador):
  while True:
    try:
      linha = int(input(f"{jogador.nome}, escolha a linha (0-2): "))
      coluna = int(input(f"{jogador.nome}, escolha a coluna (0-2): "))
      return Jogada(linha, coluna, jogador)
    except ValueError:
      print("Digite apenas números inteiros.")


def configurar_jogadores():
  print("=== Configuração dos jogadores ===")

  nome1 = input("Nome do jogador 1: ")
  nome2 = input("Nome do jogador 2: ")

  j1 = Jogador(nome1, "X")
  j2 = Jogador(nome2, "O")
  return j1, j2


def jogar_partida(jogo, j1, j2):
  jogo.inicializar()
  jogo._tabuleiro.exibir()

  while not jogo.encerrado:
    jogador = jogo.jogador_atual
    jogada = pedir_jogada(jogador)
    jogo.jogar(jogada)

    if not jogo.encerrado:
      jogo._tabuleiro.exibir()


def menu():
  print("╔══════════════════════════╗")
  print("║   JOGOS DE TABULEIRO     ║")
  print("╚══════════════════════════╝")

  j1, j2 = configurar_jogadores()
  jogo = JogoDaVelha([j1, j2])

  while True: 
    print("\n=== MENU ===")
    print("1. Nova partida")
    print("2. Ver pontuação")
    print("3. Sair")
    opcao = input("Escolha: ").strip()

    if opcao == "1":
      jogar_partida(jogo, j1, j2)
    elif opcao == "2":
      print(f"\n{j1.nome}: {j1.pontuacao} ponto(s)")
      print(f"{j2.nome}: {j2.pontuacao} ponto(s)")
    elif opcao == "3":
      print("Encerrando o jogo...")
      break
    else:
      print("Opção inválida.")

if __name__ == "__main__":
   menu()


