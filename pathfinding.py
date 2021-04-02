import numpy as np
import pygame

class board():
    def __init__(self, row, col, size=(500, 500), bgcolor = (0,0,0)):
        pygame.init()
        self.screen = pygame.display.set_mode(size)

        self.bgcolor = bgcolor
        self.size = size

        self.board = np.zeros([row, col])
        self.aStar = []
        self.step = 0
        self.finish = None
        self.path = []

    def change_board(self, row, col):
        if self.board[row][col] == 0:
            self.board[row][col] = 1
        else:
            self.board[row][col] = 0

    def draw(self):
        self.screen.fill(self.bgcolor)
        
        l = self.size[0]/len(self.board)
        d = self.size[1]/len(self.board[0])
        for i in self.aStar:
            pygame.draw.rect(self.screen, (100,0,0), (l*i[1], d*i[0], l, d))
        for i in self.path:
            if i != None:
                pygame.draw.rect(self.screen, (200,0,0), (l*i[1], d*i[0], l, d))
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    pygame.draw.rect(self.screen, (200, 200, 200), (l*j, d*i, l,d))
                elif self.board[i][j] == 2:
                    pygame.draw.rect(self.screen, (0, 200, 200), (l*j, d*i, l,d))
                elif self.board[i][j] == 3:
                    pygame.draw.rect(self.screen, (200, 200, 0), (l*j, d*i, l,d))
        pygame.display.update()

    def in_list(self, x, y):
        good = True
        if self.board[x][y] == 1:
            good = False
        for j in self.aStar:
            if j[0]==x and j[1]==y:
                good = False
        if good:
            self.aStar.append([x,y,self.step+1])

    def run(self):
        running = True
        drawing = False
        last = []
        finding = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        pos = pygame.mouse.get_pos()
                        xy = [int(pos[0]/self.size[0]*len(self.board)), int(pos[1]/self.size[1]*len(self.board[0]))]
                        self.board[xy[1], xy[0]] = 2
                    elif event.key == pygame.K_f:
                        pos = pygame.mouse.get_pos()
                        xy = [int(pos[0]/self.size[0]*len(self.board)), int(pos[1]/self.size[1]*len(self.board[0]))]
                        self.board[xy[1], xy[0]] = 3
                        self.finish = [xy[1], xy[0]]
                    elif event.key == pygame.K_SPACE:
                        finding = True
                elif event.type == pygame.MOUSEMOTION:
                    if drawing:
                        pos = pygame.mouse.get_pos()
                        xy = [int(pos[0]/self.size[0]*len(self.board)), int(pos[1]/self.size[1]*len(self.board[0]))]
                        if xy not in last:
                            self.change_board(xy[1], xy[0])
                            last.append(xy)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    drawing = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    drawing = False
                    last = []
            
            if finding:
                if len(self.aStar) == 0:
                    for i in range(len(self.board)):
                        for j in range(len(self.board[i])):
                            if self.board[i][j] == 2:
                                self.aStar.append([i, j, 0])
                                print(self.aStar)
                                break
                        if len(self.aStar) != 0:
                            break
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
                        print(i, self.finish)
                        finding = False
            else:
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
            self.draw()

if __name__ == "__main__":
    test = board(50,50)
    test.change_board(0,1)
    print(test.board)
    test.run()