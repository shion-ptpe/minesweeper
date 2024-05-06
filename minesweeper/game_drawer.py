from minesweeper.buttons.cell_button import *
from minesweeper.buttons.reset_button import *
from minesweeper.buttons.start_button import *
from minesweeper.game import *
from minesweeper.cell import *
from enum import Enum, auto

class GameState(Enum):
    GAMEPLAYING = auto()
    GAMEPAUSE = auto()
    GAMEOVER = auto()
    GAMECLEAR = auto()

class GameDrawer:
    def __init__(self, _game):
        self.game = _game
        self.width = _game.width
        self.height = _game.height
        self.resetButton:   ResetButton = ResetButton(0, 0, 16, 16)
        self.startButton:   StartButton# = StartButton()
        self.board = [[CellButton(16 + x * 16, 24 + y * 16, 16, 16) for x in range(self.width)] for y in range(self.height)]
        self.isFirstOpen = True
        self.gameState = GameState.GAMEPLAYING
        self.keylock = None

    def update_board(self):
        self.resetButton.update(self.game)
        if self.resetButton.isLeftClicked(pyxel.mouse_x, pyxel.mouse_y):
            self.isFirstOpen = True
            self.keylock = None

        for y in range(self.height):
            for x in range(self.width):
                cell = self.game.board[y][x]
                cell_button = self.board[y][x]

                cell_button.update(cell)
                if self.keylock == None:
                    if cell_button.isLeftClicked(pyxel.mouse_x, pyxel.mouse_y):
                        if self.isFirstOpen:
                            self.game.initialize_mine(x, y)
                            self.isFirstOpen = False
                        else:
                            try:
                                self.game.open_board(x, y)
                            except StepOnTheMine:
                                self.keylock = GameState.GAMEOVER
                                self.finish_gameover()
                elif self.keylock == GameState.GAMECLEAR:
                    self.finish_clear()
                elif self.keylock == GameState.GAMEOVER:
                    self.finish_gameover()
                    pass
                elif self.keylock == GameState.GAMEPAUSE:
                    pass

        if self.game.count_opened_cell() == self.game.numOpenableCell:
            self.keylock = GameState.GAMECLEAR
            self.finish_clear()


    def draw_board(self, _game):
        self.resetButton.draw()
        for y in range(self.height):
            for x in range(self.width):
                cell = _game.board[y][x]
                self.board[y][x].draw(cell, _game.count_around_mine(x, y))

    def finish_clear(self):
        # print('GameClear:)')
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            self.gameState = GameState.GAMECLEAR


    def finish_gameover(self):
        # print('GazmeOver:(')
        self.game.open_all_mine()
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            self.gameState = GameState.GAMEOVER
