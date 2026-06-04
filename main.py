from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from app.view.menu_screen import MenuScreen
from app.view.board_screen import BoardScreen
from app.controller.game_controller import GameController


class BoardGameApp(MDApp):
      def build(self):
          self.theme_cls.primary_palette = "Blue"
          self.theme_cls.theme_style = "Dark"
          self.controller = GameController()

          sm = ScreenManager()
          sm.add_widget(MenuScreen(name="menu"))
          sm.add_widget(BoardScreen(name="board", controller=self.controller))
          return sm


if __name__ == "__main__":
    BoardGameApp().run()