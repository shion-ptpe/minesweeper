import pytest
from minesweeper.game import *
from minesweeper.cell import *
import numpy as np


@pytest.fixture
def games():
    easy_early = Game.deserialize("EASY\nCCCCCCCCCC\nCCCCCCCCMM\nCCCCCCCCCC\nMMCCCCCCCC\nCCCCCCMCCC\nCCCCMCCCCM\nCCCCCMCMMC\nCCCCCCCCCC")
    
    easy_mid = Game.deserialize("EASY\nOOMCOOOOOO\nOOOXOOOOOO\nOOOOOOOXOO\nOOOOOOOCOO\nOOOOOOXXOO\nFMOOOOOMOO\nOOOOOMOCOO\nOOOOOMFCFM")
    easy_final = Game.deserialize("EASY\nOOOOOOOOOO\nOOOOOOOOMM\nOOOOOOOOOO\nMMOOOOOOOO\nOOOOOOMOOO\nOOOOMOOOOM\nOOOOOMOMMO\nOOOOOOOOOO") 
    assert np.array_equal(easy_mid.board,np.array( [[Cell(State.OPENED), Cell(State.OPENED), Cell(State.MINE),   Cell(State.CLOSE),    Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED),   Cell(State.OPENED),   Cell(State.OPENED), Cell(State.OPENED)],
                                                    [Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED), Cell(State.MINEFLAG), Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED),   Cell(State.OPENED),   Cell(State.OPENED), Cell(State.OPENED)],
                                                    [Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED),   Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED),   Cell(State.MINEFLAG), Cell(State.OPENED), Cell(State.OPENED)],
                                                    [Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED),   Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED),   Cell(State.CLOSE),    Cell(State.OPENED), Cell(State.OPENED)],
                                                    [Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED),   Cell(State.OPENED), Cell(State.OPENED), Cell(State.MINEFLAG), Cell(State.MINEFLAG), Cell(State.OPENED), Cell(State.OPENED)],
                                                    [Cell(State.FLAG),   Cell(State.MINE),   Cell(State.OPENED), Cell(State.OPENED),   Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED),   Cell(State.MINE),     Cell(State.OPENED), Cell(State.OPENED)],
                                                    [Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED),   Cell(State.OPENED), Cell(State.MINE),   Cell(State.OPENED),   Cell(State.CLOSE),    Cell(State.OPENED), Cell(State.OPENED)],
                                                    [Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED), Cell(State.OPENED),   Cell(State.OPENED), Cell(State.MINE),   Cell(State.FLAG),     Cell(State.CLOSE),    Cell(State.FLAG),   Cell(State.MINE)]] ))
    normal = Game.deserialize("NORMAL\nCCCMCMCCMCMCCMCCCC\nCMCOCCCCCCCCCCMCMC\nOOOOOMCCMCCCCMCCCC\nOOOOOCCCCCCMCMMCCC\nOOOOOOCCCCCCCCCCCC\nOOOOOOMCCCMCCCMCCC\nMCOOOOCCCCCCCCCCCC\nMCMCOCCCCMCMCCCCCC\nCCCCMCCCMCMCCCCMMC\nCCCMCCCCCCCCCCMCCC\nCCCCCCMMCCCMCCCCCC\nCCCCCMCMCCCCMCCCCM\nCCCCCCCCCCCCCCCCCM\nCCCCMCCCMMCCCCCCCC")

    hard = Game.deserialize("HARD\nCCCCMCCMMCCCCCCCCCCMCMMC\nMCMCCMCCMCCCCCCCMCCCCCMM\nCCCMCCCMCCCCCMCCCMMCCCCC\nMCMMCCMCCMCMMCCCCMCCCCMC\nCMMCCCCMCCMCMMCCCCCCCMCC\nCCMCMCCCCMCCCCMCMCMCCCCM\nCCMMMCCCCCCCCCMCCCCCMCCC\nCCCCCCCCCCMCMMCCCMCCCCCC\nCCCCCCCCMCMMCCCCMCMMCCCC\nCCCCMMMCCOOCCCMCCCMCMCMC\nCCCMCMCMOOOOMCCCMMCCCMCC\nCCCCCCCMCOOCCMCCCCCCCCMC\nMCMCCMCCMCMCCMCCMCCMCCCC\nMCCCCCCCCMCMCMCCCCCCMCCC\nCMCCMCMCMMCCCCCCCCCCCMCC\nCCCCCCCCCCCCCCCCCCCCMCCC\nCCCMCCCCCCCCMCCCCMCCMMCC\nCCCMCCMCCCCCCCMCMCCCMMCC\nCMCCCCCCCCCCCCCCMCCMCMCC")
    return (easy_early, easy_mid, easy_final, normal, hard)

def test_init():
    game = Game()
    assert game.level == None
    assert game.height == 0
    assert game.width == 0
    assert game.numMine == 0
    assert game.numCell == 0
    assert  np.array_equal(game.board, np.array([]))


def test_initialize_board():
    game = Game()
    game.initialize_board(Level.EASY)
    assert game.height == 8
    assert game.width == 10
    assert game.numMine == 10
    assert type(game.board) == np.ndarray
    assert len(game.board) == game.height
    assert len(game.board[0]) == game.width
    assert [type(x) for row in game.board for x in row] == [ Cell for _ in range(game.height * game.width) ]

def test_initialize_mine():
    game = Game()
    for _selectedX, _selectedY in [(x,y) for y in range(game.height) for x in range(game.width)]:
        countMine = 0
        game.initialize_board(level=Level.EASY)
        game.initialize_mine(_selectedX, _selectedY)
        for y, _ in enumerate(game.board):
            for x, cell in enumerate(_):
                if cell.isMine:    # 配置した爆弾の数のカウント
                    countMine += 1
                if abs(_selectedY-y) <= game.NOMINERANGE and abs(_selectedX-x) <= game.NOMINERANGE:
                    assert cell.isMine == False    # 押した場所の周辺に爆弾がない
        assert countMine == game.numMine
        countMine = 0

def test_count_opened_cell(games):
    easy_early, easy_mid, easy_final, normal, hard = games
    assert easy_early.count_opened_cell() == 0
    assert easy_mid.count_opened_cell() == 63
    assert easy_final.count_opened_cell() == Level.EASY.height * Level.EASY.width - Level.EASY.mine
    assert normal.count_opened_cell() == 28
    assert hard.count_opened_cell() == 8

def test_count_around_mine(games):
    easy_early, easy_mid, easy_final, normal, hard = games
    assert easy_mid.count_around_mine(0,0) == 0
    assert easy_mid.count_around_mine(7,3) == 3
    assert easy_mid.count_around_mine(6,5) == 4
    assert easy_mid.count_around_mine(9,7) == None

    with pytest.raises(ValueError):
        assert easy_mid.count_around_mine(7,9)

def test_num_mine_list(games):
    easy_early, easy_mid, easy_final, normal, hard = games
    assert easy_mid.num_mine_list() == [[0,   1,None,   2,1,   0,   0,   0,0,   0],
                                        [0,   1,   2,None,1,   0,   1,   1,1,   0],
                                        [0,   0,   1,   1,1,   0,   1,None,1,   0],
                                        [0,   0,   0,   0,0,   1,   3,   3,2,   0],
                                        [1,   1,   1,   0,0,   1,None,None,2,   0],
                                        [1,None,   1,   0,1,   2,   4,None,2,   0],
                                        [1,   1,   1,   0,2,None,   3,   1,2,   1],
                                        [0,   0,   0,   0,2,None,   2,   0,1,None]]
    assert normal.num_mine_list() == [  [1, 1, 2, None, 2, None, 1, 1, None, 2, None, 1, 1, None, 2, 2, 1, 1],
                                        [1, None, 2, 1, 3, 2, 2, 2, 2, 3, 1, 1, 2, 3, None, 2, None, 1],
                                        [1, 1, 1, 0, 1, None, 1, 1, None, 1, 1, 1, 3, None, 4, 3, 1, 1],
                                        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, None, 3, None, None, 1, 0, 0],
                                        [0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 2, 2, 2, 3, 3, 2, 0, 0],
                                        [1, 1, 0, 0, 0, 1, None, 1, 0, 1, None, 1, 0, 1, None, 1, 0, 0],
                                        [None, 3, 1, 1, 0, 1, 1, 1, 1, 2, 3, 2, 1, 1, 1, 1, 0, 0],
                                        [None, 3, None, 2, 1, 1, 0, 1, 2, None, 3, None, 1, 0, 1, 2, 2, 1],
                                        [1, 2, 2, 3, None, 1, 0, 1, None, 3, None, 2, 1, 1, 2, None, None, 1],
                                        [0, 0, 1, None, 2, 2, 2, 3, 2, 2, 2, 2, 1, 1, None, 3, 2, 1],
                                        [0, 0, 1, 1, 2, 2, None, None, 2, 0, 1, None, 2, 2, 1, 1, 1, 1],
                                        [0, 0, 0, 0, 1, None, 4, None, 2, 0, 1, 2, None, 1, 0, 0, 2, None],
                                        [0, 0, 0, 1, 2, 2, 2, 2, 3, 2, 1, 1, 1, 1, 0, 0, 2, None],
                                        [0, 0, 0, 1, None, 1, 0, 1, None, None, 1, 0, 0, 0, 0, 0, 1, 1]]

    assert hard.num_mine_list() == [[1, 2, 1, 2, None, 2, 2, None, None, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, None, 2, None, None, 3],
                                    [None, 2, None, 3, 3, None, 3, 4, None, 2, 0, 0, 1, 1, 1, 1, None, 3, 3, 2, 2, 3, None, None],
                                    [2, 4, 4, None, 3, 2, 3, None, 3, 2, 2, 2, 3, None, 1, 1, 3, None, None, 1, 0, 2, 3, 3],
                                    [None, 4, None, None, 2, 1, None, 3, 3, None, 3, None, None, 4, 2, 0, 2, None, 3, 1, 1, 2, None, 1],
                                    [2, None, None, 5, 2, 2, 2, None, 3, 3, None, 4, None, None, 2, 2, 2, 3, 2, 1, 1, None, 3, 2],
                                    [1, 4, None, 6, None, 2, 1, 1, 2, None, 2, 2, 2, 4, None, 3, None, 2, None, 2, 2, 2, 2, None],
                                    [0, 2, None, None, None, 2, 0, 0, 1, 2, 2, 2, 2, 4, None, 3, 2, 3, 2, 2, None, 1, 1, 1],
                                    [0, 1, 2, 3, 2, 1, 0, 1, 1, 3, None, 4, None, None, 2, 2, 2, None, 3, 3, 2, 1, 0, 0],
                                    [0, 0, 0, 1, 2, 3, 2, 2, None, 3, None, None, 3, 3, 2, 2, None, 4, None, None, 2, 2, 1, 1],
                                    [0, 0, 1, 2, None, None, None, 3, 2, 2, 2, 3, 2, 2, None, 3, 3, 5, None, 4, None, 3, None, 1],
                                    [0, 0, 1, None, 4, None, 5, None, 2, 0, 0, 1, None, 3, 2, 2, None, None, 2, 2, 2, None, 3, 2],
                                    [1, 2, 2, 2, 3, 2, 4, None, 3, 2, 1, 2, 3, None, 2, 2, 3, 3, 2, 1, 2, 2, None, 1],
                                    [None, 3, None, 1, 1, None, 2, 2, None, 3, None, 2, 4, None, 3, 1, None, 1, 1, None, 2, 2, 1, 1],
                                    [None, 4, 2, 2, 2, 3, 2, 3, 4, None, 4, None, 3, None, 2, 1, 1, 1, 1, 2, None, 2, 1, 0],
                                    [2, None, 1, 1, None, 2, None, 2, None, None, 3, 1, 2, 1, 1, 0, 0, 0, 0, 2, 3, None, 1, 0],
                                    [1, 1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 0, 0, 1, 1, 1, 2, None, 4, 2, 0],
                                    [0, 0, 2, None, 2, 1, 1, 1, 0, 0, 0, 1, None, 2, 1, 2, 2, None, 1, 3, None, None, 2, 0],
                                    [1, 1, 3, None, 2, 1, None, 1, 0, 0, 0, 1, 1, 2, None, 3, None, 3, 2, 3, None, None, 3, 0],
                                    [1, None, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 3, None, 2, 1, None, 4, None, 2, 0]]

def test_open_board(games):
    easy_early, easy_mid, easy_final, normal, hard = games
    answer1 = Game.deserialize("EASY\nOOOOOOOOCC\nOOOOOOOOMM\nOOOOOOOOCC\nMMOOOOOCCC\nCCCOOCMCCC\nCCCCMCCCCM\nCCCCCMCMMC\nCCCCCCCCCC")
    answer2 = Game.deserialize("EASY\nOOOOOOOOCC\nOOOOOOOOMM\nOOOOOOOOCC\nMMOOOOOCCC\nOOOOOCMCCC\nOOOOMCCCCM\nOOOOCMCMMC\nOOOOOCCCCC")
    answer3 = Game.deserialize("EASY\nOOOOOOOOOC\nOOOOOOOOMM\nOOOOOOOOCC\nMMOOOOOCCC\nOOOOOCMCCC\nOOOOMCCCCM\nOOOOCMCMMC\nOOOOOCCCCC")
    """ CCCCCCCCCC
        CCCCCCCCMM
        CCCCCCCCCC
        MMCCCCCCCC
        CCCCCCMCCC
        CCCCMCCCCM
        CCCCCMCMMC
        CCCCCCCCCC"""
    easy_early.open_board(3,3)
    assert easy_early == answer1
    """ OOOOOOOCCC
        OOOOOOOCMM
        CCCOOOOCCC
        MMCOOCCCCC
        CCCCCCMCCC
        CCCCMCCCCM
        CCCCCMCMMC
        CCCCCCCCCC """
    easy_early.open_board(0,7)
    assert easy_early == answer2
    """ OOOOOOOOOC
        OOOOOOOOMM
        OOOOOOOOCC
        MMOOOOOCCC
        OOOOOCMCCC
        OOOOMCCCCM
        OOOOCMCMMC
        OOOOOCCCCC"""
    easy_early.open_board(8,0)
    assert easy_early == answer3
    """ OOOOOOOOOC
        OOOOOOOOMM
        OOOOOOOOCC
        MMOOOOOCCC
        OOOOOCMCCC
        OOOOMCCCCM
        OOOOCMCMMC
        OOOOOCCCCC """
    
def test_open_all_mine(games):
    easy_mid1 = games[1]
    easy_mid2 = games[1]
    easy_mid1.open_all_mine()
    for cell1, cell2 in zip(easy_mid1.board.flatten(), easy_mid2.board.flatten()):
        if cell2.isMine:
            assert cell1.state == State.OPENEDMINE

def test_is_valid_cell(games):
    easy_early, easy_mid, easy_final, normal, hard = games
    assert easy_early.is_valid_cell(1,3)
    assert easy_early.is_valid_cell(9,7)
    assert not easy_early.is_valid_cell(-1,6)
    assert not easy_early.is_valid_cell(0,8)

def test_four_directions_safe_cell(games):
    easy_early, easy_mid, easy_final, normal, hard = games
    assert easy_mid.four_directions_safe_cell(0,0) == [(1, 0), (0, 1)]
    assert easy_mid.four_directions_safe_cell(2,0) == [(1, 0), (3, 0), (2, 1)]
    assert easy_mid.four_directions_safe_cell(4,3) == [(4, 2), (3, 3), (5, 3), (4, 4)]
    """ OOMCOOOOOO
        OOOXOOOOOO
        OOOOOOOXOO
        OOOOOOOCOO
        OOOOOOXXOO
        FMOOOOOMOO
        OOOOOMOCOO
        OOOOOMFCFM"""

def test_deserialize(games):
    easy_early, easy_mid, easy_final, normal, hard = games
    with pytest.raises(TypeError):
        _ = Game.deserialize(1)

    with pytest.raises(ValueError):
        _ = Game.deserialize("some invalid string")

    assert Game.deserialize(easy_early.serialize()) == easy_early
    assert Game.deserialize(easy_mid.serialize()) == easy_mid
    assert Game.deserialize(easy_final.serialize()) == easy_final
    assert Game.deserialize(normal.serialize()) == normal
    assert Game.deserialize(hard.serialize()) == hard


def test_serialize(games):
    easy_early, easy_mid, easy_final, normal, hard = games
    assert easy_early.serialize() == "EASY\nCCCCCCCCCC\nCCCCCCCCMM\nCCCCCCCCCC\nMMCCCCCCCC\nCCCCCCMCCC\nCCCCMCCCCM\nCCCCCMCMMC\nCCCCCCCCCC"
    assert easy_mid.serialize() == "EASY\nOOMCOOOOOO\nOOOXOOOOOO\nOOOOOOOXOO\nOOOOOOOCOO\nOOOOOOXXOO\nFMOOOOOMOO\nOOOOOMOCOO\nOOOOOMFCFM"
    assert easy_final.serialize() == "EASY\nOOOOOOOOOO\nOOOOOOOOMM\nOOOOOOOOOO\nMMOOOOOOOO\nOOOOOOMOOO\nOOOOMOOOOM\nOOOOOMOMMO\nOOOOOOOOOO"
    assert normal.serialize() == "NORMAL\nCCCMCMCCMCMCCMCCCC\nCMCOCCCCCCCCCCMCMC\nOOOOOMCCMCCCCMCCCC\nOOOOOCCCCCCMCMMCCC\nOOOOOOCCCCCCCCCCCC\nOOOOOOMCCCMCCCMCCC\nMCOOOOCCCCCCCCCCCC\nMCMCOCCCCMCMCCCCCC\nCCCCMCCCMCMCCCCMMC\nCCCMCCCCCCCCCCMCCC\nCCCCCCMMCCCMCCCCCC\nCCCCCMCMCCCCMCCCCM\nCCCCCCCCCCCCCCCCCM\nCCCCMCCCMMCCCCCCCC"
    assert hard.serialize() == "HARD\nCCCCMCCMMCCCCCCCCCCMCMMC\nMCMCCMCCMCCCCCCCMCCCCCMM\nCCCMCCCMCCCCCMCCCMMCCCCC\nMCMMCCMCCMCMMCCCCMCCCCMC\nCMMCCCCMCCMCMMCCCCCCCMCC\nCCMCMCCCCMCCCCMCMCMCCCCM\nCCMMMCCCCCCCCCMCCCCCMCCC\nCCCCCCCCCCMCMMCCCMCCCCCC\nCCCCCCCCMCMMCCCCMCMMCCCC\nCCCCMMMCCOOCCCMCCCMCMCMC\nCCCMCMCMOOOOMCCCMMCCCMCC\nCCCCCCCMCOOCCMCCCCCCCCMC\nMCMCCMCCMCMCCMCCMCCMCCCC\nMCCCCCCCCMCMCMCCCCCCMCCC\nCMCCMCMCMMCCCCCCCCCCCMCC\nCCCCCCCCCCCCCCCCCCCCMCCC\nCCCMCCCCCCCCMCCCCMCCMMCC\nCCCMCCMCCCCCCCMCMCCCMMCC\nCMCCCCCCCCCCCCCCMCCMCMCC"

def test_eq():
    game1 = Game.deserialize("EASY\nOOMCOOOOOO\nOOOXOOOOOO\nOOOOOOOXOO\nOOOOOOOCOO\nOOOOOOXXOO\nFMOOOOOMOO\nOOOOOMOCOO\nOOOOOMFCFM") 
    game2 = Game.deserialize("EASY\nOOMCOOOOOO\nOOOXOOOOOO\nOOOOOOOXOO\nOOOOOOOCOO\nOOOOOOXXOO\nFMOOOOOMOO\nOOOOOMOCOO\nOOOOOMFCFM")
    assert game1 == game2