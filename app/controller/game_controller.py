from app.models.game import Game


class GameController:
  def __init__(self):
    self.game = None
    self.on_board_update = None

  
  def start_game(self, player_names: lists[str]):
      self.game = Game(players=player_names)
      self._notify_view()


  def make_move(self, row: int, col: int) -> bool:
      success = self.game.play(row, col)
      if success:
         self._notify_view()
      return success
  

  def get_board_state(self) -> list:
      return self.game.board.get_state()
  

  def _notify_view(self):
      if self.on_board_update:
         self.on_board_update(self.get_board_state())
