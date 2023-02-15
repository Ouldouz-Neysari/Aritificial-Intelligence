from select import select
from symbol import dotted_as_name
import turtle
import math
import random
import copy
import time
from time import sleep
from sys import argv



class Sim:
    # Set true for graphical interface
    GUI = False
    screen = None
    selection = []
    turn = ''
    dots = []
    red = []
    blue = []
    available_moves = []
    minimax_depth = 0
    prune = False

    def __init__(self, minimax_depth, prune, gui):
        self.GUI = gui
        self.prune = prune
        self.minimax_depth = minimax_depth
        if self.GUI:
            self.setup_screen()

    def setup_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 800)
        self.screen.title("Game of SIM")
        self.screen.setworldcoordinates(-1.5, -1.5, 1.5, 1.5)
        self.screen.tracer(0, 0)
        turtle.hideturtle()

    def draw_dot(self, x, y, color):
        turtle.up()
        turtle.goto(x, y)
        turtle.color(color)
        turtle.dot(15)

    def gen_dots(self):
        r = []
        for angle in range(0, 360, 60):
            r.append((math.cos(math.radians(angle)), math.sin(math.radians(angle))))
        return r

    def initialize(self):
        self.selection = []
        self.available_moves = []
        for i in range(0, 6):
            for j in range(i, 6):
                if i != j:
                    self.available_moves.append((i, j))
        if random.randint(0, 2) == 1:
            self.turn = 'red'
        else:
            self.turn = 'blue'
        self.dots = self.gen_dots()
        self.red = []
        self.blue = []
        if self.GUI: turtle.clear()
        self.draw()

    def draw_line(self, p1, p2, color):
        turtle.up()
        turtle.pensize(3)
        turtle.goto(p1)
        turtle.down()
        turtle.color(color)
        turtle.goto(p2)

    def draw_board(self):
        for i in range(len(self.dots)):
            if i in self.selection:
                self.draw_dot(self.dots[i][0], self.dots[i][1], self.turn)
            else:
                self.draw_dot(self.dots[i][0], self.dots[i][1], 'dark gray')

    def draw(self):
        if not self.GUI: return 0
        self.draw_board()
        for i in range(len(self.red)):
            self.draw_line((math.cos(math.radians(self.red[i][0] * 60)), math.sin(math.radians(self.red[i][0] * 60))),
                           (math.cos(math.radians(self.red[i][1] * 60)), math.sin(math.radians(self.red[i][1] * 60))),
                           'red')
        for i in range(len(self.blue)):
            self.draw_line((math.cos(math.radians(self.blue[i][0] * 60)), math.sin(math.radians(self.blue[i][0] * 60))),
                           (math.cos(math.radians(self.blue[i][1] * 60)), math.sin(math.radians(self.blue[i][1] * 60))),
                           'blue')
        self.screen.update()
        sleep(1)
    
                
    def _evaluate(self):
        
        red_blue_degs=[]
        for i in range(6):
            red_blue_degs.append([0,0])
        for r_ed in self.red:
            red_blue_degs[r_ed[0]][0]+=1
            red_blue_degs[r_ed[1]][0]+=1
        for b_ed in self.blue:
            red_blue_degs[b_ed[0]][1]+=1
            red_blue_degs[b_ed[1]][1]+=1

        eva=0
        for v in red_blue_degs:
            if( v[0]>=2):
                eva-=((v[0]*(v[0]-1))/2)*2
                
            if( v[1]>=2):
                eva+=((v[1]*(v[1]-1))/2)
            
            eva+=v[0]*v[1]*3
        return eva
        #TODO

    def minimax(self,depth,player_turn,alpha,beta):

        if(depth==0):
            return None,self._evaluate()

        if(player_turn=="red"):
            best_score=-math.inf
        else :
            best_score=math.inf


        selected_move=None
        for i in range(len(self.available_moves)):
            first_move=self.available_moves.pop(i)
            if(player_turn=='red'):
                self.red.append(first_move)
                the_move, the_score=self.minimax(depth-1,'blue',alpha,beta)
                self.available_moves.insert(i,first_move)
                lst_move=self.red.pop()
                if (the_score >= best_score):
                    best_score=the_score
                    selected_move=first_move
                alpha=max(alpha,best_score)
                    
            else:
                self.blue.append(first_move)
                the_move, the_score=self.minimax(depth-1,'red',alpha,beta)
                self.available_moves.insert(i,first_move)
                lst_move=self.blue.pop()
                if (the_score <= best_score):
                    best_score=the_score
                    selected_move=first_move
                beta=min(beta,best_score)
            if (self.prune and beta<=alpha):
                break
        return selected_move,best_score

        
        
    def enemy(self):
        return random.choice(self.available_moves)

    def _swap_turn(self,trn):
        if(trn=='blue'):
            return 'red'
        else:
            return 'blue'
    def play(self):
        self.initialize()
        while True:
            
            if self.turn == 'red':
                alpha=-math.inf
                beta=math.inf
                selection = self.minimax(depth=self.minimax_depth, player_turn=self.turn,alpha=alpha,beta=beta)[0]
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            else:
                selection = self.enemy()
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])

            if selection in self.red or selection in self.blue:
                raise Exception("Duplicate Move!!!")
            if self.turn == 'red':
                self.red.append(selection)
            else:
                self.blue.append(selection)

            self.available_moves.remove(selection)
            self.turn = self._swap_turn(self.turn)
            selection = []
            self.draw()
            r = self.gameover(self.red, self.blue)
            if r != 0:
                return r

    def gameover(self, r, b):
        if len(r) < 3:
            return 0
        r.sort()
        for i in range(len(r) - 2):
            for j in range(i + 1, len(r) - 1):
                for k in range(j + 1, len(r)):
                    if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
                        return 'blue'
        if len(b) < 3: return 0
        b.sort()
        for i in range(len(b) - 2):
            for j in range(i + 1, len(b) - 1):
                for k in range(j + 1, len(b)):
                    if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
                        return 'red'
        return 0


if __name__=="__main__":

    game = Sim(minimax_depth=int(argv[1]), prune=True, gui=bool(int(argv[2])))
    start_time=time.time()
    results = {"red": 0, "blue": 0}
    for i in range(100):
        print(i)
        results[game.play()] += 1
    cur_time=time.time()  
    print(results)
    print(cur_time-start_time)
    