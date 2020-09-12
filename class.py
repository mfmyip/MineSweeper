# import tkinter as tk

# window = tk.Tk()

# for i in range(20):
#     for j in range(15):
#         frm = tk.Frame(
#             master=window,
#             relief=tk.RAISED,
#             borderwidth=1,
#             width=30, height=30,
#             bg="grey"
#         )
#         frm.grid(column=i, row=j)

# window.mainloop()

from random import randint

class Coordinate:
    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)

    def setCoord(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self.x == other.x and self.y == other.y
        return False
    
    def __repr__(self):
        return "<Coordinate Object, position at (%d, %d)>" % (self.x , self.y)
    def __str__(self):
        return "(%d, %d)" % (self.x , self.y)

class Board:
    def __init__(self, columns=10, rows=5):
        self.__width = columns
        self.__height = rows
        self.__grid = []
        for i in range(0, rows):
            row = []
            for j in range(0, columns):
                row.append({
                    "isHidden": True,
                    "value": 0
                })
            self.__grid.append(row)
    
    def addBomb(self, bomb):
        self.__grid[bomb.pos.y][bomb.pos.x]["value"] = bomb
        gridWidth = self.__width
        gridHeight = self.__height
        # increment the values around the bomb +1
        for row in range(bomb.pos.y - 1, bomb.pos.y + 2): # + 2 because of range goes to max - 1
            for col in range(bomb.pos.x - 1, bomb.pos.x + 2):
                # +1 if range valid or not bomb
                if ((0 <= row <= gridHeight - 1) and (0 <= col <= gridWidth - 1)):
                    if (not(isinstance(self.__grid[row][col]["value"], Bomb))): # if not bomb 
                        self.__grid[row][col]["value"] += 1
        

    def __str__(self): # overrides print()
        ret = ""
        for row in self.__grid:
            for d in row:
                if (d["isHidden"]):
                    ret += " X"
                else:
                    ret += " {}".format(d["value"] if isinstance(d["value"], int) else d["value"].__str__())
            ret += "\n"
        return ret        

class Game:
    def __init__(self, width=10, height=5):
        self.__board = Board(width, height)
        self.__score = 0
        self.__bombs = []
        # instantiate bombs, num of bombs is based on grid size, ~20% of total grid
        for i in range(0, int(width * height / 5) + 1):
            while(True):
                bomb = Bomb(x=randint(0, width-1), y=randint(0, height-1))
                if (not(bomb in self.__bombs)):
                    self.__bombs.append(bomb)
                    self.__board.addBomb(bomb)
                    break
            
    def getBombs(self):
        return self.__bombs

    def __str__(self):
        ret = self.__board.__str__()
        ret += "\nscore: {}".format(self.__score)
        return ret

class Bomb:
    def __init__(self, x=0, y=0):
        self.pos = Coordinate(x, y)
    def coord(self):
        return self.pos.__dict__

    def setPos(self, x=0, y=0):
        self.pos.setCoord(x, y)
    
    def __eq__(self, other):
        if isinstance(other, Bomb):
            return self.pos == other.pos
        return False

    def __repr__(self):
        return "<Bomb: {}>".format(self.pos.__str__())
    def __str__(self):
        return "*"

game = Game()
print(game)
        