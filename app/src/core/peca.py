class Peca: 
  def __init__(self, simbolo : str, dono):
    self.__simbolo = simbolo
    self.__dono = dono


  @property
  def simbolo(self):
    return self.__simbolo
  

  @property
  def dono(self):
    return self.__dono
  

  def __str__(self):
    return self.__simbolo