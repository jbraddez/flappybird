import pygame
from pygame.locals import *
import random
import time
from os import path

pygame.init()

font = pygame.font.SysFont('Bauhaus 93', 60)
font2 = pygame.font.SysFont('Pixel', 60)

white = (255, 255, 255)

clock = pygame.time.Clock()
fps = 60
flying = False
game_over = False
pipe_gap = 150
pipe_freq = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_freq
score = 0 
pass_pipe = False
highscore = 73 #Hs alltime: 73

SCREEN_WIDTH = 680
SCREEN_HEIGHT = 780

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")  # gives window a title

score_screen = pygame.image.load("scorescreen.png")
score_screen = pygame.transform.rotozoom(score_screen, 0, 1.4)

#define game variables
ground_scroll = 0
scroll_speed = 4

#load images
bg = pygame.image.load('bg.png')
ground = pygame.image.load('ground.png')
button_img = pygame.image.load('restart.png')


def draw_text(text,font,text_col, x, y):
    img = font.render(text, True , text_col)
    screen.blit(img, (x, y))



start_screen = pygame.image.load('startscreen.png')  
start_screen = pygame.transform.scale(start_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))


    
def reset_game():
    pipe_group.empty() # deletes everything in pipe group
    flappy.rect.x = 100
    flappy.rect.y = int(SCREEN_HEIGHT / 2)
    score = 0
    return score


class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f'bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() # creates boundaries for you
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
    
    def update(self):
        if flying == True:
            self.vel += 0.5   # gravity
            if self.vel > 8: # limit velocity
                self.vel = 8
            if self.rect.bottom < 662:   # doesnt let go through floor
                self.rect.y += int(self.vel)

        if game_over == False:
            #jump
            key = pygame.key.get_pressed() # check if key is pressed
            if key[pygame.K_SPACE] == True and self.clicked == False: # so cant hold space
                self.clicked = True
                self.vel = -10
            if key[pygame.K_SPACE] == False: # so cant hold space
                self.clicked = False 
                
            #handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
    
            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class YelBird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f'yellowbird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() # creates boundaries for you
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
    
    def update(self):
        if flying == True:
            self.vel += 0.5   # gravity
            if self.vel > 8: # limit velocity
                self.vel = 8
            if self.rect.bottom < 662:   # doesnt let go through floor
                self.rect.y += int(self.vel)

        if game_over == False:
            #jump
            key = pygame.key.get_pressed() # check if key is pressed
            if key[pygame.K_SPACE] == True and self.clicked == False: # so cant hold space
                self.clicked = True
                self.vel = -10
            if key[pygame.K_SPACE] == False: # so cant hold space
                self.clicked = False 
                
            #handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
    
            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
def draw_button():
    screen.blit(button_img, int((SCREEN_WIDTH // 2), int(SCREEN_HEIGHT // 2 + 200)))
    pygame.display.update()
    key = pygame.key.get_pressed() # check if key is pressed
    if key[pygame.K_SPACE] == True:
        pipe_group.empty()
        flappy.rect.x = 100
        flappy.rect.y = int(SCREEN_HEIGHT // 2)
        score = 0
        return score
    
def check_highscore(highscore,score):
    if score > highscore:
        highscore = score
    return highscore

def draw_end_scores(score, font2, text_col):
    scoreimg = font2.render(score, True, text_col)
    screen.blit(scoreimg, (390, 430))
    highscoreimg = font2.render(str(highscore), True, text_col)
    screen.blit(highscoreimg, (455  , 558))

def draw_text(text,font,text_col, x, y):
    img = font.render(text, True , text_col)
    screen.blit(img, (x, y))
    img1 = font.render(f'Highscore: {highscore}', True , text_col)
    x1 = SCREEN_WIDTH / 2 - 125
    y1 = SCREEN_HEIGHT - 50
    screen.blit(img1, (x1, y1))


def reset_game():
    pipe_group.empty() # deletes everything in pipe group
    flappy.rect.x = 100
    flappy.rect.y = int(SCREEN_HEIGHT / 2)
    score = 0
    game_over = False
    run = True
    flying = False
    return score ,game_over ,run, flying

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect() #create rectangle around it
        #position 1 is from top -1 is from bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x,y + int(pipe_gap / 2)]
    
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()



class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        #draw button
        screen.blit(button_img, (self.rect.x, self.rect.y))

        #check if mouse over button
        if flappy.rect.bottom >= 662:
            if keys[pygame.K_SPACE]:
                action = True
            elif self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1: # index for left center or right click
                    action = True


        return action

        
red_start = pygame.image.load("redstart1.png")
red_start = pygame.transform.rotozoom(red_start, 0 , 2)
yellow_start = pygame.image.load("yelstart.png")
yellow_start = pygame.transform.rotozoom(yellow_start, 0 ,2)

        
class StartButton():
    def __init__(self ,x ,y ,img ):
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False



        screen.blit(self.image, (self.rect.x , self.rect.y))

        return action


redbutton = StartButton(60, 350, red_start)
yelbutton = StartButton(380, 350 , yellow_start)


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(SCREEN_HEIGHT / 2))

bird_group.add(flappy) # bord class added to bird group



#create restart button instance
button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100, button_img)


logo = pygame.image.load("logo.png").convert()
logo = pygame.transform.rotozoom(logo, 0, 0.2)

game_over_sign = pygame.image.load("gameover.png").convert()
game_over_sign = pygame.transform.rotozoom(game_over_sign, 0 , 0.47)

press_to_start_img = pygame.image.load("press_to_start.png")
press_to_start_img = pygame.transform.rotozoom(press_to_start_img, 0 , 1.45)

game_started = False
first_jump = False

bird_col = ""
bird_chosen = False

red_start_rect = red_start.get_rect()
yel_start_rect = yellow_start.get_rect()

def draw_menu():
    screen.blit(red_start, (50, 250))
    screen.blit(yellow_start, (400, 250))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        bird_col = "red"
        
        return bird_col
    elif keys[pygame.K_d]:
        bird_col = "yellow"
        
        return bird_col
begin = True
run = True
while run:

    
    

    clock.tick(fps)

    #draw background
    screen.blit(bg, (0,0))

    #draw bird
    bird_group.draw(screen)
    bird_group.update()

    #draw pipes
    pipe_group.draw(screen)
    

    #draw ground
    screen.blit(ground, (ground_scroll,662)) 

    #check score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
        and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(SCREEN_WIDTH / 2), 20)

    #look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0: #if set to true it kills certain group
        game_over = True
    #check if bird has hit the ground
    if flappy.rect.bottom >= 662:
        game_over = True
        flying = False


    if game_started == False:
        screen.blit(start_screen, (0,0))
        if redbutton.draw():
            bird_col = "red"
            flappy = Bird(100, int(SCREEN_HEIGHT // 2))
            bird_group.empty()
            bird_group.add(flappy)
            game_started = True   
        if yelbutton.draw():
            bird_col = "yellow"
            flappy = YelBird(100, int(SCREEN_HEIGHT // 2))
            bird_group.empty()
            bird_group.add(flappy)
            game_started = True   
        
        
    if first_jump == False and game_started == True:
        screen.blit(logo, (102, 105))
        screen.blit(press_to_start_img, (105, int(SCREEN_HEIGHT // 2 + 80)))
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            first_jump = True
    
    if game_over == False and flying == True:
        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_freq:
            pipe_height = random.randint(-100,100)
            btm_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, -1)
            top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now


        #scroll ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > SCREEN_WIDTH-645:
            ground_scroll = 0

        #update pipes
        pipe_group.update()
    
    #check for game over and reset   # this section is what closes the window
    if game_over == True:
        screen.blit(game_over_sign, (60, 80))
        screen.blit(score_screen, (70,300 ))
        draw_end_scores(str(score), font2, white)
        if button.draw() == True:
                game_over = False
                score,game_over,run,flying = reset_game()


        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and flying == False and game_over == False:
            flying = True
        if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
            time.sleep(2.5)

    
            

        
    pygame.display.update()



pygame.quit()