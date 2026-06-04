from abc import ABC, abstractmethod
from .tabuleiro import Tabuleiro
from .jogada import Turno


class JogoTabuleiro(ABC):
  def __init__(self, jogadores : list, linhas : int, colunas : int):
    self._tabuleiro = Tabuleiro(linhas, colunas)
    self._turno = Turno(jogadores)
    self._jogadores = jogadores
    self._encerrado = False
    self._vencedor = None


  @abstractmethod
  def verificar_fim(self) -> bool:
    pass


  @abstractmethod
  def validar_jogada(self, jogada) -> bool:
    pass

  @abstractmethod
  def aplicar_jogada(self, jogada):
    pass


  def inicializar(self):
    self._tabuleiro.limpar()
    self._turno.reiniciar()
    self._encerrado = False
    self._vencedor = None

  
  def jogar(self, jogada):
    if self._encerrado: 
      print("O jogo já foi encerrado.")
      return
    if not self.validar_jogada(jogada):
      print("Jogada inválida.")
      return

    self.aplicar_jogada(jogada)
    if self.verificar_fim():
      self._encerrado = True
      if self.vencedor: 
        self._vencedor.adicionar_ponto()
        print(f"Fim de jogo! Vencedor: {self._vencedor}")
      else:
        print("Empate!")
    else:
      self._turno.alternar()


  @property
  def encerrado(self):
    return self._encerrado
  

  @property
  def vencedor(self):
    return self._vencedor
  

  @property
  def jogador_atual(self):
    return self._turno.jogador_atual
