from minesweeper.button import *
from minesweeper.game import *
import pyxel

class ResetButton(Button):
    def __init__(self, _x: int, _y: int, _width: int, _height: int):
        super().__init__(_x, _y, _width, _height)
        self.isClicked: bool = False

    def draw(self):
        if self.isLeftClicked(pyxel.mouse_x, pyxel.mouse_y):
            pyxel.blt(self.x, self.y, 0, 80, 0, 16, 16)
        else:
            pyxel.blt(self.x, self.y, 0, 64, 0, 16, 16)

    def update(self, _game: Game):
        if self.isLeftClicked(pyxel.mouse_x, pyxel.mouse_y):
            _game.initialize_board(_game.level)

