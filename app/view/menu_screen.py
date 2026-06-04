from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivy.metrics import dp


class MenuScreen(MDScreen):
      def __init__(self, **kwargs):
          super().__init__(**kwargs)
  
      def on_enter(self):
          self.clear_widgets()
          self._build_ui()

      def _build_ui(self):
          root = MDBoxLayout(
            orientation="vertical",
            md_bg_color=[0.07, 0.07, 0.12, 1],
            padding=[dp(32), dp(48), dp(32), dp(48)],
            spacing=dp(24),
          )  

          header = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(160),
            spacing=dp(8),
          )

          titulo = MDLabel(
            text="JOGO DA VELHA",
            halign="center",
            font_style="H3",
            bold=True,
            theme_text_color="Primary",
          )

          subtitulo = MDLabel(
            text="Melhor de cinco partidas",
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Secondary",
          )

          header.add_widget(titulo)
          header.add_widget(subtitulo)

          card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(180),
            padding=dp(20),
            spacing=dp(12),
            radius=[dp(16)],
            elevation=4,
            md_bg_color=[0.13, 0.13, 0.20, 1],
          )

          grid_label = MDLabel(
            text=" X  │  O  │  X \n────┼────┼────\n O  │  X  │  O \n────┼────┼────\n X  │  O  │  X ",
            halign="center",
            font_style="H6",
            theme_text_color="Primary",
          )
          card.add_widget(grid_label)

          botoes = MDBoxLayout(
            orientation="vertical",
            spacing=dp(14),
            size_hint_y=None,
            height=dp(180),
          )

          btn_jogar = MDRaisedButton(
            text="NOVA PARTIDA",
            size_hint_x=1,
            height=dp(52),
            font_size="16sp",
            on_release=self.ir_para_config,
          )

          btn_pontuacao = MDFlatButton(
            text="VER PONTUAÇÃO",
            size_hint_x=1,
            height=dp(48),
            font_size="15sp",
            on_release=self.ver_pontuacao,
          )

          btn_sair = MDFlatButton(
            text="SAIR",
            size_hint_x=1,
            height=dp(48),
            font_size="15sp",
            theme_text_color="Error",
            on_release=self.sair,
          )

          botoes.add_widget(btn_jogar)
          botoes.add_widget(btn_pontuacao)
          botoes.add_widget(btn_sair)

          rodape = MDLabel(
            text="POO • Fatec Ribeirão Preto",
            halign="center",
            font_style="Caption",
            theme_text_color="Hint",
            size_hint_y=None,
            height=dp(32),
          )

          root.add_widget(header)
          root.add_widget(card)
          root.add_widget(botoes)
          root.add_widget(rodape)

          self.add_widget(root)

      def ir_para_config(self, *args):
          self.manager.current = "config"

      def ver_pontuacao(self, *args):
          from kivymd.uix.dialog import MDDialog
          from kivymd.uix.button import MDFlatButton

          dialog = MDDialog(
            title="Pontuação",
            text="Nenhuma partida jogada ainda.",
            buttons=[
                MDFlatButton(
                    text="FECHAR",
                    on_release=lambda x: dialog.dismiss(),
                )
            ],
          )
          dialog.open()

      def sair(self, *args):
          from kivy.app import App
          App.get_running_app().stop()