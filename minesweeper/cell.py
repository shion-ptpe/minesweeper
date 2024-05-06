from minesweeper.button import *
from enum import Enum

class State(Enum):
    CLOSE = 1
    FLAG = 2
    OPENED = 3
    MINE = 4
    MINEFLAG = 5
    OPENEDMINE = 6


"""
Mineを押したときに専用の例外を発生させる
"""
class StepOnTheMine(Exception):
    pass

class Cell:
    """
    Cellの初期化
    state変数を指定することで他の変数も定義される(state_update)
    """
    def __init__(self, state = State.CLOSE):
        self.state = state
        self.state_update(self.state)

    """
    引数staetの値に対応して自分(self)の変数を一括で変更
    """
    def state_update(self, state):
        if state == State.CLOSE:
            self.state = State.CLOSE
            self.isFlag = False
            self.isOpened = False
            self.isMine = False
        elif state == State.FLAG:
            self.state = State.FLAG
            self.isFlag = True
            self.isOpened = False
            self.isMine = False
        elif state == State.OPENED:
            self.state = State.OPENED
            self.isFlag = False
            self.isOpened = True
            self.isMine = False
        elif state == State.MINE:
            self.state = State.MINE
            self.isFlag = False
            self.isOpened = False
            self.isMine = True
        elif state == State.MINEFLAG:
            self.state = State.MINEFLAG
            self.isFlag = True
            self.isOpened = False
            self.isMine = True
        elif state == State.OPENEDMINE:
            self.state = State.OPENEDMINE
            self.isFlag = False
            self.isOpened = True
            self.isMine = True

    """
    Cellを開く関数
    isMine==Trueでopen関数を読んだらStepOnTheMineエラー
    """
    def open(self):
        if self.isOpened:
            pass
        elif self.isFlag:
            pass
        elif self.isMine:
            self.state_update(State.OPENEDMINE)
            raise StepOnTheMine
        else:
            self.state_update(State.OPENED)

    """
    Mineを開く
    ゲーム終了時の答え合わせに使う
    """
    def open_mine(self):
        if self.isMine:
            self.state_update(State.OPENEDMINE)

    """
    フラグの上げ下げを行う
    """
    def operate_flag(self):
        if self.state == State.OPENED:
            pass
        elif self.state == State.CLOSE:
            self.state_update(State.FLAG)
        elif self.state == State.FLAG:
            self.state_update(State.CLOSE)
        elif self.state == State.MINE:
            self.state_update(State.MINEFLAG)
        elif self.state == State.MINEFLAG:
            self.state_update(State.MINE)


    """
    mineを埋め込む
    """
    def bury_mine(self):
        if self.isFlag:
            self.state_update(State.MINEFLAG)
        elif not self.isOpened:
            self.state_update(State.MINE)
        else:
            raise ValueError

    def __eq__(self, other):
        return isinstance(other, Cell) and \
                self.state == other.state and \
                self.isMine == other.isMine and \
                self.isFlag == other.isFlag and \
                self.isOpened == other.isOpened

    """
    シリアライズ
    """
    def serialize(self):
        '''
        マスが閉じている=C
        空のマスにフラグが立ってる=F
        マスが空いている=O
        爆弾が入っていて閉じている=M
        爆弾があってフラグが立ってる=X
        '''
        if self.state == State.OPENEDMINE:
            raise ValueError
        return 'X' if self.state == State.MINEFLAG else self.state.name[0]

    """
    デシリアライズ
    @classmethodをつけることで、Cell.関数名のように直接メソッドが使えるようになる
    """
    @classmethod
    def deserialize(cls, char):
        board = cls()
        if char == 'C':
            board.state_update(State.CLOSE)
        elif char == 'F':
            board.state_update(State.FLAG)
        elif char == 'O':
            board.state_update(State.OPENED)
        elif char == 'M':
            board.state_update(State.MINE)
        elif char == 'X':
            board.state_update(State.MINEFLAG)
        else:
            raise ValueError
        return board
