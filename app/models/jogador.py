class Jogador:
  def __init__(self, nome: str, simbolo : str):
    self.__nome = nome
    self.__simbolo = simbolo
    self.__pontuacao = 0


  @property
  def nome(self):
    return self.__nome
  

  @property
  def simbolo(self):
    return self.__simbolo
  

  @property
  def pontuacao(self):
    return self.__pontuacao
  

  def adicionar_ponto(self):
    self.__pontuacao += 1

  
  def __str__(self):
    return f"{self.__nome} ({self.__simbolo})"
