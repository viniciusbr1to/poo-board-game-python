from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from app.view.theme_button import ThemeToggleButton


title = "Match Settings"
player1_label = "Player 1"
player2_label = "Player 2"
HINT_NOME = "Player name"
symbol_label = "Symbol"
confirm_label = "PLAY"
back_label = "BACK"
error_empty_name = "Enter the names of two players."
error_same_symbol = "The players cannot have the same symbol."


class SymbolSelector(MDBoxLayout):
    def __init__(self, initial_symbol="X", on_change=None, **kwargs):
        super().__init__(**kwargs)
        self.on_change = on_change
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(48)
        self.spacing = dp(8)
        self._symbol = initial_symbol
        self._buttons = {}
        self._build()


    def _build(self):
        label = MDLabel(
            text=symbol_label,
            size_hint_x=0.4,
            theme_text_color="Secondary",
            font_style="Body1",
        )

        self.add_widget(label)

        for symbol in ("X", "O"):
            btn = MDRaisedButton(
                text=symbol,
                size_hint_x=0.3,
                on_release=lambda x, s=symbol: self._select(s),
            )
            self._buttons[symbol] = btn
            self.add_widget(btn)
        self._update_look()


    def _select(self, symbol):
        self._symbol = symbol
        self._update_look()
        if self.on_change:
            self.on_change()


    def _update_look(self):
        for s, btn in self._buttons.items():
            if s == self._symbol:
                btn.md_bg_color = [0.75, 0.10, 0.10, 1] if s == "X" else [0.10, 0.25, 0.55, 1]
                btn.text_color = [1, 1, 1, 1]
            else:
                btn.md_bg_color = [0.08, 0.08, 0.08, 1]
                btn.text_color = [1, 1, 1, 1]


    @property
    def symbol(self):
        return self._symbol


class PlayerPanel(MDCard):
    def __init__(self, title: str, initial_symbol: str, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint = (1, None)
        self.height = dp(180)
        self.padding = dp(16)
        self.spacing = dp(12)
        self.radius = [dp(12)]
        self.elevation = 2

        label = MDLabel(
            text=title,
            font_style="H6",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(32),
            bold=True,
        )

        self._name_field = MDTextField(
            hint_text=HINT_NOME,
            mode="rectangle",
            size_hint_y=None,
            height=dp(52),
        )

        self._selector = SymbolSelector(
            initial_symbol=initial_symbol,
            on_change=self.update_textfield_color,
        )

        self.add_widget(label)
        self.add_widget(self._name_field)
        self.add_widget(self._selector)
        self.update_textfield_color()


    def update_textfield_color(self):
        color = [0.75, 0.10, 0.10, 1] if self.symbol == "X" else [0.10, 0.25, 0.55, 1]
        self._name_field.line_color_focus = color
        self._name_field.text_color_focus = color
        self._name_field.hint_text_color_focus = color


    @property
    def name(self):
        return self._name_field.text.strip()


    @property
    def symbol(self):
        return self._selector.symbol


class ConfigScreen(MDScreen):
    """Tela de configuração — define nomes e símbolos dos jogadores."""
    def __init__(self, controller=None, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self._panel_p1: PlayerPanel | None = None
        self._panel_p2: PlayerPanel | None = None
        self._dialog: MDDialog | None = None


    def on_enter(self) -> None:
        self.clear_widgets()
        self._build_ui()


    def _build_ui(self) -> None:
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

        title_label = MDLabel(
            text=title,
            halign="center",
            font_style="H5",
            bold=True,
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(48),
        )

        self._panel_p1 = PlayerPanel(title=player1_label, initial_symbol="X")
        self._panel_p2 = PlayerPanel(title=player2_label, initial_symbol="O")

        actions = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(52),
            spacing=dp(12),
        )

        back_button = MDRaisedButton(
            text=back_label,
            size_hint_x=0.4,
            font_size="17sp",
            font_name="RobotoMedium",
            md_bg_color=[0.75, 0.10, 0.10, 1],
            text_color=[1, 1, 1, 1],
            on_release=self._back,
        )

        confirm_button = MDRaisedButton(
            text=confirm_label,
            size_hint_x=0.6,
            font_size="17sp",
            font_name="RobotoMedium",
            md_bg_color=[0.10, 0.25, 0.55, 1],
            text_color=[1, 1, 1, 1],
            on_release=self.confirm,
        )

        actions.add_widget(back_button)
        actions.add_widget(confirm_button)
        root.add_widget(title_label)
        root.add_widget(self._panel_p1)
        root.add_widget(self._panel_p2)
        root.add_widget(actions)
        self.add_widget(container)


    def confirm(self, *args) -> None:
        try:
            name1 = self._panel_p1.name
            name2 = self._panel_p2.name
            symbol1 = self._panel_p1.symbol
            symbol2 = self._panel_p2.symbol

            if not name1 or not name2:
                self._show_error(error_empty_name)
                return

            if symbol1 == symbol2:
                self._show_error(error_same_symbol)
                return

            if self.controller:
                self.controller.start_game(
                    names=[name1, name2],
                    symbols=[symbol1, symbol2],
                )

            self.manager.transition.direction = "left"
            self.manager.current = "board"

        except Exception as e:
            print(f"[ConfigScreen] Erro ao confirmar configuração: {e}")


    def _show_error(self, message: str) -> None:
        self._dialog = MDDialog(
            title="Attention",
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self._dialog.dismiss(),
                )
            ],
        )
        self._dialog.open()


    def _back(self, *args) -> None:
        try:
            self.manager.transition.direction = "right"
            self.manager.current = "menu"
        except Exception as e:
            print(f"[ConfigScreen] Erro ao navegar para menu: {e}")
