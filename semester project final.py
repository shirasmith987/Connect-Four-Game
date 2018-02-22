import Draw
import time
Draw.setCanvasSize(600,600)
Draw.setBackground(Draw.BLUE)

def whiteCircle(x,y):  # x, y is the top left corner coordinate
   Draw.setColor(Draw.WHITE)
   Draw.filledOval(x, y, 100, 100)
   
def makeBoard(): #draws a board 6 rows x 6 columns
   for yPos in range(0, 601, 100):
      for xPos in range(0,601,100):
         whiteCircle(yPos, xPos)
         

def playGame():
   global turn
   
   #initialize an empty board
   board = [[None for xPos in range(6)] for yPos in range(6)] 
   
   turn = 0
   #if turn is an even number, the computer knows it is the user's turn
   #everytime the user clicks, turn will increment by 1 
   #everytime the computer moves, turn will increment by 1
   while not endGame(board): #while no one has won the game     
      if turn % 2 == 0:
         userMove(board) 
         time.sleep(1)
      else:
         computerMove(board) 
   return # when someone has won, playGame() falls out of the while loop

#takes in the position in the 2D list that the user chose
def redCircle(yPos, xPos): 
   Draw.setColor(Draw.RED)
   #convert the single integer to an x, y cooridinate on the 600 x 600 board
   x = (xPos) * 100     
   y = (yPos) * 100   
   Draw.filledOval(x, y, 100, 100)
   Draw.show()
   
# draws a yellow circle at the specified location of the computerMove()   
def yellowCircle(yPos, xPos): 
   Draw.setColor(Draw.YELLOW)
   x = (xPos) * 100
   y = (yPos) * 100
   Draw.filledOval(x, y, 100, 100)
   
def userMove(board):
   global turn
   
   while True:
      if Draw.mousePressed():
         x = Draw.mouseX()
         y = Draw.mouseY()
      
         #converts the position which is in terms of 100 to a single digit  
         #integer that can be found in the 2D list
         xPos = x // 100 
         yPos = y // 100
         
         # check if that circle is empty
         if board[yPos][xPos] == None: 
            
            #move the position to the lowest open spot in that row
            curY = yPos 
            #while curY is not the bottom row and the space below it is empty          
            while curY < 5 and board[curY+1][xPos] == None:
               # move the position in the 2D list down a row
               curY += 1   
               
            #once the position is either the bottom or the space below it is full,
            #draw a red circle in that location
            redCircle(curY, xPos)                         
            board[curY][xPos] = "R" #update the 2D list position
            turn += 1     #the turn variable is incremented in playGame()
         return         
   
def possibleMoves1(board):
   
   #everytime this function is called, it loops through the board
   #and finds all possible moves for the computer
   
   moves = []
   for yPos in range(6):
      for xPos in range(6):
         # if the spot is empty and (it's the bottom row, 
         # or the position below it is full)
         if board[yPos][xPos] == None and \
            (yPos == 5 or board[yPos+1][xPos] != None):
            # add that position to the list as a tuple 
            moves += [[yPos, xPos]] 
            
   return moves # a list of possible moves in tuples of the yPos and xPos

def looper(board, yPos, xPos, dy, dx, color): 
   
   #takes in a single position, and returns the length of the uninterrupted run
   #of that color in a specified direction (up, down, left, right, or diagonal)
   
   #increment the position through the rows and columns in a given direction (dx, dy)
   cury, curx = yPos + dy, xPos + dx 
   ans = 0 
   # while the position is still on the board and still that color
   while cury >= 0 and cury < 6 and curx >= 0 and curx < 6\
         and board[cury][curx] == color: 
      #increment the run length by one
      ans += 1   
      #move the position on the board AGAIN in the direction indicated
      cury += dy  
      curx += dx
      
   return ans    #returns how long the run of that color is in that direction

def runSize(board, yPos, xPos, color): 
   # counts the run length backwards and forewards in a given direction, 
   #adds one for the empty position that was passed into the function, 
   #and returns the total possible run length for a move in that position
   
   horiz = looper(board, yPos, xPos, 1, 0, color) + \
      looper(board, yPos, xPos, -1, 0, color) + 1
   vert = looper(board, yPos, xPos, 0, 1, color) + \
      looper(board, yPos, xPos, 0, -1, color) + 1
   diagL = looper(board, yPos, xPos, 1, 1, color) + \
      looper(board, yPos, xPos, -1, -1, color) + 1
   diagR = looper(board, yPos, xPos, 1, -1, color) + \
      looper(board, yPos, xPos, -1, 1, color) + 1 
   
   #finds the longest run of all possible directions
   x = max( horiz, vert, diagL, diagR) 
   return x
      
def bestMove(board, possibleMoves, color):
   longest = 0
   bestY = 0 
   bestX = 0
   #loops through all the possible moves
   for move in possibleMoves:
      # separates the elements of the list into a yPos and xPos
      yPos, xPos = move 
      #passes that position into runSize() to determine its longest run length
      s = runSize(board, yPos, xPos, color) 
      
      if s > longest:    # if that length is longer than the current longest run
         longest = s     # update the longest variable to the length of s
         bestY = yPos    # update the the best y and x position
         bestX = xPos
         
   return bestY, bestX, longest   # returns the best move for that color

def computerMove(board):
   global turn
   #increment the turn variable in playGame()
   turn += 1 
   
   possibleMoves = possibleMoves1(board)
   yPos, xPos, length = bestMove(board, possibleMoves, "Y") 
   yPos2, xPos2, length2 = bestMove(board, possibleMoves, "R") 
   
   # if the length of the computer's best move is longer than the user's 
   #best run length, the computer will move there
   if length >= length2: 
      yellowCircle(yPos, xPos)
      board[yPos][xPos] = "Y"
   # if the user's best move will give the user a longer run, 
   #the computer blocks that run 
   else:            
      board[yPos2][xPos2] = "Y"     
      yellowCircle(yPos2, xPos2)      
   return

def checkWinner(board, color):
   #loops through all the positions of the board to see if someone has won
   for yPos in range(6):
         for xPos in range(6):  
            #looper is only called if the position is filled with the color 
            #passed into the function
            if board[yPos][xPos] == color: 
               # finds the uninterrupted run length of that color in each direction
               # the 1 is added because looper only counts the spots dx or dy  
               # away from the position passed into the function
               horiz = looper(board, yPos, xPos, 1, 0, color) + 1 
               vert = looper(board, yPos, xPos, 0, 1, color) + 1
               diagL = looper(board, yPos, xPos, 1, 1, color) + 1
               diagR = looper(board, yPos, xPos, 1, -1, color) + 1 
               
               #if any run length is 4, that color has won
               if horiz == 4 or vert == 4 or diagL == 4 or diagR == 4: 
                  return True
   else:
      return False

def fullBoard(board):
   #returns true if there are no more empty spots on the board
   for yPos in range(6):
      for xPos in range(6):
         if board[yPos][xPos] == None:
            return False
   return True
   
def endGame(board):
   
   Draw.setColor(Draw.DARK_GREEN)
   Draw.setFontFamily('Courier')
   Draw.setFontSize(70)
   Draw.setFontBold(True)  
   
   #if someone has won or the board is full, it will return true
   if fullBoard(board):
      return True
   
   # if the user has a run of 4
   if checkWinner(board,"R"): 
      Draw.string("You \nWon!", 200,200) # displays on the board
      Draw.show()
      
      # endGame() returns True, playGame() falls out of the loop, and the game ends
      return True 
   
   # if the computer has a run of 4
   elif checkWinner(board,"Y"): 
      Draw.string(" Sorry,\nyou lost!", 50,200) 
      Draw.show()
      return True
   
   # if no one has won, endGame() returns false and the game continues
   return False 

def main():
   makeBoard()
   playGame()
main()
Draw.show