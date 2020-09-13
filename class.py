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
        pass

    def setCoord(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)
        pass

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self.x == other.x and self.y == other.y
        return False
    
    def __repr__(self):
        return "<Coordinate Object, position at (%d, %d)>" % (self.x , self.y)
    def __str__(self):
        return "(%d, %d)" % (self.x , self.y)

class Board:
    def __init__(self, columns=10, rows=5, hide=True):
        self.width = columns
        self.height = rows
        self.__grid = []
        for i in range(0, rows):
            row = []
            for j in range(0, columns):
                row.append({
                    "isHidden": hide,
                    "isFlagged": False,
                    "value": 0
                })
            self.__grid.append(row)
        pass
    
    def addBomb(self, bomb):
        self.__grid[bomb.pos.y][bomb.pos.x]["value"] = bomb
        gridWidth = self.width
        gridHeight = self.height
        # increment the values around the bomb +1
        for row in range(bomb.pos.y - 1, bomb.pos.y + 2): # + 2 because of range goes to max - 1
            for col in range(bomb.pos.x - 1, bomb.pos.x + 2):
                # +1 if range valid or not bomb
                if ((0 <= row <= gridHeight - 1) and (0 <= col <= gridWidth - 1)):
                    if (not(isinstance(self.__grid[row][col]["value"], Bomb))): # if not bomb 
                        self.__grid[row][col]["value"] += 1
        pass
    
    def getCell(self, x=0, y=0):
        return self.__grid[y][x]["value"]
    
    def unHideCell(self, x=0, y=0):
        self.__grid[y][x]["isHidden"] = False
        cellValue = self.__grid[y][x]["value"]

        if (cellValue == 0): # if we click on 0, propagate to other 0's and unhide everything around
            for row in range(y - 1, y + 2): # + 2 because of range goes to max - 1
                for col in range(x - 1, x + 2):
                    if ((0 <= row <= self.height - 1) and (0 <= col <= self.width - 1)):
                        tempBool = self.__grid[row][col]["isHidden"]
                        self.__grid[row][col]["isHidden"] = False

                        if (self.__grid[row][col]["value"] == 0 and tempBool):
                            self.unHideCell(col, row)
        pass

    def flagCell(self, x=0, y=0):
        tempBool = self.__grid[y][x]["isFlagged"]
        self.__grid[y][x]["isFlagged"] = not(tempBool)
        return not(tempBool)

    def countNonHiddenCells(self):
        count = 0
        for row in self.__grid:
            for cell in row:
                if not(cell["isHidden"]):
                    count += 1
        return count
        
    def __str__(self): # overrides print()
        ret = ""
        for row in self.__grid:
            for d in row:
                ret += " {}".format(d["value"] if isinstance(d["value"], int) else d["value"].__str__())
                if (d["isFlagged"]):
                    ret += "f"
                elif (d["isHidden"]):
                    ret += "h"
                else:
                    ret += " "
            ret += "\n"
        return ret

class Game:
    def __init__(self, width=10, height=5):
        self.__board = Board(width, height)
        self.__bombs = []
        # instantiate bombs, num of bombs is based on grid size, ~20% of total grid
        for i in range(0, int(width * height / 5) + 1):
            while(True):
                bomb = Bomb(x=randint(0, width-1), y=randint(0, height-1))
                if (not(bomb in self.__bombs)):
                    self.__bombs.append(bomb)
                    self.__board.addBomb(bomb)
                    break
        self.__numBombs = len(self.__bombs)
        pass
            
    def getBombs(self):
        return self.__bombs

    def select(self, x=0, y=0):
        # if bomb lose, otherise ishidden will be false
        # if bordering a 0, the other numbers (!=0) bordering 0's will be shown
        cell = self.__board.getCell(x, y)
        self.__board.unHideCell(x, y)

        if (isinstance(cell, Bomb)):
            self.__lost()
            # set all to non hidden
        if (self.__board.countNonHiddenCells() == self.__board.width * self.__board.width - len(self.__bombs)):
            self.__win()

    # flags cells
    def flag(self, x=0, y=0):
        flagged = self.__board.flagCell(x, y)
        if (flagged):
            self.__numBombs = self.__numBombs - 1
        else:
            self.__numBombs = self.__numBombs + 1
        pass

    def __lost(self):
        print("game lost :(")
        pass
    def __win(self):
        print("win! :)")
        pass

    def __str__(self):
        ret = self.__board.__str__()
        ret += "\n# bombs: {}".format(self.__numBombs)
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

game = Game(width=30, height=16)
print(game)
        