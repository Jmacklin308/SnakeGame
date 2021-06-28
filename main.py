import pygame, sys, random
from pygame.math import Vector2




class INPUT: #contains keys used
    UP = pygame.K_w
    DOWN = pygame.K_s
    LEFT = pygame.K_a
    RIGHT = pygame.K_d


class SNAKE: #the snaaeeeek
    def __init__(self):
        #store every body part in our snake
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False
        
    
        #setup the sprites:
    
        #head
        self.head_up = pygame.image.load('res/snakeHead-up.png')
        self.head_down = pygame.image.load('res/snakeHead-down.png')
        self.head_left = pygame.image.load('res/snakeHead-left.png')
        self.head_right = pygame.image.load('res/snakeHead-right.png')
    
        #tail
        self.tail_up = pygame.image.load('res/snaketail-up.png')
        self.tail_down = pygame.image.load('res/snaketail-down.png')
        self.tail_left = pygame.image.load('res/snaketail-left.png')
        self.tail_right = pygame.image.load('res/snaketail-right.png')
    
    
        #body
        self.body_up = pygame.image.load('res/snakeBody-up.png')
        self.body_down = pygame.image.load('res/snakeBody-down.png')
        self.body_left = pygame.image.load('res/snakeBody-left.png')
        self.body_right = pygame.image.load('res/snakeBody-right.png')
    
        #curve
        self.body_tr = pygame.image.load('res/tailCurve-tr.png')
        self.body_tl = pygame.image.load('res/tailCurve-tl.png')
        self.body_br = pygame.image.load('res/tailCurve-br.png')
        self.body_bl = pygame.image.load('res/tailCurve-bl.png')

        self.head = self.head_right
        self.tail = self.tail_right
    
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        
        
        for index,block in enumerate(self.body):
            #1. need a rect for positioning
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos,y_pos,CELL_SIZE,CELL_SIZE)
            
            #2. what direction is head heading
            if index == 0: #this is the head
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            
            
            else:
                pygame.draw.rect(screen,c_orange,block_rect)
            
            #3.

    def update_head_graphics(self):
        head_direction = self.body[1] - self.body[0]
        if head_direction == Vector2(1,0): self.head = self.head_left
        if head_direction == Vector2(-1,0): self.head = self.head_right
        if head_direction == Vector2(0,1): self.head = self.head_up
        if head_direction == Vector2(0,-1): self.head = self.head_down
        
        
    ###################WORKED ON TAIL LAST
    #TODO: Fix up tail (follow https://www.youtube.com/watch?v=QFvqStqPCRU)
    def update_tail_graphics(self):
        tail_direction = self.body[1] - self.body[-1]
        if tail_direction == Vector2(1,0): self.tail = self.tail_left
        if tail_direction == Vector2(-1,0): self.tail = self.tail_right
        if tail_direction == Vector2(0,1): self.tail = self.tail_up
        if tail_direction == Vector2(0,-1): self.tail = self.tail_down
        
    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True


class FRUIT:#for the fruit
    def __init__(self):
        self.x = None
        self.y = None
        self.pos = None
        self.randomize()
    def draw_Fruit(self):
        fruit_Rectangle = pygame.Rect(int(self.pos.x * CELL_SIZE),int(self.pos.y * CELL_SIZE),CELL_SIZE,CELL_SIZE)
        #pygame.draw.rect(screen,c_orange,fruit_Rectangle)
        screen.blit(apple,fruit_Rectangle)
    def randomize(self):
        self.x = random.randint(0,CELL_NUMBER-1)
        self.y = random.randint(0,CELL_NUMBER-1)
        self.pos = Vector2(self.x,self.y)


class MAIN:#main game class
    def __init__(self): #create the snake and fruit objects
        self.snake = SNAKE()
        self.fruit = FRUIT()
        
    def update(self):#called each frame
        self.snake.move_snake()
        self.check_collision()
        #check if you hit the wall or yourself
        self.check_fail()
        
    def draw_elements(self): #called each frame
        self.fruit.draw_Fruit()
        self.snake.draw_snake()
        
    def input_check(self): #check for input, called each frame
        for event in pygame.event.get():
            #quit if player closes the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN: #check keyboard input
                if event.key == INPUT.UP:
                    if main_game.snake.direction.y != 1:
                        self.snake.direction = Vector2(0,-1)
                if event.key == INPUT.DOWN:
                    if main_game.snake.direction.y != -1:
                        self.snake.direction = Vector2(0,1)
                if event.key == INPUT.LEFT:
                    if main_game.snake.direction.x != 1:
                        self.snake.direction = Vector2(-1,0)
                if event.key == INPUT.RIGHT:
                    if main_game.snake.direction.x != -1:
                        self.snake.direction = Vector2(1,0)
    
    def check_collision(self):
        #check if the head is over the apple
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize() #randomize location
            self.snake.add_block()
    
    def check_fail(self):
        #if the head is less than the cell number (up and down)
        if not 0 <= self.snake.body[0].x < CELL_NUMBER:
            self.game_over()
        if not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.game_over()
        #check if the snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
        
        #TODO: check if the snake hits itself

    @staticmethod
    def game_over():
        pygame.quit()
        sys.exit()
        
        
        
#initalize the game
pygame.init()

#game constants
CELL_SIZE = 40
CELL_NUMBER = 20

#main screen
screen = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE),0,32)

#set colors
c_white = (255, 246, 211)
c_orange = (235, 107, 111)
c_brown = (124, 63, 88)
c_peach = (249, 168, 117)

#create delta
clock = pygame.time.Clock()


#create a timer for movement
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,100)

#create game graphics
apple = pygame.image.load('res/applex2.png')
snakeBody = pygame.image.load('res/snakeBodyx2.png')
snakeHead = pygame.image.load('res/snakeHeadx2.png')

main_game = MAIN()

while True:
    #Event loop
    main_game.input_check()
    
    #refresh the screen
    screen.fill(c_white)
    
    #draw the elements
    main_game.draw_elements()

    #update to next frame
    pygame.display.update()
    
    #set game to 60 fps
    clock.tick(60)
    
