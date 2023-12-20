import numpy as np
import pygame
import random
import copy

pygame.font.init() #initializes fonts
pygame.init()

win = pygame.display.set_mode((500, 1000)) #window size
pygame.display.set_caption("pygame") #window title
testFont = pygame.font.Font(None, 50) #defines font type

#mat = np.zeros((21, 10))
mat = [[0] * 10] * 20
change = False
#mat[5][5] = 4

colorList = {0: (30, 30, 30),
             1: (70, 70, 255),
             2: (255, 255, 0),
             3: (255,163,67),
             4: (255, 0, 255),
             5: (255, 255, 255),
             6: (0, 255, 0),
             7: (255, 0, 0)}

def returnColor(num):
    return colorList[num]

shapes = {
        1: np.array([
            [1, 1, 1, 1]
        ]),
        2: np.array([
            [2, 2],
            [2, 2]
        ]),
        3: np.array([
            [3, 3, 3],
            [3, 0, 0],
        ]),
        4: np.array([
            [4, 4, 4],
            [0, 0, 4],
        ]),
        5: np.array([
            [0, 5, 0],
            [5, 5, 5]
        ]),
        6: np.array([
            [6, 6, 0],
            [0, 6, 6],
        ]),
        7: np.array([
            [0, 7, 7],
            [7, 7, 0],
        ])
    }

list1  = [0, 1, 2, 3, 4, 5]
print(str(list1[:5]) + str(list1[5+1:]))
print([[0] * 10] * 10)


def lookupShape(num):
    return(shapes[num])

class Piece:

    def __init__(self, pos = [0, 0], rotation = 0, shape = None):
        #print(self.shapes)
        if shape is None:
            shape = random.randint(1, 7)
        shape = lookupShape(shape)
        self.shape = shape
        self.pos = pos
        self.rotation = rotation

    def solidifyToMat(self, mat):
        global change
        change = True
        for y, row in enumerate(self.shape):
            for x, item in enumerate(row):
                # print(x)
                if item != 0:
                    mat[y + self.pos[1]][x + self.pos[0]] = item
        self.pos = [0, 0]
        return mat

    def printPiece(self):
        for y, row in enumerate(self.shape):
            for x, item in enumerate(row):
                # print(x)
                if item != 0:
                    pygame.draw.rect(win, colorList[item], ((2 + 50 * (x + self.pos[0]), 2 + 50 * (y + self.pos[1])), (46, 46)), border_radius=8)

    def move(self, dir, mat):
        if dir == 1 and self.pos[1] > 0:
            self.pos[1] -= 1
        if dir == 2 and self.pos[0] > 0:
            self.pos[0] -= 1
        if dir == 3:# and self.pos[1] < 20 - len(self.shape):
            self.pos[1] += 1
        if dir == 4 and self.pos[0] < 10 - len(self.shape[0]):
            self.pos[0] += 1

        safe = True
        for y, row in enumerate(self.shape):
            for x, item in enumerate(row):
                #print(str(self.pos[0] + x) + " " + str(self.pos[1] + y))
                if (item != 0 and mat[self.pos[1] + y][self.pos[0] + x] != 0) or self.pos[1] == 21 - len(self.shape):
                    if dir == 1:
                        self.pos[1] += 1
                    if dir == 2:
                        self.pos[0] += 1
                    if dir == 3:
                        self.pos[1] -= 1
                    if dir == 4:
                        self.pos[0] -= 1
                    mat = self.solidifyToMat(mat)



        return mat

    def rotate(self, dir = 1):
        self.shape = np.rot90(self.shape, dir)
        if len(self.shape[0]) + self.pos[0] > 10 or len(self.shape) + self.pos[1] > 20:
            self.shape = np.rot90(self.shape, dir)
            print("failed turn")
        #print(self.shape)







    def __str__(self):
        return f"({self.shape})"

objects = {}
objects[0] = Piece([0, 0])
currentObj = 1

score = 0
extraMat = copy.deepcopy(mat)
timer = 0
running = True
while running:
    pygame.time.delay(60) #time between frames (in ms)



    keys = pygame.key.get_pressed() #all pressed keys

    win.fill((60, 60, 60)) #fills screen background

    for y, row in enumerate(mat):
        for x, item in enumerate(row):
            #print(x)
            pygame.draw.rect(win, colorList[item], ((2 + 50 * x, 2 + 50 * y), (46, 46)), border_radius=8)
            pass






    #This makes the rectangles on screen
    #pygame.draw.rect(win, (255, 255, 255), ((15, 10), (75, 50)))
    # rect(window, color in rgb, ((xpos top left, ypostopleft), (x-width, y-height)))

    #pygame.draw.rect(win, (255, 255, 255), ((15, 70), (75, 50)), border_radius=10)
    # rect(window, color in rgb, ((xpos top left, ypostopleft), (x-width, y-height)), rounded corners = x)

    #pygame.draw.rect(win, (255, 255, 255), ((15, 130), (75, 50)), width=5)
    # rect(window, color in rgb, ((xpos top left, ypostopleft), (x-width, y-height)), side width = x)

    timer += 1
    if timer % 10 == 0:
        mat = objects[list(objects)[-1]].move(3, mat)



    for event in pygame.event.get(): #when close button pushed, loop ends
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                mat = objects[list(objects)[-1]].solidifyToMat(mat)
            if event.key == pygame.K_e:
                objects[list(objects)[-1]].rotate()

    extraMat = copy.deepcopy(mat)

    if keys[pygame.K_w]:
        mat = objects[list(objects)[-1]].move(1, mat)
    if keys[pygame.K_a]:
        mat = objects[list(objects)[-1]].move(2, mat)
    if keys[pygame.K_s]:
        mat = objects[list(objects)[-1]].move(3, mat)
    if keys[pygame.K_d]:
        mat = objects[list(objects)[-1]].move(4, mat)

    #print(mat)

    if keys[pygame.K_SPACE] or change:
        objects[currentObj] = Piece([0, 0])
        currentObj += 1
        objects[list(objects)[-1]]
        print("--------------")
        print(objects)
        change = False

    '''
    for item in objects:
        objects[item].printPiece()
    '''
    objects[list(objects)[-1]].printPiece()
    for y, row in enumerate(mat):
        if not 0 in row:
            for i in range(len(row)):
                for j in range(y):
                    mat[y - j][i] = mat[y - 1 - j][i]
            score += 1
            print(f"score: {score}")

    pygame.display.update()
pygame.quit() #when the loop ends it closes the window
