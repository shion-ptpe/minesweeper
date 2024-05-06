from minesweeper.button import *
from minesweeper.cell import *

class CellButton(Button):
    def __init__(self, _x: int, _y: int, _width: int, _height: int):
        super().__init__(_x, _y, _width, _height)
        self.numColor = 0

    def change_num_color(self, _num):
        # 周囲の爆弾の数に応じて、数字の色が変わる
        if      _num == 1:  self.numColor = 0
        elif    _num == 2:  self.numColor = 3
        elif    _num == 3:  self.numColor = 8
        elif    _num == 3:  self.numColor = 1
        elif    _num == 5:  self.numColor = 2
        elif    _num >= 6:  self.numColor = 4

    def update(self, _cell):
        if self.isRightClicked(pyxel.mouse_x, pyxel.mouse_y):
            _cell.operate_flag()

    def draw(self, _cell, _num):
        # stateを反映して描画する
        if _cell.state == State.OPENED: pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16)
        elif _cell.state == State.CLOSE: pyxel.blt(self.x, self.y, 0, 16, 0, 16, 16)
        elif _cell.state == State.MINE: pyxel.blt(self.x, self.y, 0, 16, 0, 16, 16)
        elif _cell.state == State.OPENEDMINE: pyxel.blt(self.x, self.y, 0, 32, 0, 16, 16)
        elif _cell.state == State.MINEFLAG: pyxel.blt(self.x, self.y, 0, 48, 0, 16, 16)
        elif _cell.state == State.FLAG: pyxel.blt(self.x, self.y, 0, 48, 0, 16, 16)

        # 周囲の爆弾の数をマス目に表示
        if _cell.state == State.OPENED:
            if _num > 0:
                self.change_num_color(_num)
                pyxel.text(
                    self.x + self.width * 2 // 5,
                    self.y + self.height // 3,
                    str(_num),
                    self.numColor)

