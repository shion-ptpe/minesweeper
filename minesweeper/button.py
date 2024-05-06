import pyxel

class Button:
    def __init__(self, _x: int, _y: int, _width: int, _height: int):
        # 引数の型が正しいか確認
        assert isinstance(_x, int)
        assert isinstance(_y, int)
        assert isinstance(_width, int)
        assert isinstance(_height, int)
        # 値を登録
        self.x: int = _x
        self.y: int = _y
        self.width: int = _width
        self.height:    int = _height

    def isInside(self, _x: int, _y: int):
        # 引数の方が正しいか確認
        assert isinstance(_x, int)
        assert isinstance(_y, int)
        # buttonの四点の位置を設定
        l:  int = self.x
        r:  int = self.x + self.width
        u:  int = self.y
        d:  int = self.y + self.height
        # 四角形内部に入っているか
        inX:    bool = (l < _x) and (_x < r)
        inY:    bool = (u < _y) and (_y < d)
        return (inX and inY)

    # 左ボタンがクリックされたなら
    def isLeftClicked(self, _x: int, _y: int):
        return pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.isInside(_x, _y)

    # 右ボタンがクリックされたなら
    def isRightClicked(self, _x: int, _y: int):
        return pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) and self.isInside(_x, _y)

