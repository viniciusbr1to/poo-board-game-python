from app.models.jogo import JogoTabuleiro
from app.models.jogada import Jogada
from app.models.peca import Peca


class JogoDaVelha(JogoTabuleiro):
  def __init__(self, jogadores : list):
    super().__init__(jogadores, linhas = 3, colunas = 3)

  
  def validar_jogada(self, jogada : Jogada) -> bool:
    l, c = jogada.linha, jogada.coluna
    if not (0 <= l < 3 and 0 <= c < 3):
      return False
    return self._tabuleiro.esta_vazio(l, c)
  

  def aplicar_jogada(self, jogada : Jogada):
    peca = Peca(jogada.jogador.simbolo, jogada.jogador)
    self._tabuleiro.definir(jogada.linha, jogada.coluna, peca)

  
  def verificar_fim(self) -> bool:
    t = self._tabuleiro

    for i in range(3):
      if self.__linha_vencedora(t.obter(i, 0), t.obter(i, 1), t.obter(i, 2)):
        self._vencedor = t.obter(i, 0).dono
        return True
      if self.__linha_vencedora(t.obter(0, i), t.obter(1, i), t.obter(2, i)):
        self._vencedor = t.obter(0, i).dono
        return True
      
    if self.__linha_vencedora(t.obter(0, 0), t.obter(1, 1), t.obter(2, 2)):
      self._vencedor = t.obter(0, 0).dono
      return True
    if self.__linha_vencedora(t.obter(0, 2), t.obter(1, 1), t.obter(2, 0)):
      self._vencedor = t.obter(0, 2).dono
      return True
    
    if self._tabuleiro.esta_cheio():
      self._vencedor = None
      return True
    
    return False
  

  def __linha_vencedora(self, a, b, c) -> bool:
    return a is not None and b is not None and c is not None and a.simbolo == b.simbolo == c.simbolo
