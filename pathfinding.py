import numpy as np
import pygame
from settings import Settings

class board():
    def __init__(self):
        self.settings = Settings()

        pygame.init()
        self.screen = pygame.display.set_mode(self.settings.size)
        self.board = np.zeros([self.settings.row, self.settings.col])

        self.aStar = []
        self.step = 0
        self.finish = None
        self.start = None
        self.path = []

    def change_board(self, row, col):
        if self.board[row][col] == 0:
            self.board[row][col] = 1
        elif self.board[row][col] == 1:
            self.board[row][col] = 0

    def draw(self):
        self.screen.fill(self.settings.bgcolor)
        l = self.settings.size[0]/len(self.board)
        d = self.settings.size[1]/len(self.board[0])
        for i in self.aStar:
            pygame.draw.rect(self.screen, self.settings.acolor, (l*i[0], d*i[1], l, d))
        for i in self.path:
            if i != None:
                pygame.draw.rect(self.screen, self.settings.pcolor, (l*i[0], d*i[1], l, d))
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    pygame.draw.rect(self.screen, self.settings.wcolor, (l*j, d*i, l,d))
        if self.start:
            pygame.draw.rect(self.screen, self.settings.scolor, (l*self.start[0], d*self.start[1], l, d))
        if self.finish:
            pygame.draw.rect(self.screen, self.settings.fcolor, (l*self.finish[0], d*self.finish[1], l, d))
        pygame.display.update()

    def in_list(self, x, y):
        if x>=0 and y>=0 and x<self.settings.row and y<self.settings.col:
            good = True
            if self.board[y][x] == 1:
                good = False
            for j in self.aStar:
                if j[0]==x and j[1]==y:
                    good = False
            if good:
                self.aStar.append([x,y,self.step+1])
    
    def pathFind(self):
        tmp = self.step
        lista = [self.finish]
        for i in range(tmp):
            t = tmp-i
            for j in self.aStar:
                if t == j[2]:
                    if j[0]==lista[-1][0]+1 and j[1]==lista[-1][1]:
                        lista.append(j)
                        break
                    elif j[0]==lista[-1][0]-1 and j[1]==lista[-1][1]:
                        lista.append(j)
                        break
                    elif j[0]==lista[-1][0] and j[1]==lista[-1][1]+1:
                        lista.append(j)
                        break
                    elif j[0]==lista[-1][0] and j[1]==lista[-1][1]-1:
                        lista.append(j)
                        break
        self.path = lista

    def aStarFind(self):
        if len(self.aStar) == 0:
            self.aStar.append(self.start+[0])
        else:
            for i in self.aStar:
                if i[2] == self.step:
                    self.in_list(i[0]+1, i[1])
                    self.in_list(i[0]-1, i[1])
                    self.in_list(i[0], i[1]+1)
                    self.in_list(i[0], i[1]-1)
            self.step+=1
        for i in self.aStar:
            if i[0] == self.finish[0] and i[1] == self.finish[1]:
                self.finding = False
                self.pathFind()

    def controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    pos = pygame.mouse.get_pos()
                    xy = [int(pos[0]/self.settings.size[0]*len(self.board)), int(pos[1]/self.settings.size[1]*len(self.board[0]))]
                    self.start = xy
                elif event.key == pygame.K_f:
                    pos = pygame.mouse.get_pos()
                    xy = [int(pos[0]/self.settings.size[0]*len(self.board)), int(pos[1]/self.settings.size[1]*len(self.board[0]))]
                    self.finish = xy
                elif event.key == pygame.K_SPACE:
                    self.finding = True
            elif event.type == pygame.MOUSEMOTION:
                if self.drawing:
                    pos = pygame.mouse.get_pos()
                    xy = [int(pos[0]/self.settings.size[0]*len(self.board)), int(pos[1]/self.settings.size[1]*len(self.board[0]))]
                    if xy not in self.last:
                        self.change_board(xy[1], xy[0])
                        self.last.append(xy)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.drawing = False
                self.last = []

    def run(self):
        self.running = True
        self.drawing = False
        self.last = []
        self.finding = False

        while self.running:
            self.controls()
            if self.finding:
                self.aStarFind()
            self.draw()

if __name__ == "__main__":
    test = board()
    test.run()