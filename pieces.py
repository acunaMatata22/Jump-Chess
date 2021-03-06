# Contains all piece classes for chess 3D
from constant import *
from utils import *

board = [[([None] * 8) for row in range(8)] for i in range(2)]
check = False
# the board keeps track of the locations of all the pieces
class Piece(object):
    def __init__(self, color, modelPath, pos, node, scale=1, rotation=0):
        # number is so different pieces arent equivalent and can be selected
        # individually
        self.model = loader.loadModel(modelPath)
        self.model.reparentTo(node)
        self.model.setColor(color)
        self.model.setPos(squarePos(pos))
        if rotation != 0:
            self.model.setHpr(rotation, 0, 0)
        if scale != 1:
            self.model.setScale(scale)
        self.position = pos
        self.color = None
    def move(self, newCoor, chessObj, promotion=False):
        self.take = False
        self.takenPiece = None
        # just moves the model to a new spot
        if self.testCollision(newCoor) or promotion: # sees if collides with friendly piece
            print("no collision")
            oldPos = self.position
            origCoor = indexToTuple(self.position)
            origPiece = board[origCoor[0]][origCoor[1]][origCoor[2]]
            if not self.checkTests(newCoor, chessObj):
                print("legal")
                print("new Coor:", newCoor, "old Coor:", origCoor)
                # a tuple containing the pieces original location
                # sets old spot on board to None and new to the piece
                newPos = tupleToIndex(newCoor)
                self.model.setPos(squarePos(newPos))
                if self.isCheck(newCoor, chessObj):
                    print("CHECK")
                    check = True
                    if self.isCheckMate(newCoor, chessObj, origCoor):
                        return "gameOver"
                return "success"
            else:
                print("puts king in check")
                # must undo move
                self.position = oldPos
                if self.take:
                    self.unTake(self.takenPiece, chessObj)
                board[origCoor[0]][origCoor[1]][origCoor[2]] = self
                board[newCoor[0]][newCoor[1]][newCoor[2]] = origPiece
                return "collision"
        else:
            return "collision"
    def checkTests(self, newCoor, chessObj):
        # makes sure move wont put self in check
        newPos = tupleToIndex(newCoor)
        origCoor = indexToTuple(self.position)
        board[origCoor[0]][origCoor[1]][origCoor[2]] = None
        board[newCoor[0]][newCoor[1]][newCoor[2]] = self
        self.position = newPos
        for Possibleking in chessObj.king:
            if Possibleking.color == self.color:
                king = Possibleking
                kingCoor = indexToTuple(king.position)
            else:
                secondKing = Possibleking
        for pawn in chessObj.pawn:
            if pawn.color != king.color:
                moves = pawn.getSquares(indexToTuple(pawn.position))
                for move in moves:
                    if move == kingCoor:
                        return True
        for knight in chessObj.knight:
            if knight.color != king.color:
                moves = knight.getSquares(indexToTuple(knight.position))
                for move in moves:
                    if move == kingCoor:
                        return True
        for rook in chessObj.rook:
            if rook.color != king.color:
                moves = rook.getSquares(indexToTuple(rook.position))
                for move in moves:
                    if move == kingCoor:
                        return True
        for bishop in chessObj.bishop:
            if bishop.color != king.color:
                moves = bishop.getSquares(indexToTuple(bishop.position))
                for move in moves:
                    if move == kingCoor:
                        return True
        for queen in chessObj.queen:
            if queen.color != king.color:
                moves = queen.getSquares(indexToTuple(queen.position))
                for move in moves:
                    if move == kingCoor:
                        return True
        for secondKing in chessObj.king:
            if secondKing != king:
                moves = king.getSquares(indexToTuple(king.position))
                for move in moves:
                    if move == kingCoor:
                        return True
        for newPiece in chessObj.newPieces:
            if newPiece.color != king.color:
                moves = newPiece.getSquares(indexToTuple(newPiece.position))
                for move in moves:
                    if move == kingCoor:
                        return True
        return False
    def isCheck(self, newCoor, chessObj, color=None):
        # checks if the new move will put opponent in check
        if color == None:
            color = self.color
        for Possibleking in chessObj.king:
            if Possibleking.color != color:
                king = Possibleking
                kingCoor = indexToTuple(king.position)
            else:
                secondKing = Possibleking
        for pawn in chessObj.pawn:
            if pawn.color != king.color:
                moves = pawn.getSquares(indexToTuple(pawn.position))
                for move in moves:
                    if move == kingCoor:
                        return True
        for knight in chessObj.knight:
            if knight.color != king.color:
                moves = knight.getSquares(indexToTuple(knight.position))
                for move in moves:
                    if move == kingCoor:
                        return True
        for rook in chessObj.rook:
            if rook.color != king.color:
                moves = rook.getSquares(indexToTuple(rook.position))
                for move in moves:
                    if move == kingCoor:
                        return True
        for bishop in chessObj.bishop:
            if bishop.color != king.color:
                moves = bishop.getSquares(indexToTuple(bishop.position))
                for move in moves:
                    if move == kingCoor:
                        return True
        for queen in chessObj.queen:
            if queen.color != king.color:
                moves = queen.getSquares(indexToTuple(queen.position))
                for move in moves:
                    if move == kingCoor:
                        return True
        for newPiece in chessObj.newPieces:
            if newPiece.color != king.color:
                moves = newPiece.getSquares(indexToTuple(newPiece.position))
                for move in moves:
                    if move == kingCoor:
                        return True
        return False
    def isCheckMate(self, newCoor, chessObj, origCoor):
        for potentKing in chessObj.king:
            if potentKing.color != self.color:
                king = potentKing
        for kingMove in king.getSquares(indexToTuple(king.position)):
            if self.testCollision(newCoor, king):
                newPos = tupleToIndex(newCoor)
                board[origCoor[0]][origCoor[1]][origCoor[2]] = None
                board[newCoor[0]][newCoor[1]][newCoor[2]] = king
                if not checkTests(self, newCoor, chessObj):
                    return False
                else: return True
    def testCollision(self, curCoor, piece=None):
        # tests if a piece can move somewhere
        squareVal = board[curCoor[0]][curCoor[1]][curCoor[2]]
        # the object currently located at the board location
        if piece == None:
            piece = self
        print("squareVal:", squareVal)
        if squareVal == None:
            print("empty space")
            return True
        else:
            if squareVal == piece:
                print("itself")
                return False
            elif squareVal.color == piece.color:
                print("same color:", piece.color)
                return False
            else:
                piece.takePiece(squareVal)
                print("different color")
                self.take = True
                self.takenPiece = squareVal
                return True
    def takePiece(self, piece):
        # add piece to list of taken pieces and removes from board
        piece.model.removeNode() # call detachNode() to not draw but not delete
        print("piece taken")
    def unTake(self, piece, chessObj):
        chessObj.newPieces.append(piece)
    def getSquares(self, curCoor):
        moves = self.getMoves(curCoor)
        # z, y, x = curCoor[0], curCoor[1], curCoor[2]
        for move in moves:
            if move[0] == 1 and (type(board[0][move[1]][move[2]]) == King or \
                    type(board[0][move[1]][move[2]]) == Queen):
                moves.remove(move)
        return moves
    def gridMoves(self, z, y, x):
        # returrns the files and ranks that can be travelled by rooks and queens
        moves = []
        for i in range(1, 8 - x): # generates moves to the right
            if z == 1:
                if (type(board[0][y][x + i]) == King or \
                        type(board[0][y][x + i]) == Queen):
                    break
            if board[z][y][x + i] == None:
                moves.append([z, y, x + i])
            elif board[z][y][x + i].color != self.color:
                moves.append([z, y, x + i]) # can attack can't jump over
                break
            else:
                break # can't move there and can't jump over piece
        for i in range(1, x + 1): # moves to the left
            if z == 1:
                if (type(board[0][y][x - i]) == King or \
                        type(board[0][y][x - i]) == Queen):
                    break
            if board[z][y][x - i] == None:
                moves.append([z, y, x - i])
            elif board[z][y][x - i].color != self.color:
                moves.append([z, y, x -i])
                break
            else:
                break
        for i in range(1, 8 - y): # moves above
            if z == 1:
                if (type(board[0][y + i][x]) == King or \
                        type(board[0][y + i][x]) == Queen):
                    break
            if board[z][y + i][x] == None:
                moves.append([z, y + i, x])
            elif board[z][y + i][x].color != self.color:
                moves.append([z, y + i, x])
                break
            else:
                break
        for i in range(1, y + 1): # moves below
            if z == 1:
                if (type(board[0][y - i][x]) == King or \
                        type(board[0][y - i][x]) == Queen):
                    break
            if board[z][y - i][x] == None:
                moves.append([z, y - i, x])
            elif board[z][y - i][x].color != self.color:
                moves.append([z, y - i, x])
                break
            else:
                break
        return moves
    def diagonalMoves(self, z, y, x):
        # returns the diagonals for the movesets of bishops and queens
        moves = []
        mRight = 8 - x # includes all but last move
        mUp = 8 - y
        mLeft = x + 1
        mDown = y + 1
        for i in range(1, min(mRight, mUp)):
            if z == 1:
                if (type(board[0][y + i][x + i]) == King or \
                        type(board[0][y + i][x + i]) == Queen):
                    break
            if board[z][y + i][x + i] == None:
                moves.append([z, y + i, x + i])
            elif board[z][y + i][x + i].color != self.color:
                moves.append([z, y + i, x + i])
                break
            else:
                break
        for i in range(1, min(mUp, mLeft)):
            if z == 1:
                if (type(board[0][y + i][x - i]) == King or \
                        type(board[0][y + i][x - i]) == Queen):
                    break
            if board[z][y + i][x - i] == None:
                moves.append([z, y + i, x - i])
            elif board[z][y + i][x - i].color != self.color:
                moves.append([z, y + i, x - i])
                break
            else:
                break
        for i in range(1, min(mLeft, mDown)):
            if z == 1:
                if (type(board[0][y - i][x - i]) == King or \
                        type(board[0][y - i][x - i]) == Queen):
                    break
            if board[z][y - i][x - i] == None:
                moves.append([z, y - i, x - i])
            elif board[z][y - i][x - i].color != self.color:
                moves.append([z, y - i, x - i])
                break
            else:
                break
        for i in range(1, min(mDown, mRight)):
            if z == 1:
                if (type(board[0][y - i][x + i]) == King or \
                        type(board[0][y - i][x + i]) == Queen):
                    break
            if board[z][y - i][x + i] == None:
                moves.append([z, y - i, x + i])
            elif board[z][y - i][x + i].color != self.color:
                moves.append([z, y - i, x + i])
                break
            else:
                break
        return moves
class Pawn(Piece):
    def __init__(self, number, color, node):
        if color == "black":
            col = BLACKP
            pos = number + 48
            board[0][6][number] = self
        else:
            col = WHITEP
            pos = number + 8
            board[0][1][number] = self
        super(Pawn, self).__init__(col, "models/pawn", pos, node)
        self.color = color
        self.specialMove = True
    def __repr__(self):
        return "Pawn"
    def getSquares(self, curCoor):
        return super(Pawn, self).getSquares(curCoor)
    def getMoves(self, curCoor):
        # returns a list of all legal moves possible
        # pawn can jump between boards in addition to traditional moveset
        z, y, x = curCoor[0], curCoor[1], curCoor[2]
        moves = []
        moves.append([(z + 1) % 2, y, x]) # board jump
        if self.color == "white":
            if y + 1 < 8 and board[z][y + 1][x] == None: # forward move
                moves.append([z, y + 1, x])
            # diagonal attacks
            if x + 1 < 8 and y + 1 < 8 and board[z][y + 1][x + 1] != None and \
                            board[z][y + 1][x + 1].color != self.color:
                moves.append([z, y + 1, x + 1])
            if x - 1 >= 0 and y + 1 < 8 and board[z][y + 1][x - 1] != None and \
                            board[z][y + 1][x - 1].color != self.color:
                moves.append([z, y + 1, x - 1])
            # now to implement starting special move
            if self.specialMove and board[z][y + 1][z] == None and \
                    board[z][y + 2][x] == None:
                moves.append([z, y + 2, x])
        else:
            if y - 1 >= 0 and board[z][y - 1][x] == None: # forward move
                moves.append([z, y - 1, x])

            if x + 1 < 8 and y - 1 >= 0 and board[z][y - 1][x + 1] != None and \
                            board[z][y - 1][x + 1].color != self.color:
                moves.append([z, y - 1, x + 1])
            if x - 1 >= 0 and y - 1 >= 0 and board[z][y - 1][x - 1] != None and \
                            board[z][y - 1][x - 1].color != self.color:
                moves.append([z, y - 1, x - 1])

            if self.specialMove and board[z][y - 1][x] == None and \
                    board[z][y - 2][x] == None:
                moves.append([z, y - 2, x])
        return moves
    def move(self, newCoor, chessObj):
        self.specialMove = False
        returnVal = "success"
        if super(Pawn, self).move(newCoor, chessObj):
            if (self.color == "black" and newCoor[1] == 0) or \
                    (self.color == "white" and newCoor[1] == 7):
                returnVal = "promotion"
            return returnVal
class Rook(Piece):
    def __init__(self, number, color, node, implicit=True):
        if color == "black":
            col = BLACKP
            if implicit: # implied that its just being called to set up the board
                pos = number * 7 + 56
                board[0][7][number * 7] = self
            else:
                pos = number
                coor = indexToTuple(pos)
                board[coor[0]][coor[1]][coor[2]] = self
        else:
            col = WHITEP
            if implicit:
                pos = number * 7
                board[0][0][number * 7] = self
            else:
                pos = number
                coor = indexToTuple(pos)
                board[coor[0]][coor[1]][coor[2]] = self
        super(Rook, self).__init__(col, "models/rook", pos, node)
        self.color = color
    def __repr__(self):
        return "Rook"
    def getSquares(self, curCoor):
        return super(Rook, self).getSquares(curCoor)
    def getMoves(self, curCoor):
        # returns a list of all legal moves possible
        # rook can move along ranks, files, and to upper board
        z, y, x = curCoor[0], curCoor[1], curCoor[2]
        moves = self.gridMoves(z, y, x)
        moves.append([(z + 1) % 2, y, x]) # moves vertically        
        return moves
class Knight(Piece):
    def __init__(self, number, color, node, implicit=True):
        if color == "black":
            col = BLACKP
            if implicit:
                pos = number * 5 + 57
                board[0][7][number * 5 + 1] = self
            else:
                pos = number
                coor = indexToTuple(pos)
                board[coor[0]][coor[1]][coor[2]] = self
            rotation = 180
        else:
            col = WHITEP
            if implicit:
                pos = number * 5 + 1
                board[0][0][number * 5 + 1] = self
            else:
                pos = number
                coor = indexToTuple(pos)
                board[coor[0]][coor[1]][coor[2]] = self
            rotation = 0
        super(Knight, self).__init__(col, "models/knight", pos, node,
                                                        rotation=rotation)
        self.color = color
    def __repr__(self):
        return "Knight"
    def getSquares(self, curCoor):
        moves = super(Knight, self).getSquares(curCoor)
        result = []
        for move in moves:
            if not (board[move[0]][move[1]][move[2]] != None and \
                    board[move[0]][move[1]][move[2]].color == self.color):
                result.append(move)
        return result
    def getMoves(self, curCoor):
        # knight can move in an 'L' shape in 3D now, as long as path is still
        # preserved
        z, y, x = curCoor[0], curCoor[1], curCoor[2]
        moves = []
        if z == 1:
            moves.append([0, y, x])
        if y + 2 < 8: # no other clean way but if statements unfortunately
            if x + 1 < 8:
                moves.append([z, y + 2, x + 1])
            if x - 1 >= 0:
                moves.append([z, y + 2, x - 1])
            if z == 0:
                moves.append([1, y + 2, x])
        if y - 2 >= 0:
            if x + 1 < 8:
                moves.append([z, y - 2, x + 1])
            if x - 1 >= 0:
                moves.append([z, y - 2, x - 1])
            if z == 0:
                moves.append([1, y - 2, x])
        if x + 2 < 8:
            if y + 1 < 8:
                moves.append([z, y + 1, x + 2])
            if y - 1 >= 0:
                moves.append([z, y - 1, x + 2])
            if z == 0:
                moves.append([1, y, x + 2])
        if x - 2 >= 0:
            if y + 1 < 8:
                moves.append([z, y + 1, x - 2])
            if y - 1 >= 0:
                moves.append([z, y - 1, x - 2])
            if z == 0:
                moves.append([1, y, x - 2])
        return moves
class Bishop(Piece):
    def __init__(self, number, color, node, implicit=True):
        if color == "black":
            col = BLACKP
            if implicit:
                pos = number * 3 + 58
                board[0][7][number * 3 + 2] = self
            else:
                pos = number
                coor = indexToTuple(pos)
                board[coor[0]][coor[1]][coor[2]] = self
            rotation = 180
        else:
            col = WHITEP
            if implicit:
                pos = number * 3 + 2
                board[0][0][number * 3 + 2] = self
            else:
                pos = number
                coor = indexToTuple(pos)
                board[coor[0]][coor[1]][coor[2]] = self
            rotation = 0
        super(Bishop, self).__init__(col, "models/bishop", pos, node,
                                                        rotation = rotation)
        self.color = color
    def __repr__(self):
        return "Bishop"
    def getSquares(self, curCoor):
        return super(Bishop, self).getSquares(curCoor)
    def getMoves(self, curCoor):
        # bishops can jump boards in addition to their traditional moveset
        z, y, x = curCoor[0], curCoor[1], curCoor[2]
        moves = self.diagonalMoves(z, y, x)
        moves.append([(z + 1) % 2, y, x])
        return moves
class Queen(Piece):
    def __init__(self, number, color, node, scale=1, implicit=True):
        if color == "black":
            col = BLACKP
            if implicit:
                pos = 59
                board[0][7][3] = self
            else:
                pos = number
                coor = indexToTuple(pos)
                board[0][coor[1]][coor[2]] = self
        else:
            col = WHITEP
            if implicit:
                pos = 3
                board[0][0][3] = self
            else:
                pos = number
                coor = indexToTuple(pos)
                board[coor[0]][coor[1]][coor[2]] = self
        super(Queen, self).__init__(col, "models/queen", pos, node, scale)
        self.color = color
    def __repr__(self):
        return "Queen"
    def getSquares(self, curCoor):
        moves = super(Queen, self).getSquares(curCoor)
        return moves
    def getMoves(self, curCoor):
        z, y, x = curCoor[0], curCoor[1], curCoor[2]
        moves = self.gridMoves(z, y, x)
        moves += self.diagonalMoves(z, y, x)
        return moves

class King(Piece):
    def __init__(self, color, node, scale=1):
        rotation = 90
        if color == "black":
            col = BLACKP
            pos = 60
            board[0][7][4] = self
        else:
            col = WHITEP
            pos = 4
            board[0][0][4] = self
        super(King, self).__init__(col, "models/king", pos, node, scale,
                                                        rotation = rotation)
        self.color = color
    def __repr__(self):
        return "King"
    def getSquares(self, curCoor):
        moves = super(King, self).getSquares(curCoor)
        result = []
        for move in moves:
            if not (board[move[0]][move[1]][move[2]] != None and \
                    board[move[0]][move[1]][move[2]].color == self.color):
                result.append(move)
        return result
    def getMoves(self, curCoor):
        # can move one square in any direction but up
        z, y, x = curCoor[0], curCoor[1], curCoor[2]
        moves = []
        if x + 1 < 8: # moves to the right
            moves.append([z, y, x + 1])
            if y + 1 < 8:
                moves.append([z, y + 1, x + 1])
            if y - 1 >= 0:
                moves.append([z, y - 1, x + 1])
        if x - 1 >= 0: # to the left
            moves.append([z, y, x - 1])
            if y + 1 < 8:
                moves.append([z, y + 1, x - 1])
            if y - 1 >= 0:
                moves.append([z, y - 1, x - 1])
        if y + 1 < 8: # forward and back
            moves.append([z, y + 1, x])
        if y - 1 >= 0:
            moves.append([z, y - 1, x])
        return moves