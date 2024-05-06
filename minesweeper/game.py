from minesweeper.cell import *
from enum import Enum
import numpy as np
import random
import re


class Level(Enum):
    EASY = (8, 10, 10)
    NORMAL = (14, 18, 40)
    HARD = (19, 24, 108)
    
    def __init__(self, height, width, mine):
        self.height = height
        self.width = width
        self.mine = mine

class Game:

    """
    Gameで扱う変数の初期化
    """
    NOMINERANGE = 1
    def __init__(self) -> None:
        self.level = None
        self.height = 0
        self.width = 0
        self.numMine = 0
        self.numCell = 0
        self.board = np.array([])

    @property
    def numOpenableCell(self):
        return self.numCell - self.numMine
        
    """
    boardの初期化
    levelに応じて高さ、幅、mineの数を設定
    self.boardは Cell(state=State.CLOSE) で初期化 ->  initialize_mineで爆弾配置
    """
    def initialize_board(self, level=Level.EASY):
        self.level = level
        self.height, self.width, self.numMine = self.level.value
        self.numCell = self.height * self.width
        self.board = np.array([[Cell() for _ in range(self.width)] for _ in range(self.height)])

    """
    mineの初期化
    _selectedX, _selectedYの周囲(NOMINERANGE)にmineは置かない
    .bury_mine()でcellにmineの設置
    """
    def initialize_mine(self, _selectedX, _selectedY):
        if self.numCell-9 < self.numMine:
            raise ValueError("Number of mines exceeds the size of the board.")
        for _ in range(self.numMine):
            while True:
                y, x = random.randint(0, self.height-1), random.randint(0, self.width-1)
                if (not self.board[y][x].isMine) and (not (x,y) in self.eight_directions_safe_cell(_selectedX, _selectedY)):
                    break
            self.board[y][x].bury_mine()
        self.num_mine_list()
        self.open_board(_selectedX, _selectedY)

    """
    開いているCellを数える
    Appがゲームの終了判定時につかう
    """
    def count_opened_cell(self) -> int:
        return sum(cell.isOpened for cell in self.board.flatten())
    
    """
    count_num_mine -> count_around_mineに改名
    x,yを指定して周囲のmineの数を数える
    範囲外の指定はValueError
    mineを指定したらNone
    """
    def count_around_mine(self, _selectX, _selectY) -> int:
        if not self.is_valid_cell(_selectX, _selectY):
            raise ValueError
        if self.board[_selectY][_selectX].isMine:
            return None
        slice = self.board[max(_selectY-1, 0):min(_selectY+1, self.height)+1, max(_selectX-1, 0):min(_selectX+1, self.width)+1]
        return sum(cell.isMine for cell in slice.flatten())

    """
    Cellごとの周囲のmineを数え、リストにして返す。
    mineはNoneで返る
    Cellの数を描画するメソッドはこのリストを参照し、数が書かれている座標にはmineの数を表す色をつける
    """
    def num_mine_list(self) -> list:
        self.numMineList = []
        for y in range(self.height):
            self.numMineList.append([self.count_around_mine(x, y) for x in range(self.width)])
        return self.numMineList
    
    """
    押された座標x,yを起点とし、周囲のCellを開く
    """
    def open_board(self, _selectX, _selectY):
        if self.is_valid_cell(_selectX, _selectY) and self.numMineList[_selectY][_selectX] != 0:
            self.board[_selectY][_selectX].open()
            return
        open_queue = set([(_selectX, _selectY)])
        will_search = set(self.four_directions_safe_cell(_selectX,_selectY))
        while will_search:
            next_search = set()
            for x, y in will_search.copy():
                open_queue.add((x, y))
                if not self.count_around_mine(x, y):  # 番号付きのCellでなければ再帰でさらにcellをopenする
                    next_search |= set(self.four_directions_safe_cell(x, y))
            will_search = next_search - open_queue

        for (x,y) in open_queue:
            assert self.board[y][x].isMine == False
            self.board[y][x].state_update(State.OPENED)

    """
    全てのmineを開く。
    ゲーム終了時の答え合わせに使う
    """
    def open_all_mine(self):
        for cell in self.board.flatten():
            cell.open_mine() 

    """
    boardの範囲外を指定したらFalse
    """
    def is_valid_cell(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    """
    board内のx,yを指定すると周囲四方向の要素を確認し、isMine==Trueだったらその座標をリストにまとめて返す
    """
    def four_directions_safe_cell(self, x, y): 
        openableCell = []
        for _y in [-1,0,1]:
            for _x in [-1,0,1]:
                if abs(_x+_y)==1 and self.is_valid_cell(x+_x, y+_y) and (not self.board[y+_y][x+_x].isMine):
                    openableCell.append((x+_x, y+_y))
        return openableCell 

    """
    board内のx,yを指定すると周囲八方向の要素を確認し、isMine==Trueだったらその座標をリストにまとめて返す
    """
    def eight_directions_safe_cell(self, x, y):
        return [(x+_x, y+_y) for _y in [-1,0,1] for _x in [-1,0,1] if self.is_valid_cell(x+_x, y+_y) and (not self.board[y+_y][x+_x].isMine)]

    """
    シリアライズ
    cell.serialize()はCellのシリアライズを呼び出す。<-状態がC, F, O, M, Xのいずれかで帰ってくる
    """
    def serialize(self):
        '''
        マスが閉じている=C
        空のマスにフラグが立ってる=F
        マスが空いている=O
        爆弾が入っていて閉じている=M
        爆弾があってフラグが立ってる=X
        "EASY\nOOMCOOOOOO\nOOOXOOOOOO\nOOOOOOOXOO\nOOOOOOOCOO\nOOOOOOXXOO\nFMOOOOOMOO\nOOOOOMOCOO\nOOOOOMFCFM"
        '''
        serializeBoard = []
        for board in self.board:
            serializeBoard.append(''.join(list(map(lambda cell: cell.serialize(), board))))
        return self.level.name + '\n' + '\n'.join(serializeBoard)
    
    """
    デシリアライズ
    typeが違う or 正規表現にマッチしない -> エラー
    Game.deserialize("文字列")のように呼び出す。
    """
    @classmethod
    def deserialize(cls, strings:str):
        if type(strings) is not str:
            raise TypeError
        if not (re.fullmatch(r"^EASY\n(?:[OCMFX]{10}\n){7}[OCMFX]{10}$", strings) or \
                re.fullmatch(r"^NORMAL\n(?:[OCMFX]{18}\n){13}[OCMFX]{18}$", strings) or \
                re.fullmatch(r"^HARD\n(?:[OCMFX]{24}\n){18}[OCMFX]{24}$", strings)):
            raise ValueError

        data = strings.split('\n')
        game = cls()
        game.level = Level.__members__[data[0]]
        game.initialize_board(game.level)
        

        board = []
        for row in data[1::]:
            board.append([Cell.deserialize(cell) for cell in row])
        game.board = np.array(board)
        game.num_mine_list()


        return game

    def __eq__(self, other):
        return isinstance(other, Game) and \
                self.level == other.level and \
                self.height == other.height and \
                self.width == other.width and \
                self.numMine == other.numMine and \
                self.numCell == other.numCell and \
                np.array_equal(self.board, other.board)
