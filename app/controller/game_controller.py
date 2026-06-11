from app.models.game.jogo_da_velha import JogoDaVelha
from app.models.jogador import Jogador
from app.models.jogada import Jogada


PONTOS_PARA_VENCER = 3  


class GameController:
    """Ponte entre as telas KivyMD e a lógica do jogo."""
    def __init__(self):
        """Inicializa o controller sem partida ativa."""
        self.game = None
        self.on_board_update = None
        self.historico = []

    def registrar_partida(self):
        """Salva resultado da partida no histórico."""
        scores = self.get_scores()
        vencedor = self.get_vencedor()
        self.historico.append({
            "jogador1": scores[0],
            "jogador2": scores[1],
            "vencedor": vencedor.nome if vencedor else "Empate"
        })


    def start_game(self, names, symbols=None) -> None:
        if symbols is None:
            symbols = ["X", "O"]

        p1 = Jogador(names[0], symbols[0])
        p2 = Jogador(names[1], symbols[1])
        self.game = JogoDaVelha([p1, p2])
        self.game.inicializar()
        self._notify_view()


    def make_move(self, line: int, column: int) -> bool:
        if not self.game or self.game.encerrado:
            return False

        move = Jogada(line, column, self.game.jogador_atual)
        self.game.jogar(move)
        self._notify_view()
        return True


    def is_match_over(self) -> bool:
        """Retorna True se algum jogador atingiu 3 pontos (venceu a MD5)."""
        if not self.game:
            return False
        return any(j.pontuacao >= PONTOS_PARA_VENCER for j in self.game._jogadores)


    def get_match_winner(self):
        """Retorna o Jogador que venceu a MD5, ou None."""
        if not self.game:
            return None
        for j in self.game._jogadores:
            if j.pontuacao >= PONTOS_PARA_VENCER:
                return j
        return None


    def next_round(self) -> None:
        """Inicia a próxima rodada mantendo a pontuação."""
        if self.game:
            self.game.inicializar()
            self._notify_view()


    def get_board_state(self) -> list[list[str]]:
        """Retorna matriz 3x3 com os símbolos atuais."""
        grid = []
        for l in range(3):
            line = []
            for c in range(3):
                piece = self.game._tabuleiro.obter(l, c)
                line.append(piece.simbolo if piece else "")
            grid.append(line)
        return grid


    def get_jogador_atual(self) -> str:
        """Retorna o nome do jogador do turno atual."""
        return self.game.jogador_atual.nome


    def get_vencedor(self):
        """Retorna o Jogador vencedor da rodada atual, ou None."""
        return self.game.vencedor


    def get_scores(self) -> list[dict]:
        """Retorna lista com nome, simbolo e pontuacao de cada jogador."""
        return [
            {"nome": p.nome, "simbolo": p.simbolo, "pontuacao": p.pontuacao}
            for p in self.game._jogadores
        ]


    def _notify_view(self) -> None:
        """Dispara o callback de atualização da view."""
        if self.on_board_update:
            self.on_board_update(self.get_board_state())
