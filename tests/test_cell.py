import pytest
from minesweeper.cell import *
import copy

@pytest.fixture
def cell():
    c = Cell()
    c.state=State.CLOSE; c.isFlag = False; c.isOpened = False; c.isMine = False; 
    f = Cell()
    f.state=State.FLAG; f.isFlag = True; f.isOpened = False; f.isMine = False; 
    o = Cell()
    o.state=State.OPENED; o.isFlag = False; o.isOpened = True; o.isMine = False; 
    m = Cell()
    m.state=State.MINE; m.isFlag = False; m.isOpened = False; m.isMine = True; 
    mf = Cell()
    mf.state=State.MINEFLAG; mf.isFlag = True; mf.isOpened = False; mf.isMine = True; 
    return (c,f,o,m,mf)

def test_init():
    c1 = Cell(State.CLOSE)
    assert c1.state == State.CLOSE
    assert c1.isFlag == False
    assert c1.isOpened == False
    assert c1.isMine == False
    c2 = Cell(State.FLAG)
    assert c2.state == State.FLAG
    assert c2.isFlag == True
    assert c2.isOpened == False
    assert c2.isMine == False
    c3 = Cell(State.OPENED)
    assert c3.state == State.OPENED
    assert c3.isFlag == False
    assert c3.isOpened == True
    assert c3.isMine == False
    c4 = Cell(State.MINE)
    assert c4.state == State.MINE
    assert c4.isFlag == False
    assert c4.isOpened == False
    assert c4.isMine == True
    c5 = Cell(State.MINEFLAG)
    assert c5.state == State.MINEFLAG
    assert c5.isFlag == True
    assert c5.isOpened == False
    assert c5.isMine == True

def test_state_update(cell):
    c,f,o,m,mf = cell
    cell = Cell()
    cell.state_update(State.CLOSE)
    assert cell== c
    cell.state_update(State.FLAG) 
    assert cell == f
    cell.state_update(State.OPENED)
    assert cell == o
    cell.state_update(State.MINE)
    assert cell == m
    cell.state_update(State.MINEFLAG)
    assert cell == mf
    
def test_open(cell):
    c,f,o,m,mf = cell
    cell = Cell(state=State.CLOSE)
    cell.open()
    assert cell == o
    cell = Cell(state=State.FLAG)
    cell.open()
    assert cell == f
    cell = Cell(state=State.OPENED)
    cell.open()
    assert cell == o
    cell = Cell(state=State.MINEFLAG)
    cell.open()
    assert cell == mf

    with pytest.raises(StepOnTheMine):
        cell = Cell(state=State.MINE)
        cell.open()

def test_open_mine(cell):
    c1,f1,o1,m1,mf1 = copy.deepcopy(cell)
    c2,f2,o2,m2,mf2 = cell
    c1.open_mine()
    assert c1== c2
    f1.open_mine()
    assert f1== f2
    o1.open_mine()
    assert o1 == o2
    m1.open_mine()
    assert m1.state == State.OPENEDMINE
    mf1.open_mine()
    assert mf1.state == State.OPENEDMINE


def test_operate_flag(cell):
    c1,f1,o1,m1,mf1 = copy.deepcopy(cell)
    c2,f2,o2,m2,mf2 = cell
    o1.operate_flag()
    assert o1 == o2
    c1.operate_flag()
    assert c1 == f2
    f1.operate_flag()
    assert f1 == c2
    m1.operate_flag()
    assert m1 == mf2
    mf1.operate_flag()
    assert mf1 == m2
    

def test_bury_mine(cell):
    c1,f1,o1,m1,mf1 = copy.deepcopy(cell)
    c2,f2,o2,m2,mf2 = cell
    c1.bury_mine()
    assert c1 == m2
    f1.bury_mine()
    assert f1 == mf2

    with pytest.raises(ValueError):
        o1.bury_mine()
        m1.bury_mine()
        mf1.bury_mine()


def test_serialize(cell):
    c,f,o,m,mf = cell
    assert c.serialize() == 'C'
    assert f.serialize() == 'F'
    assert o.serialize() == 'O'
    assert m.serialize() == 'M'   
    assert mf.serialize() == 'X'
    with pytest.raises(ValueError):
        Cell(state=State.OPENEDMINE).serialize()

def test_deserialize(cell):
    c,f,o,m,mf = cell
    assert Cell.deserialize('C') == c
    assert Cell.deserialize('F') == f
    assert Cell.deserialize('O') == o
    assert Cell.deserialize('M') == m
    assert Cell.deserialize('X') == mf

def test_eq():
    assert Cell(state=State.FLAG) == Cell(state=State.FLAG)
    assert Cell(state=State.MINE) == Cell(state=State.MINE)