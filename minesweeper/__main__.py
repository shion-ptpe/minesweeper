from minesweeper.buttons.cell_button import *
from minesweeper.buttons.reset_button import *
from minesweeper.buttons.start_button import *
from minesweeper.game import *
from minesweeper.game_drawer import *
import pyxel
import sys

class LevelDraw(Enum):
    EASY = ((190, 170), (31, 20))
    NORMAL = ((320, 270), (90, 60))
    HARD = ((415, 350), (140, 100))

    def __init__(self, frame, picture):
        self.frame = frame
        self.picture = picture

class AppState(Enum):
    TITLE = auto()
    MENU = auto()
    GAMEPLAYING = auto()

class App():
    def __init__(self, level="EASY"):
        self.level = Level.__members__[level.upper()]
        self.levelDraw = LevelDraw.__members__[level.upper()]
        self.paused = False
        self.appState = AppState.TITLE
        self.waitTime = 0


        pyxel.init(*self.levelDraw.frame, fps=60)
        pyxel.load("minesweeper.pyxres")
        pyxel.images[1].load(0, 0, "title.png")
        pyxel.mouse(visible=True)

        # --------
        self.game = Game()
        self.game.initialize_board(self.level)
        self.gameDrawer = GameDrawer(self.game)
        # --------
        pyxel.run(self.update, self.draw)

    def update(self):

        if self.appState == AppState.TITLE:
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                self.appState = AppState.GAMEPLAYING

        if self.appState == AppState.GAMEPLAYING and self.waitTime > 30:
            self.gameDrawer.update_board()

    def draw(self):
        pyxel.cls(13)

        if self.appState == AppState.TITLE:
            pyxel.blt(*self.levelDraw.picture, 1, 0, 0, 128, 128)

        elif self.appState == AppState.MENU:
            pass

        elif self.appState == AppState.GAMEPLAYING:
            if self.gameDrawer.gameState == GameState.GAMEPLAYING:
                if (self.waitTime > 30):
                    self.gameDrawer.draw_board(self.game)
                else:
                    self.waitTime += 1
            elif self.gameDrawer.gameState == GameState.GAMECLEAR:
                pyxel.images[2].load(0, 0, "gameclear.png")
                pyxel.blt(*self.levelDraw.picture, 2, 0, 0, 128, 128)
                if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                    self.gameDrawer.gameState = GameState.GAMEPLAYING
            elif self.gameDrawer.gameState == GameState.GAMEOVER:
                pyxel.images[2].load(0, 0, "gameover.png")
                pyxel.blt(*self.levelDraw.picture, 2, 0, 0, 128, 128)
                if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                    self.gameDrawer.gameState = GameState.GAMEPLAYING


if __name__ == '__main__':
    level = sys.argv[1] if len(sys.argv) > 1 else "EASY"
    if level.upper() in ["EASY", "NORMAL", "HARD"]:
        App(level)
    else:
        print("usage:\n```\npython -m minesweeper easy\n```")
        print('you can choice the level from "easy", "normal", "hard".')