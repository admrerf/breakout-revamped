# -*- coding: utf-8 -*-
"""
huge reference from TokyoEdTech@youtube

"""



import pygame, sys, math, random




pygame.init() #inisialisasi
pygame.display.set_caption("Breakout! Revamped by Team D") #judul di header
clock = pygame.time.Clock() #idk why this part exists

WIDTH = 1200 #lebar screen
HEIGHT = 800 #panjang screen

HITAM = (0, 0, 0) #default rgb hitam
PUTIH = (255, 255, 255) #default rgb putih
HIJAU = (86, 174, 87)
MERAH = (242, 85, 96)
BIRU = (69, 177, 232)
paddle_col = (142, 135, 123)
paddle_outline = (100, 100, 100)

#bikin layarnya
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#bikin classes
class Paddle:
    def __init__(self):
        self.x = 0
        self.y = 700
        self.dx = 0
        self.width = 200
        self.height = 25
        self.score = 0
 
    def left(self):
        self.dx = -20 #kecepatan gerak ke kiri
    
    def right(self):
        self.dx = 20 #kecepatan gerak ke kanan
    
    def move(self):
        self.x += self.dx #ini beda dari source codenya
        
        #cek kalau mentok ke pinggir layar
        if self.x < 0 + (self.width/2):
            self.x = 0 + self.width/2
            self.dx = 0
        
        elif self.x > WIDTH - (self.width/2):
            self.x = WIDTH - (self.width/2)
            self.dx = 0
            
    def render(self):
        pygame.draw.rect(screen, paddle_col, pygame.Rect(int(self.x-self.width/2), int(self.y-self.height/2), self.width, self.height)) #bikin paddle bentuk persegi panjang
        pygame.draw.rect(screen, paddle_outline, pygame.Rect(int(self.x-self.width/2), int(self.y-self.height/2), self.width, self.height), 3)
        #jadi .rect itu urutannya left, top, width, height
        #kalau mau ngambil topnya, berarti ambil int(self.y - self.height/2)
        
class Ball:
    def __init__(self):
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.dx = 6
        self.dy = -6
        self.width = 20
        self.height = 20
     
    def move(self):
        self.x += self.dx
        self.y += self.dy
        
        #cek kalau mentok ke pinggir layar
        if self.x < 0 + (self.width/2):
            self.x = 0 + (self.width/2)
            self.dx *= -1
        
        elif self.x > WIDTH - (self.width/2):
            self.x = WIDTH - (self.width/2)
            self.dx *= -1
        
        if self.y < 0 + (self.height/2):
            self.y = 0 + (self.height/2)
            self.dy *= -1 #mantul
        
        elif self.y > HEIGHT - (self.height/2):
            self.y = HEIGHT - (self.height/2)
            self.x = WIDTH/2 #balik ke tengah
            self.y = HEIGHT/2
            
            
    def render(self):
        pygame.draw.rect(screen, PUTIH, pygame.Rect(int(self.x-self.width/2), int(self.y-self.height/2), self.width, self.height)) #bikin paddle bentuk persegi panjang        

    def is_aabb_collision(self, other):
        #Axis Aligned Bounding Box
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision= (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return(x_collision and y_collision)

class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 25
        self.color = random.choice([BIRU, HIJAU, MERAH])
            
    def render(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(int(self.x-self.width/2), int(self.y-self.height/2), self.width, self.height)) #bikin paddle bentuk persegi panjang

#create font
font = pygame.font.SysFont("monospace", 30)

#create sound
bounce_sound = pygame.mixer.Sound("bounce.wav")
pop_sound = pygame.mixer.Sound("brickpop.wav")
#bikin object
paddle = Paddle()
ball = Ball()

bricks = []
for y in range(100, 375, 25): #1200-25 for every 50x
    color = random.choice([PUTIH, MERAH, HIJAU, BIRU])
    for x in range(25, 1200, 50):
        bricks.append(Brick(x, y))
        bricks[-1].color = color

#---------------------main game loop---------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit() #buat keluar game
    
        #keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle.left() #gerak kiri
            elif event.key == pygame.K_RIGHT:
                paddle.right() #gerak kanan
                
    #update objects
    paddle.move()
    ball.move()
    
    #check for collisions
    if ball.is_aabb_collision(paddle): #kalau bola collide dengan paddle
        ball.dy *= -1 #mantul kalo tabrakan sama paddle
        bounce_sound.play()

    
    dead_bricks = []
    for brick in bricks:
        if ball.is_aabb_collision(brick):
            ball.dy *= -1
            dead_bricks.append(brick)
            paddle.score += 10
            pop_sound.play()

    for brick in dead_bricks:
        bricks.remove(brick) #ngapus brick yang udah disingkirin

    if len(bricks) <= 0: #kalau brick udah habis
        print("GAME OVER")
            
    #Render (draw stuffs)
    #fill background color
    screen.fill(HITAM)
    
    #render objects
    paddle.render()
    ball.render()
    
    for brick in bricks:
        brick.render()
    
    
    
    #render the score
    score_surface = font.render(f"Score: {paddle.score}", True, PUTIH)
    screen.blit(score_surface, ((WIDTH/2)-75, 20))
    
    
    #flip layar
    pygame.display.flip()
    
    #set fps
    clock.tick(30)