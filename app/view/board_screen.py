from kivymd.uix.screen import MDScreen


class BoardScreen(MDScreen):
      def __init__(self, controller=None, **kwargs):
          super().__init__(**kwargs)
          self.controller = controller