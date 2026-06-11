from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from app.view.menu_screen import MenuScreen
from app.view.config_screen import ConfigScreen
from app.view.board_screen import BoardScreen
from app.controller.game_controller import GameController
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from app.view.result_screen import ScoreboardScreen


class BoardGameApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        self.controller = GameController()
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(ConfigScreen(name="config", controller=self.controller))
        sm.add_widget(BoardScreen(name="board", controller=self.controller))
        sm.add_widget(ScoreboardScreen(name="scoreboard",controller=self.controller))
        return sm


if __name__ == "__main__":
    BoardGameApp().run()