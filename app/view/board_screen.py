from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from app.view.theme_button import ThemeToggleButton
from app.view.result_screen import ScoreboardScreen



LABEL_TURN = "{nome}'s turn"
LABEL_ROUND_WINNER = "{nome} wins this round!"
LABEL_DRAW = "Draw!"
LABEL_MATCH_WINNER = "{nome} wins the match!"
LABEL_NEW_ROUND = "NEXT ROUND"
LABEL_NEW_MATCH = "NEW MATCH"
LABEL_LEAVE = "LEAVE"
TITLE_ROUND_OVER = "Round Over"
TITLE_MATCH_OVER = "Match Over"


class CellButton(MDCard):
    """Célula clicável do tabuleiro, exibe o símbolo da peça."""
    symbol = StringProperty("")
    def __init__(self, line: int, column: int, callback, **kwargs):
        """Inicializa a célula."""
        super().__init__(**kwargs)
        self.line = line
        self.column = column
        self._callback = callback
        self.size_hint = (1, 1)
        self.radius = [dp(8)]
        self.elevation = 2
        self.ripple_behavior = True
        self.md_bg_color = [0.08, 0.08, 0.08, 1]

        self._label = MDLabel(
            text=self.symbol,
            halign="center",
            valign="center",
            font_style="H4",
            bold=True,
            theme_text_color="Primary",
        )

        self.add_widget(self._label)
        self.bind(on_release=self._on_press)


    def update(self, symbol: str) -> None:
        """Atualiza o símbolo exibido na célula."""
        self.symbol = symbol
        self._label.text = symbol
        if symbol == "X":
            self._label.theme_text_color = "Custom"
            self._label.text_color = [0.75, 0.10, 0.10, 1]
        elif symbol == "O":
            self._label.theme_text_color = "Custom"
            self._label.text_color = [0.10, 0.25, 0.55, 1]
        else:
            self._label.theme_text_color = "Primary"


    def _on_press(self, *args) -> None:
        """Dispara o callback com a posição da célula."""
        try:
            self._callback(self.line, self.column)
        except Exception as e:
            print(f"[CellButton] Erro ao processar clique: {e}")


class ScoreCard(MDCard):
    """Card de placar individual de um jogador."""
    def __init__(self, symbol: str, **kwargs):
        """Inicializa o card. Args: symbol: 'X' ou 'O'."""
        super().__init__(**kwargs)
        self.symbol = symbol
        self.size_hint = (1, None)
        self.height = dp(72)
        self.radius = [dp(10)]
        self.elevation = 3
        self.orientation = "vertical"
        self.padding = [dp(8), dp(4)]
        self.spacing = dp(2)
        self.md_bg_color = [0.75, 0.10, 0.10, 1] if symbol == "X" else [0.10, 0.25, 0.55, 1]

        self._label_name = MDLabel(
            text=symbol,
            halign="center",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
        )

        self._label_score = MDLabel(
            text="0",
            halign="center",
            font_style="H5",
            bold=True,
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
        )

        self.add_widget(self._label_name)
        self.add_widget(self._label_score)


    def update(self, name: str, score: int) -> None:
        """Atualiza nome e pontuação. Args: name: Nome do jogador. score: Pontuação atual."""
        self._label_name.text = f"{name} ({self.symbol})"
        self._label_score.text = str(score)


class BoardScreen(MDScreen):
    """Tela principal do jogo — exibe o tabuleiro e o painel de status."""
    def __init__(self, controller=None, **kwargs):
        """Inicializa a tela do tabuleiro."""
        super().__init__(**kwargs)
        self.controller = controller
        self._cells: list[list[CellButton]] = []
        self._dialog: MDDialog | None = None
        self._label_turn: MDLabel | None = None
        self._score_p1: ScoreCard | None = None
        self._score_p2: ScoreCard | None = None


    def on_enter(self) -> None:
        """Chamado ao entrar na tela — constrói ou reconstrói a UI."""
        self.clear_widgets()
        self._cells = []
        self._build_ui()
        if self.controller:
            self.controller.on_board_update = self._update_board


    def _build_ui(self) -> None:
        """Constrói todos os widgets da tela."""
        container = FloatLayout()

        root = MDBoxLayout(
            orientation="vertical",
            padding=[dp(32), dp(24), dp(32), dp(48)],
            spacing=dp(16),
            size_hint=(1, 1),
        )

        toggle = ThemeToggleButton()
        container.add_widget(root)
        container.add_widget(toggle)

        scoreboard = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(72),
            spacing=dp(12),
        )

        self._score_p1 = ScoreCard(symbol="X")
        self._score_p2 = ScoreCard(symbol="O")

        if self.controller and self.controller.game:
            scores = self.controller.get_scores()
            self._score_p1.update(scores[0]["nome"], scores[0]["pontuacao"])
            self._score_p2.update(scores[1]["nome"], scores[1]["pontuacao"])

        scoreboard.add_widget(self._score_p1)
        scoreboard.add_widget(self._score_p2)

        status = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(56),
            padding=[dp(16), dp(8)],
            radius=[dp(12)],
            md_bg_color=[0.08, 0.08, 0.08, 1],
            elevation=2,
        )

        current_name = ""
        if self.controller and self.controller.game:
            current_name = self.controller.get_jogador_atual()

        self._label_turn = MDLabel(
            text=LABEL_TURN.format(nome=current_name),
            halign="center",
            font_style="H6",
            theme_text_color="Primary",
        )
        status.add_widget(self._label_turn)

        grid = MDGridLayout(
            cols=3,
            spacing=dp(8),
            padding=dp(8),
            size_hint=(1, 1),
        )

        for l in range(3):
            line = []
            for c in range(3):
                cell = CellButton(
                    line=l,
                    column=c,
                    callback=self._on_clicked_cell,
                )
                grid.add_widget(cell)
                line.append(cell)
            self._cells.append(line)

        actions = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(52),
            spacing=dp(12),
        )

        btn_leave = MDRaisedButton(
            text=LABEL_LEAVE,
            size_hint_x=0.4,
            height=dp(52),
            font_size="17sp",
            font_name="RobotoMedium",
            md_bg_color=[0.75, 0.10, 0.10, 1],
            text_color=[1, 1, 1, 1],
            on_release=self._go_to_menu,
        )

        btn_new = MDRaisedButton(
            text=LABEL_NEW_MATCH,
            size_hint_x=0.6,
            height=dp(52),
            font_size="17sp",
            font_name="RobotoMedium",
            md_bg_color=[0.10, 0.25, 0.55, 1],
            text_color=[1, 1, 1, 1],
            on_release=self._new_match,
        )

        actions.add_widget(btn_leave)
        actions.add_widget(btn_new)
        root.add_widget(scoreboard)
        root.add_widget(status)
        root.add_widget(grid)
        root.add_widget(actions)
        self.add_widget(container)


    def _on_clicked_cell(self, line: int, column: int) -> None:
        """Trata o clique em uma célula do tabuleiro."""
        if not self.controller:
            return
        try:
            self.controller.make_move(line, column)
            if self.controller.game.encerrado:
                if self.controller.is_match_over():
                    self._show_match_over()
                else:
                    self._show_round_over()
        except Exception as e:
            print(f"[BoardScreen] Erro ao processar jogada: {e}")


    def _update_turn_label(self) -> None:
        """Atualiza o label do turno com cor do jogador atual."""
        if not self.controller or not self._label_turn:
            return
        name = self.controller.get_jogador_atual()
        symbol = self.controller.game.jogador_atual.simbolo
        self._label_turn.text = LABEL_TURN.format(nome=name)
        self._label_turn.theme_text_color = "Custom"
        self._label_turn.text_color = [0.75, 0.10, 0.10, 1] if symbol == "X" else [0.10, 0.25, 0.55, 1]


    def _update_scoreboard(self) -> None:
        """Atualiza os cards de placar com a pontuação atual."""
        if not self.controller:
            return
        scores = self.controller.get_scores()
        self._score_p1.update(scores[0]["nome"], scores[0]["pontuacao"])
        self._score_p2.update(scores[1]["nome"], scores[1]["pontuacao"])


    def _update_board(self, state: list[list]) -> None:
        """Atualiza visualmente todas as células com o estado atual."""
        try:
            for l in range(3):
                for c in range(3):
                    self._cells[l][c].update(state[l][c])

            if not self.controller.game.encerrado:
                self._update_turn_label()

            self._update_scoreboard()
        except Exception as e:
            print(f"[BoardScreen] Erro ao atualizar tabuleiro: {e}")


    def _show_round_over(self) -> None:
        """Exibe dialog de fim de rodada com opção de próxima rodada."""
        try:
            winner = self.controller.get_vencedor()
            text = LABEL_ROUND_WINNER.format(nome=winner.nome) if winner else LABEL_DRAW

            scores = self.controller.get_scores()
            placar = "\n".join(
                f"{s['nome']}: {s['pontuacao']}/3" for s in scores
            )

            self._dialog = MDDialog(
                title=TITLE_ROUND_OVER,
                text=f"{text}\n\n{placar}",
                buttons=[
                    MDRaisedButton(
                        text=LABEL_LEAVE,
                        md_bg_color=[0.75, 0.10, 0.10, 1],
                        text_color=[1, 1, 1, 1],
                        on_release=lambda x: self._close_dialog_and_go(destiny="menu"),
                    ),
                    MDRaisedButton(
                        text=LABEL_NEW_ROUND,
                        md_bg_color=[0.10, 0.25, 0.55, 1],
                        text_color=[1, 1, 1, 1],
                        on_release=lambda x: self._close_dialog_and_go(destiny="round"),
                    ),
                ],
            )
            self._dialog.open()
        except Exception as e:
            print(f"[BoardScreen] Erro ao exibir fim de rodada: {e}")


    def _show_match_over(self) -> None:
        """Exibe dialog de fim de partida (MD5 encerrada)."""
        try:
            winner = self.controller.get_match_winner()
            text = LABEL_MATCH_WINNER.format(nome=winner.nome) if winner else LABEL_DRAW

            scores = self.controller.get_scores()
            placar = "\n".join(
                f"{s['nome']}: {s['pontuacao']}/3" for s in scores
            )

            if self.controller:
                self.controller.registrar_partida()

            self._dialog = MDDialog(
                title=TITLE_MATCH_OVER,
                text=f"{text}\n\n{placar}",
                buttons=[
                    MDRaisedButton(
                        text=LABEL_LEAVE,
                        md_bg_color=[0.75, 0.10, 0.10, 1],
                        text_color=[1, 1, 1, 1],
                        on_release=lambda x: self._close_dialog_and_go(destiny="menu"),
                    ),
                    MDRaisedButton(
                    text=LABEL_NEW_MATCH,
                    md_bg_color=[0.10, 0.25, 0.55, 1],
                    text_color=[1, 1, 1, 1],
                    on_release=lambda x: self._close_dialog_and_go(destiny="match"),
                    ),
                ],
            )
            self._dialog.open()
        except Exception as e:
            print(f"[BoardScreen] Erro ao exibir fim de partida: {e}")


    def _close_dialog_and_go(self, destiny: str) -> None:
        """Fecha o dialog e executa a ação escolhida."""
        if self._dialog:
            self._dialog.dismiss()
            self._dialog = None

        if destiny == "menu":
            self._go_to_menu()
        elif destiny == "round":
            self._next_round()
        elif destiny == "match":
            self._new_match()


    def _next_round(self, *args) -> None:
        """Inicia a próxima rodada mantendo o placar."""
        try:
            if self.controller:
                self.controller.next_round()
                self._update_turn_label()
        except Exception as e:
            print(f"[BoardScreen] Erro ao iniciar próxima rodada: {e}")


    def _new_match(self, *args) -> None:
        try:
            self.manager.transition.direction = "left"
            self.manager.current = "config"
        except Exception as e:
            print(f"[BoardScreen] Erro ao reiniciar partida: {e}")

            
    def _go_to_menu(self, *args) -> None:
        try:
            self.manager.transition.direction = "right"
            self.manager.current = "menu"
        except Exception as e:
            print(f"[BoardScreen] Erro ao navegar para menu: {e}")

    