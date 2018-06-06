import sys
import random
from tkinter import Tk, Frame, Canvas, ALL, NW

WIDTH = 600
HEIGHT = 600
DELAY = 500
MATRIX_SIZE = 15
SNAKE_TAIL = 40
GOLD_DELAY = 5000

FREE = 0
SNAKE = 1
APPLE = 2
WALL = 3
GOLD = 4
SNAKE_HEAD = 5

class Board(Canvas):

    def __init__(self, parent):
        Canvas.__init__(self, width=WIDTH, height=HEIGHT)

        self.parent = parent
        self.initGame()
        self.pack()

    def initGame(self):
        self.field = [[FREE] * MATRIX_SIZE for i in range(MATRIX_SIZE)]
        self.snake_tail_x = [[0] * SNAKE_TAIL]
        self.snake_tail_y = [[0] * SNAKE_TAIL]
        self.current_length = 0
        self.snake_x = 0
        self.snake_y = 0
        self.inGame = True
        self.last_move = 2
        self.score = 0
        self.focus_get()

        self.delay = DELAY

        self.CreateRectField()
        self.SpawnSnake()
        self.SpawnFruits(1)

        self.bind_all("<Key>", self.onKeyPressed)
        self.after(DELAY, self.onTimer)
        self.after(DELAY, self.speedUp)

    def doMove(self):
        head_prev_x = self.snake_x
        head_prev_y = self.snake_y

        if self.last_move == 0:
            self.snake_x -= 1
        elif self.last_move == 1:
            self.snake_x += 1
        elif self.last_move == 2:
            self.snake_y += 1
        elif self.last_move == 3:
            self.snake_y -= 1

        if self.field[self.snake_y][self.snake_x] == WALL:
            self.inGame = False
            return
        elif self.field[self.snake_y][self.snake_x] == SNAKE:
            self.inGame = False
            return
        elif self.field[self.snake_y][self.snake_x] == FREE:

            self.field[head_prev_y][head_prev_x] = FREE
            if self.current_length != 0:
                self.field[self.snake_tail_y[self.current_length-1]][self.snake_tail_x[self.current_length-1]] = FREE
                i = self.current_length - 1
                while i > 0:
                    self.snake_tail_x[i] = self.snake_tail_x[i-1]
                    self.snake_tail_y[i] = self.snake_tail_y[i-1]
                    i-=1
                self.snake_tail_x[0] = head_prev_x
                self.snake_tail_y[0] = head_prev_y

        elif self.field[self.snake_y][self.snake_x] == APPLE or self.field[self.snake_y][self.snake_x] == GOLD:

            self.field[head_prev_y][head_prev_x] = FREE
            i = self.current_length - 1
            self.snake_tail_x.insert(0,head_prev_x)
            self.snake_tail_y.insert(0,head_prev_y)
            self.current_length += 1
            self.SpawnFruits(1)
            self.randomEvent()

            if self.field[self.snake_y][self.snake_x] == APPLE:
                self.score += 1
            elif self.field[self.snake_y][self.snake_x] == GOLD:
                self.score += 2

        self.field[self.snake_y][self.snake_x] = SNAKE_HEAD

        for i in range(self.current_length):
            tail_x = self.snake_tail_x[i]
            tail_y = self.snake_tail_y[i]
            self.field[tail_y][tail_x] = 1

    def CreateRectField(self):
        for i in range(MATRIX_SIZE):
            self.field[0][i] = 3
            self.field[MATRIX_SIZE - 1][i] = 3
            self.field[i][0] = 3
            self.field[i][MATRIX_SIZE - 1] = 3

    def SpawnSnake(self):
        spawn_flag = False
        while spawn_flag == False:
            x = random.randint(MATRIX_SIZE/3, MATRIX_SIZE/3*2)
            y = random.randint(MATRIX_SIZE/3, MATRIX_SIZE/3*2)

            if self.field[y][x] == 3:
                continue
            else:
                self.field[y][x] = 1
                self.snake_x = x
                self.snake_y = y

                spawn_flag = True

    def SpawnFruits(self, count, golden = False):

        if golden == False:
            for i in range(count):
                spawn_flag = False
                while spawn_flag == False:
                    x = random.randint(0, MATRIX_SIZE - 1)
                    y = random.randint(0, MATRIX_SIZE - 1)
                    if self.field[y][x] == SNAKE or self.field[y][x] == WALL or self.field[y][x] == APPLE:
                        continue
                    else:
                        self.field[y][x] = APPLE
                        spawn_flag = True
        else:
            spawn_flag = False
            while spawn_flag == False:
                x = random.randint(0, MATRIX_SIZE - 1)
                y = random.randint(0, MATRIX_SIZE - 1)
                if self.field[y][x] == 1 or self.field[y][x] == 3 or self.field[y][x] == 2:
                    continue
                else:
                    self.field[y][x] = GOLD
                    spawn_flag = True

    def drawField(self):
        self.delete('square')
        y = 0
        x = 0
        cell_size = WIDTH / MATRIX_SIZE

        while y < MATRIX_SIZE:
            while x < MATRIX_SIZE:

                new_x = x * cell_size
                new_y = y * cell_size

                color = '';
                current_state = self.field[y][x]

                if (current_state == SNAKE):
                    color = 'green'
                elif (current_state == FREE):
                    color = 'white'
                elif (current_state == APPLE):
                    color = 'red'
                elif (current_state == WALL):
                   color = 'black'
                elif (current_state == GOLD):
                    color = 'yellow'
                elif (current_state == SNAKE_HEAD):
                    color = 'olive'

                self.create_rectangle(new_x,new_y,new_x+cell_size,new_y+cell_size,fill = color, tags='square')

                x += 1
            y += 1
            x = 0

    def onKeyPressed(self, e):
        key = e.keysym
        print(key)
        if key == "Left" and self.last_move != 1:
            self.last_move = 0


        if key == "Right" and self.last_move != 0:
            self.last_move = 1


        if key == "Up" and self.last_move != 2:
            self.last_move = 3


        if key == "Down" and self.last_move != 3:
            self.last_move = 2


    def randomEvent(self):
        chance = random.randint(0, 100)
        if chance < 20:
            self.SpawnFruits(1, golden = True)
            self.after(GOLD_DELAY, self.removeGold)


    def removeGold(self):
        y = 0
        x = 0

        while y < MATRIX_SIZE:
            while x < MATRIX_SIZE:

                if self.field[y][x] == GOLD:
                    self.field[y][x] = FREE
                    return
                x += 1
            y += 1
            x = 0

    def speedUp(self):
        self.delay -= 1
        self.after(DELAY, self.speedUp)

    def onTimer(self):

        if self.inGame:
            self.doMove()
            self.drawField()

            self.after(self.delay, self.onTimer)
        else:
            self.gameOver()


    def gameOver(self):

        self.delete(ALL)
        message = "Game Over. Your score is " + str(self.score)
        self.create_text(self.winfo_width()/2, self.winfo_height()/2,
            text=message, fill="black", font=('Arial',30))


class Snake(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        parent.title('Snake game')
        self.board = Board(parent)
        self.pack()

root = Tk()
nib = Snake(root)
root.mainloop()
