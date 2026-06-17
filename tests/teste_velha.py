import pytest
from app.models.jogador import Jogador
from app.models.jogada import Jogada
from app.models.game.jogo_da_velha import JogoDaVelha


@pytest.fixture
def jogo():
  j1 = Jogador("Sophia", "X")
  j2 = Jogador("Vinicius", "O")
  jogo = JogoDaVelha([j1, j2])
  jogo.inicializar()
  return jogo


@pytest.fixture
def jogadores():
  j1 = Jogador("Sophia", "X")
  j2 = Jogador("Vinicius", "O")
  return j1, j2


def test_jogada_invalida_fora_do_tabuleiro(jogo, jogadores):
  j1, _ = jogadores
  jogada = Jogada(5, 5, j1)
  assert jogo.validar_jogada(jogada) == False


def test_jogada_invalida_posicao_ocupada(jogo, jogadores):
  j1, j2 = jogadores
  jogo.jogar(Jogada(0, 0, j1))
  assert jogo.validar_jogada(Jogada(0, 0, j2)) == False


def test_alternancia_de_turno(jogo, jogadores):
  j1, j2 = jogadores
  assert jogo.jogador_atual.nome == "Sophia"
  jogo.jogar(Jogada(0, 0, j1))
  assert jogo.jogador_atual.nome == "Vinicius"


def test_vitoria_linha(jogo, jogadores):
  j1, j2 = jogadores
  jogo.jogar(Jogada(0, 0, j1))
  jogo.jogar(Jogada(1, 0, j2))
  jogo.jogar(Jogada(0, 1, j1))
  jogo.jogar(Jogada(1, 1, j2))
  jogo.jogar(Jogada(0, 2, j1))
  assert jogo.encerrado == True
  assert jogo.vencedor.nome == "Sophia"


def test_vitoria_coluna(jogo, jogadores):
  j1, j2 = jogadores
  jogo.jogar(Jogada(0, 0, j1))
  jogo.jogar(Jogada(0, 1, j2))
  jogo.jogar(Jogada(1, 0, j1))
  jogo.jogar(Jogada(1, 1, j2))
  jogo.jogar(Jogada(2, 0, j1))
  assert jogo.encerrado == True
  assert jogo.vencedor.nome == "Sophia"


def test_vitoria_diagonal(jogo, jogadores):
  j1, j2 = jogadores
  jogo.jogar(Jogada(0, 0, j1))
  jogo.jogar(Jogada(0, 1, j2))
  jogo.jogar(Jogada(1, 1, j1))
  jogo.jogar(Jogada(0, 2, j2))
  jogo.jogar(Jogada(2, 2, j1))
  assert jogo.encerrado == True
  assert jogo.vencedor.nome == "Sophia"


def test_empate(jogo, jogadores):
  j1, j2 = jogadores
  jogo.jogar(Jogada(0, 0, j1))
  jogo.jogar(Jogada(0, 1, j2))
  jogo.jogar(Jogada(0, 2, j1))
  jogo.jogar(Jogada(1, 1, j2))
  jogo.jogar(Jogada(1, 0, j1))
  jogo.jogar(Jogada(1, 2, j2))
  jogo.jogar(Jogada(2, 1, j1))
  jogo.jogar(Jogada(2, 0, j2))
  jogo.jogar(Jogada(2, 2, j1))
  assert jogo.encerrado == True
  assert jogo.vencedor is None


def test_jogo_encerrado_nao_aceita_jogada(jogo, jogadores):
  j1, j2 = jogadores
  jogo.jogar(Jogada(0, 0, j1))
  jogo.jogar(Jogada(1, 0, j2))
  jogo.jogar(Jogada(0, 1, j1))
  jogo.jogar(Jogada(1, 1, j2))
  jogo.jogar(Jogada(0, 2, j1))
  assert jogo.encerrado == True
  jogo.jogar(Jogada(2, 2, j2))
  assert jogo.vencedor.nome == "Sophia"