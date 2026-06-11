from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from app.view.theme_button import ThemeToggleButton
from kivymd.uix.button import MDRaisedButton


class ScoreboardScreen(MDScreen):
    """Tela que mostra o histórico de partidas jogadas."""
    def __init__(self, controller=None, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller


    def on_enter(self):
        self.clear_widgets()
        self._build_ui()


    def _build_ui(self):
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

        title = MDLabel(
            text="SCOREBOARD",
            halign="center",
            font_style="H4",
            bold=True,
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(64),
        )

        root.add_widget(title)

        if self.controller and self.controller.historico:
            for partida in self.controller.historico:
                card = MDCard(
                    orientation="vertical",
                    size_hint=(1, None),
                    height=dp(120),
                    padding=dp(16),
                    radius=[dp(12)],
                    elevation=2,
                    md_bg_color=[0.08, 0.08, 0.08, 1],
                )
                
                card.add_widget(MDLabel(text=f"{partida['jogador1']['nome']} ({partida['jogador1']['pontuacao']})"))
                card.add_widget(MDLabel(text=f"{partida['jogador2']['nome']} ({partida['jogador2']['pontuacao']})"))
                card.add_widget(MDLabel(text=f"Vencedor: {partida['vencedor']}"))
                root.add_widget(card)
        else:
            root.add_widget(MDLabel(
                text="Nenhuma partida registrada ainda.",
                halign="center",
                theme_text_color="Hint",
            ))

        back_button = MDRaisedButton(
            text="BACK",
            size_hint=(0.4, None),
            height=dp(52),
            font_size="17sp",
            font_name="RobotoMedium",
            md_bg_color=[0.75, 0.10, 0.10, 1],
            text_color=[1, 1, 1, 1],
            on_release=self._back,
        )

        root.add_widget(back_button)
        self.add_widget(container)

    def _back(self, *args):
        self.manager.transition.direction = "right"
        self.manager.current = "menu"

        
