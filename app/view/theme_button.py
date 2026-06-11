from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp
from kivy.metrics import dp


class ThemeToggleButton(MDIconButton):
    """Botão flutuante que alterna entre tema claro e escuro."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = "weather-night"
        self.pos_hint = {"right": 1, "y": 0}
        self.size_hint = (None, None)
        self.size = (dp(48), dp(48))
        self.theme_text_color = "Custom"
        self.text_color = [1, 1, 1, 1]
        self.on_release = self._toggle


    def _toggle(self, *args) -> None:
        """Alterna entre Dark e Light e atualiza o ícone."""
        app = MDApp.get_running_app()
        if app.theme_cls.theme_style == "Dark":
            app.theme_cls.theme_style = "Light"
            self.icon = "weather-sunny"
        else:
            app.theme_cls.theme_style = "Dark"
            self.icon = "weather-night"


    def _toggle(self, *args) -> None:
        """Alterna entre Dark e Light e atualiza o ícone."""
        app = MDApp.get_running_app()
        if app.theme_cls.theme_style == "Dark":
            app.theme_cls.theme_style = "Light"
            self.icon = "weather-sunny"
            self.text_color = [0, 0, 0, 1]
            self._set_colors(
                card_color=[0.9, 0.9, 0.9, 1],
                cell_color=[0.85, 0.85, 0.85, 1],
            )
        else:
            app.theme_cls.theme_style = "Dark"
            self.icon = "weather-night"
            self.text_color = [1, 1, 1, 1]
            self._set_colors(
                card_color=[0.08, 0.08, 0.08, 1],
                cell_color=[0.08, 0.08, 0.08, 1],
            )


    def _set_colors(self, card_color, cell_color) -> None:
        """Aplica as cores nos cards e células de todas as telas."""
        from app.view.board_screen import CellButton, ScoreCard
        from kivymd.uix.card import MDCard

        app = MDApp.get_running_app()
        for screen in app.root.screens:
            self._walk_widgets(screen, card_color, cell_color, CellButton, ScoreCard)


    def _walk_widgets(self, widget, card_color, cell_color, CellButton, ScoreCard) -> None:
        """Percorre widgets recursivamente e aplica as cores."""
        from kivymd.uix.card import MDCard
        if isinstance(widget, CellButton):
            widget.md_bg_color = cell_color
        elif isinstance(widget, ScoreCard):
            pass  
        elif isinstance(widget, MDCard):
            widget.md_bg_color = card_color
        for child in widget.children:
            self._walk_widgets(child, card_color, cell_color, CellButton, ScoreCard)