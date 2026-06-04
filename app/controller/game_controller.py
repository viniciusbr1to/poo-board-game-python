from app.models.game.jogo_da_velha import JogoDaVelha
from app.models.jogador import Jogador
from app.models.jogada import Jogada


class GameController:
      def __init__(self):
          self.game = None
          self.on_board_update = None


      def start_game(self, nomes: list[str]):
          j1 = Jogador(nomes[0], "X")
          j2 = Jogador(nomes[1], "O")
          self.game = JogoDaVelha([j1, j2])
          self.game.inicializar()
          self._notify_view()


      def make_move(self, linha: int, coluna: int) -> bool:
          if not self.game or self.game.encerrado:
                 return False
          jogada = Jogada(linha, coluna, self.game.jogador_atual)
          self.game.jogar(jogada)
          self._notify_view()
          return True

      def get_board_state(self) -> list:
          grade = []
          for l in range(3):
              linha = []
              for c in range(3):
                  peca = self.game._tabuleiro.obter(l, c)
                  linha.append(peca.simbolo if peca else "")
              grade.append(linha)
          return grade

      def get_jogador_atual(self) -> str:
          return self.game.jogador_atual.nome

      def get_vencedor(self):
          return self.game.vencedor

      def get_scores(self) -> list[dict]:
          return[
            {"nome": j.nome, "simbolo": j.simbolo, "pontuacao": j.pontuacao}
            for j in self.game._jogadores
          ]

      def _notify_view(self):
          if self.on_board_update:
             self.on_board_update(self.get_board_state())