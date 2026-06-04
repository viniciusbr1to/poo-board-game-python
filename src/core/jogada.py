class Jogada:
  def __init__(self, linha : int, coluna : int, jogador):
    self.__linha = linha
    self.__coluna = coluna
    self.__jogador = jogador

  
  @property
  def linha(self):
    return self.__linha
  

  @property
  def coluna(self):
    return self.__coluna
  

  @property
  def jogador(self):
    return self.__jogador
  


class Turno:
  def __init__(self, jogadores : list):
    self.__jogadores = jogadores
    self.__indice = 0


  @property
  def jogador_atual(self):
    return self.__jogadores[self.__indice]
  

  def alternar(self):
    self.__indice = (self.__indice + 1) % len(self.__jogadores)

  
  def reiniciar(self):
    self.__indice = 0