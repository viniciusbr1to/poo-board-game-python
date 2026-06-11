from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from app.view.theme_button import ThemeToggleButton


class MenuScreen(MDScreen):
  """Tela de menu principal do Jogo da Velha."""
  def __init__(self, **kwargs):
    """Inicializa a tela."""
    super().__init__(**kwargs)


  def on_enter(self):
    """Constrói a UI ao entrar na tela."""
    self.clear_widgets()
    self._build_ui()


  def _build_ui(self):
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

    title = MDLabel(
      text="JOGO DA VELHA",
      halign="center",
      font_style="H3",
      bold=True,
      theme_text_color="Primary",
      size_hint_y=None,
      height=dp(80),
    )

    card = MDCard(
      orientation="vertical",
      size_hint=(1, None),
      height=dp(160),
      padding=dp(20),
      radius=[dp(16)],
      elevation=4,
      md_bg_color=[0.08, 0.08, 0.08, 1],
    )

    game_image = Image(
      source="assets/images/logo.png", 
      allow_stretch=True,
      keep_ratio=True,
    )     
    card.add_widget(game_image)

    anchor = AnchorLayout(
      anchor_x="center",
      anchor_y="center",
      size_hint=(1, 1),
    )

    buttons = MDBoxLayout(
      orientation="vertical",
      spacing=dp(12),
      size_hint=(0.25, None),
      height=dp(192),
    )

    btn_play = MDRaisedButton(
      text="NEW MATCH",
      size_hint=(1, None),
      height=dp(56),
      font_size="17sp",
      font_name="RobotoMedium",
      md_bg_color=[0.10, 0.25, 0.55, 1],
      text_color=[1, 1, 1, 1],
      on_release=self.go_to_config,
    ) 

    btn_score = MDRaisedButton(
      text="SCOREBOARD",
      size_hint=(1, None),
      height=dp(56),
      font_size="17sp",
      font_name="RobotoMedium",
      md_bg_color=[0.08, 0.08, 0.08, 1],
      text_color=[1, 1, 1, 1],
      on_release=self.show_score,
    )

    btn_exit = MDRaisedButton(
      text="EXIT",
      size_hint=(1, None),
      height=dp(56),
      font_size="17sp",
      font_name="RobotoMedium",
      md_bg_color=[0.75, 0.10, 0.10, 1],
      text_color=[1, 1, 1, 1],
      on_release=self.exit,
    )

    buttons.add_widget(btn_play)
    buttons.add_widget(btn_score)
    buttons.add_widget(btn_exit)
    anchor.add_widget(buttons)

    baseboard = MDLabel(
      text="POO • Fatec Ribeirão Preto",
      halign="center",
      font_style="Caption",
      theme_text_color="Hint",
      size_hint_y=None,
      height=dp(32),
    )

    root.add_widget(title)
    root.add_widget(card)
    root.add_widget(anchor)
    root.add_widget(baseboard)
    self.add_widget(container)


  def go_to_config(self, *args):
    self.manager.transition.direction = "left"
    self.manager.current = "config"


  def show_score(self, *args):
    """Exibe o placar em um dialog."""
    self.manager.transition.direction = "left"
    self.manager.current = "scoreboard"


  def exit(self, *args):
    """Encerra o aplicativo."""
    from kivy.app import App
    App.get_running_app().stop()