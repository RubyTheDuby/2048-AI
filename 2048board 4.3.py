from collections import namedtuple
from random import choice
from monte_carlo_tree_search import MCTS, Node
import random
import tkinter as tk
import copy

_TTTB = namedtuple("Board2048", "tup turn winner terminal")
queue=None
NUM=0
big_tile=0

class Board2048(_TTTB, Node):
   
    def to_pretty_string(board):
        string = ""
        for row in range(4):
            for col in range(4):
                element = board.tup[4 * row + col]
                string += " " + str(element)
                if col < 3:
                    string += " |"
            string += "\n"
            if row < 3:
                string += "------------\n"
        return string




    def find_children(board):#computationally inefficient check something with terminal
      if board.terminal:
          return set()
      children = set()
      
      if board.tup!=_Upward(board.tup):
          up = _Upward(board.tup)
          children.add(Board2048(up, not board.turn, None, _find_loser(up)))
      if board.tup!=_Downward(board.tup):
          down = _Downward(board.tup)
          children.add(Board2048(down, not board.turn, None,  _find_loser(down)))
          
      if board.tup!=_Left(board.tup):
          left = _Left(board.tup)
          children.add(Board2048(left, not board.turn, None,  _find_loser(left)))
          
      if board.tup!=_Right(board.tup):
          right = _Right(board.tup)
          children.add(Board2048(right, not board.turn, None,  _find_loser(right)))
     

     
      return children






    def find_random_child(board):
        global queue
        global NUM
        if board.terminal:
            print("None")
            return None
        directions = ['up', 'down', 'left', 'right']
        tup = board.tup
        if not _find_loser(tup):
            directions = ['up', 'down', 'left', 'right']
            new_tup = board.tup
            best_tup = tup
            best_score = float("-inf")
            for direction in directions:
                if direction == 'up':
                    new_tup = _Upward(tup)
                elif direction == 'down':
                    new_tup = _Downward(tup)
                elif direction == 'left':
                    new_tup = _Left(tup)
                else:
                    new_tup = _Right(tup)
                score = calculate_score(new_tup)+calculate_snake_score(new_tup)
                if new_tup[15] == max(new_tup):
                    score += 1000 
                if score > best_score:
                    best_score = score
                    best_tup = new_tup
            best_tup = random1(best_tup,queue[NUM])
            NUM += 1
            turn = not board.turn
            winner = _find_winner(best_tup)
            is_terminal = _find_loser(best_tup)
            board = Board2048(best_tup, turn, winner, _find_loser(best_tup))
            return board







    def reward(board):
      global big_tile
      score=0
      maxnum=max(board.tup)
      maxrem=0
      num_zero_score=0
      num_zeros = board.tup.count(0)
      adjacent_values=[]
      if board.tup[15]==maxnum or board.tup[0]==maxnum or board.tup[3]==maxnum or board.tup[12]==maxnum:
        score+=0.30
      if num_zeros>=8:
          score+=0.20
      elif num_zeros>=6:
          score+=0.15
      elif num_zeros>=4:
           score+=0.10
      elif num_zeros>=3:
          score+=0.05
      elif num_zeros>=2:
           score+=0.025
      elif num_zeros>=1:
           score+=0.001
        

      answer=1-(0)
      rounded_result = round(answer, 50)
      return (score)
      raise RuntimeError(f"board has unknown winner type {board.winner}")

       

    ########################################################################################################
    #GAME MOVE
    ########################################################################################################



    def is_terminal(board):
        return board.terminal



    def _make_move(board,tup):
            tup=tup
            turn = not board.turn
            winner = _find_winner(tup)
            is_terminal = _find_loser(tup)
            return Board2048(tup, turn, winner, is_terminal)
         







    ################################################################################################



def random1(tup,queue):
    tup = list(tup)
    #if tup[queue[1]] ==0:
        #tup[queue[1]] = queue[0]
        #tup = tuple(tup)
        #return tup

    empty_positions = [i for i, val in enumerate(tup) if val == 0]
    if empty_positions:
        position = random.choice(empty_positions)
        tup[position] = random.choice([2, 4])  
    tup = tuple(tup)
    return tup







def _Right(tup):

        tup = list(tup)
        for x in range(0, 13, 4):
            for i in range(1, 4, 1):
                for l in range(x, x + i, 1):
                    if tup[l] == 0 and tup[x + i] != 0:
                        tup[l] = tup[x + i]
                        tup[x + i] = 0
                        break
            if tup[x + 1] == tup[x] and tup[x + 2] == tup[x + 3]:
                y = tup[x]
                e = tup[x + 2]
                tup[x] = y * 2
                tup[x + 1] = e * 2
                tup[x + 2] = 0
                tup[x + 3] = 0
            elif tup[x + 1] == tup[x]:
                y = tup[x]
                tup[x] = y * 2
                tup[x + 1] = tup[x + 2]
                tup[x + 2] = tup[x + 3]
                tup[x + 3] = 0
            elif tup[x + 1] == tup[x + 2]:
                y = tup[x + 1]
                tup[x + 1] = y * 2
                tup[x + 2] = tup[x + 3]
                tup[x + 3] = 0
            elif tup[x + 3] == tup[x + 2]:
                y = tup[x + 2]
                tup[x + 2] = y * 2
                tup[x + 3] = 0

        tup = tuple(tup)
       
        return tup






def _Left(tup):
        tup = list(tup)

        for x in range(3, 16, 4):
            for i in range(1, 4, 1):
                for l in range(x, x - i, -1):
                    if tup[l] == 0 and tup[x - i] != 0:
                        tup[l] = tup[x - i]
                        tup[x - i] = 0
                        break
            if tup[x - 1] == tup[x] and tup[x - 2] == tup[x - 3]:
                y = tup[x]
                e = tup[x - 2]
                tup[x] = y * 2
                tup[x - 1] = e * 2
                tup[x - 2] = 0
                tup[x - 3] = 0
            elif tup[x - 1] == tup[x]:
                y = tup[x]
                tup[x] = y * 2
                tup[x - 1] = tup[x - 2]
                tup[x - 2] = tup[x - 3]
                tup[x - 3] = 0
            elif tup[x - 1] == tup[x - 2]:
                y = tup[x - 1]
                tup[x - 1] = y * 2
                tup[x - 2] = tup[x - 3]
                tup[x - 3] = 0
            elif tup[x - 3] == tup[x - 2]:
                y = tup[x - 2]
                tup[x - 2] = y * 2
                tup[x - 3] = 0

        tup = tuple(tup)

        return tup






def _Upward(tup):
        tup = list(tup)

        for x in range(0, 4, 1):
            for i in range(4, 13, 4):
                for l in range(x, x + i, 4):
                    if tup[l] == 0 and tup[x + i] != 0:
                        tup[l] = tup[x + i]
                        tup[x + i] = 0
                        break
            if tup[x + 4] == tup[x] and tup[x + 8] == tup[x + 12]:
                y = tup[x]
                e = tup[x + 8]
                tup[x] = y * 2
                tup[x + 4] = e * 2
                tup[x + 8] = 0
                tup[x + 12] = 0
            elif tup[x + 4] == tup[x]:
                y = tup[x]
                tup[x] = y * 2
                tup[x + 4] = tup[x + 8]
                tup[x + 8] = tup[x + 12]
                tup[x + 12] = 0
            elif tup[x + 4] == tup[x + 8]:
                y = tup[x + 4]
                tup[x + 4] = y * 2
                tup[x + 8] = tup[x + 12]
                tup[x + 12] = 0
            elif tup[x + 12] == tup[x + 8]:
                y = tup[x + 8]
                tup[x + 8] = y * 2
                tup[x + 12] = 0

        tup = tuple(tup)
       
        return tup












def _Downward(tup):
       
        tup = list(tup)


        for x in range(12, 16, 1):
            for i in range(4, 13, 4):
                for l in range(x, x - i, -4):
                    if tup[l] == 0 and tup[x - i] != 0:
                        tup[l] = tup[x - i]
                        tup[x - i] = 0
                        break
            if tup[x - 4] == tup[x] and tup[x - 8] == tup[x - 12]:
                y = tup[x]
                e = tup[x - 8]
                tup[x] = y * 2
                tup[x - 4] = e * 2
                tup[x - 8] = 0
                tup[x - 12] = 0
            elif tup[x - 4] == tup[x]:
                y = tup[x]
                tup[x] = y * 2
                tup[x - 4] = tup[x - 8]
                tup[x - 8] = tup[x - 12]
                tup[x - 12] = 0
            elif tup[x - 4] == tup[x - 8]:
                y = tup[x - 4]
                tup[x - 4] = y * 2
                tup[x - 8] = tup[x - 12]
                tup[x - 12] = 0
            elif tup[x - 12] == tup[x - 8]:
                y = tup[x - 8]
                tup[x - 8] = y * 2
                tup[x - 12] = 0

        tup = tuple(tup)
       
        return tup


def _find_winner(tup):
    for x in tup:
        if x == 2048:
            print("yeah")
            return True

        else:
            return None





def _find_loser(tup):
    

    up = _Upward(tup)
    down = _Downward(tup)
    left = _Left(tup)
    right = _Right(tup)
    

    if tup==up and tup==down and tup==left and tup==right and 0 not in tup:
        return True

    else:
        return False


def calculate_snake_score(tup):
    score = 0
    for i in range(4):
        for j in range(4):
            index = i * 4 + j
            if i % 2 == 0:
                index = (i * 4) + (3 - j)
            score += tup[index]
    return score


def calculate_score(tup):
    max_tile_value = max(tup)
    monotonicity_score = calculate_monotonicity(tup)
    return max_tile_value + monotonicity_score


def calculate_monotonicity(tup):
    row_monotonicity = sum(abs(tup[i] - tup[i + 1]) for i in range(len(tup) - 1))
    col_monotonicity = sum(abs(tup[i] - tup[i + 4]) for i in range(12))
    return max(row_monotonicity, col_monotonicity)




def generate():
    queue = []
    while len(queue) != 4000:#4096
        random_positions = random.randint(0, 9)

        if random_positions <= 8:
            x = 2
        else:
            x = 4
        random_positions = random.randint(0, 15)
        queue.append([x, random_positions])
    return queue






def play_game():
    global queue
    global NUM
    global big_tile
    num=0
    tree = MCTS()
    board = new_2048_board()
    root = tk.Tk()
    root.title("2048Board")

    display_board(root, board)  # Display the initial game board

    queue=generate()
    while True:
        if board.terminal:
            break
        for _ in range(9):  # 7
            NUM = num
            tree.do_rollout(board)
        board = tree.choose(board)
        display_board(root, board)  # Update the displayed board
        root.after(10)  # Wait 1 second (1000 milliseconds)

        tup = random1(board.tup, queue[num])
        board = board._make_move(tup)

        print(board.terminal)
        big_tile = max(board.tup)
        print(big_tile)
        num += 1
        print(board.to_pretty_string())
        if board.terminal:
            break

    root.destroy()





def display_board(root, board):
    # Clear the existing content in the GUI window
    for widget in root.winfo_children():
        widget.destroy()

    # Display the game board
    for i, cell in enumerate(board.tup):
        row, col = divmod(i, 4)
        if cell is None:
            cell_text = ""
        else:
            cell_text = str(cell)
        tk.Label(root, text=cell_text, width=6, height=3, font=("Helvetica", 24)).grid(row=row, column=col)

    # Update the GUI window
    root.update()




def new_2048_board():
  tup = (0,) * 16  
   
  random_positions = random.sample(range(16), 2)

  temp = list(tup)
  for position in random_positions:
    temp[position] = 2
  tup = tuple(temp)

  return Board2048(tup=tup, turn=True, winner=None, terminal=False)

if __name__ == "__main__":
    play_game()
