class Tabuleiro:
  def __init__(self, linhas : int, colunas : int):
    self.__linhas = linhas
    self.__colunas = colunas
    self.__grade = [[None] * colunas for _ in range(linhas)]

  
  @property
  def linhas(self):
    return self.__linhas
  

  @property
  def colunas(self):
    return self.__colunas
  

  def obter(self, linha: int, coluna : int):
    return self.__grade[linha][coluna]
  

  def definir(self, linha : int, coluna : int, peca):
    self.__grade[linha][coluna] = peca

  
  def esta_vazio(self, linha : int, coluna : int) -> bool:
    return self.__grade[linha][coluna] is None
  

  def esta_cheio(self) -> bool:
    return all(self.__grade[l][c] is not None for l in range(self.__linhas) for c in range(self.__colunas))
  

  def limpar(self):
    self.__grade = [[None] * self.__colunas for _ in range(self.__linhas)]

  
  def exibir(self):
    for linha in self.__grade:
      print(" | ".join(str(p) if p else "." for p in linha))
    print()

    
  