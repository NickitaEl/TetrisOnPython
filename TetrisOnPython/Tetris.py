import pygame,random
pygame.init()
colors = [
    (149,34,206),
    (255,0,0),
    (0,255,34),
    (0,51,255),
    (255,230,0)
    ]
class Figure():
    figures = [
        [ [1,5,9,13], [4,5,6,7]  ],
        [ [1,2,5,6] ],
        [ [4,5,9,10], [2,6,5,9] ],
        [ [6,7,9,10], [1,5,6,10]],
        [ [1,2,5,9], [0,4,5,6],[1,5,8,9],[4,5,6,10]],
        [ [1,2,6,10],[5,6,7,9],[2,6,10,11],[3,5,6,7]],
        [ [1,4,5,6],[1,4,5,9],[4,5,6,9],[1,5,6,9]]     
    ]
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.type = random.randint(0,len(self.figures)-1)
        self.rotation= 0
        self.color = random.randint(0,len(colors)-1)
        
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

    def image(self):
        return self.figures[self.type][self.rotation]
    
class Tetris():
    x = 100
    y = 60
    kl = 20
    score = 0
    state = "start"
    width = 10
    height = 20
    def __init__(self):
        self.field = []
        for i in range(self.height):
            self.field.append([])
            for j in range(self.width):
                self.field[i].append(-1)
                
    def new_figure(self):
        self.figure = Figure(3,0)
        
    def intersect(self):
        for i in range(4):
            for j in range(4):
                if i*4+j in self.figure.image():
                    if i+self.figure.y >= self.height or not( 0<= j+self.figure.x < self.width) or self.field[i+self.figure.y][j+self.figure.x] != -1:
                        return True
        return False
    
    def break_lines(self):
        for i in range(1,self.height):
            zero = 0
            for j in range(self.width):
                if self.field[i][j] == -1:
                    zero += 1
            if zero == 0:
                self.score += 1
                for k in range(i,1,-1):
                    for j in range(self.width):
                        self.field[k][j] = self.field[k-1][j]
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i*4+j in self.figure.image():
                    self.field[i+self.figure.y][j+self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersect():
            self.state = 'dead'
    def down(self):
        self.figure.y += 1
        if self.intersect():
            self.figure.y -= 1
            self.freeze()
    def left(self):
        self.figure.x -= 1
        if self.intersect():
            self.figure.x += 1
    def right(self):
        self.figure.x += 1
        if self.intersect():
            self.figure.x -= 1
    def rotate(self):
        old = self.figure.rotation
        self.figure.rotate()
        if self.intersect():
            self.figure.rotation = old

size = (400,500)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 15

game = Tetris()
game.new_figure()
play = True

count = 0
while play:
    count += 1
    if count%5==0 and game.state == 'start':
        game.down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        game.left()
    if key[pygame.K_RIGHT]:
        game.right()
    if key[pygame.K_DOWN]:
        game.down()
    if key[pygame.K_UP]:
        game.rotate()

    screen.fill(pygame.Color('black'))
    for i in range(game.height):
        for j in range(game.width):
            if game.field[i][j] != -1:
                pygame.draw.rect(screen,colors[game.field[i][j]],[game.x+game.kl*j, game.y+game.kl*i, game.kl,game.kl] )
    for i in range(4):
        for j in range(4):
            p = i*4+j
            if p in game.figure.image():
                pygame.draw.rect(screen, colors[game.figure.color], [ game.x+game.kl*(j+game.figure.x),game.y+game.kl*(i+game.figure.y),game.kl,game.kl])
    for i in range(game.x, game.width*game.kl+game.x+1, game.kl):
        pygame.draw.line(screen,pygame.Color('white'),[i,game.y],[i,game.y+game.height*game.kl],2)
    for i in range(game.y, game.height*game.kl+game.y+1, game.kl):
        pygame.draw.line(screen,pygame.Color('white'),[game.x,i],[game.x+game.kl*game.width,i],2)
    if game.state == 'dead':
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
    clock.tick(fps)
    pygame.display.flip()
