class BoardGameApp(MDApp):
    def build(self):
        self.theme_cls_primary_palette = 'Blue'
        self.theme_cls.theme_style = 'Lights'
        self.controller = GameController()

        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(BoardScreen(name='board', 
                                  controller='self.controller'
        ))
        return sm


if __name__ == '__main__':
    BoardGameApp().run()

