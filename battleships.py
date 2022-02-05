import pygame 
import os
pygame.font.init() #init pygame font lib
pygame.mixer.init() #init pygame music lib

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BATTLESHIPS")

RED = ( 255 , 0 , 0 )
WHITE = ( 255 , 255 , 255 )
BLACK = ( 0 , 0 , 0 )
YELLOW = (255, 255, 0)

FPS = 60

HEALTH_FONT = pygame.font.SysFont('ariel', 40)
WINNER_FONT = pygame.font.SysFont('ariel', 100)

BORDER = pygame.Rect(WIDTH/2-5, 0, 10, HEIGHT)

VEL = 5
BULLET_VEL = 5

MAX_BULLETS = 5

RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT = 50,50

YELLOW_SPACE_SHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACE_SHIP_IMAGE = pygame.transform.scale (YELLOW_SPACE_SHIP_IMAGE, (SPACE_SHIP_WIDTH,SPACE_SHIP_HEIGHT))
YELLOW_SPACE_SHIP_IMAGE = pygame.transform.rotate (YELLOW_SPACE_SHIP_IMAGE, 90 )

RED_SPACE_SHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACE_SHIP_IMAGE = pygame.transform.scale (RED_SPACE_SHIP_IMAGE, (SPACE_SHIP_WIDTH,SPACE_SHIP_HEIGHT))
RED_SPACE_SHIP_IMAGE = pygame.transform.rotate (RED_SPACE_SHIP_IMAGE, 270 )

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT ))

FIRE = pygame.mixer.Sound(os.path.join('Assets', "Gun+Silencer.mp3"))
CRASH = pygame.mixer.Sound(os.path.join('Assets', "Grenade+1.mp3"))




def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:    #LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:    #RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:    #UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT:    #DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:     #LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:    #RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:       #UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:     #DOWN
        red.y += VEL
        
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
            
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
        
        
    

def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    
    WIN.blit(BACKGROUND, (0, 0))
    
    red_health_text = HEALTH_FONT.render("Health: "+ str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: "+ str(yellow_health), 1, WHITE)
    WIN.blit( red_health_text, (WIDTH- red_health_text.get_width()- 10, 10))
    WIN.blit( yellow_health_text, (10, 10))
    
    pygame.draw.rect(WIN, WHITE, BORDER)
    WIN.blit(YELLOW_SPACE_SHIP_IMAGE, (yellow.x,yellow.y))
    WIN.blit(RED_SPACE_SHIP_IMAGE, (red.x,red.y))
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)    
        
    pygame.display.update() #window is not updated just from the program; is it essential to update the window with this; try without command

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2-draw_text.get_width()//2, HEIGHT//2))
    
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    
    yellow = pygame.Rect(100, 225, SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)
    red = pygame.Rect(800, 225, SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)
    
    yellow_bullets = []
    red_bullets = []
    
    yellow_health = 5
    red_health = 5
    
    clock = pygame.time.Clock()
    run = True #makes sure game keeps running unless told otherwise
    
    while run: #main loop
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.width//2, 10, 5) #bullet creation
                    yellow_bullets.append(bullet)   #bullet added to yellow bullet list
                    FIRE.play()
                    
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x , red.y + red.width//2, 10, 5)   #red bullet creation
                    red_bullets.append(bullet)
                    FIRE.play()
                    
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                CRASH.play()
                
            if event.type == RED_HIT:
                red_health -= 1
                CRASH.play()
                
        winner_txt = ""
        if red_health <= 0:
            winner_txt = "FUCK YOU RED"
            
        if yellow_health <= 0:
            winner_txt = "FUCK YOU YELLOW"
            
        if winner_txt != "":
            draw_winner(winner_txt)
            break
                
            
                    
        keys_pressed = pygame.key.get_pressed() #gets the value of any key pressed and stores it in keys_pressed
        yellow_handle_movement( keys_pressed, yellow)
        red_handle_movement( keys_pressed, red)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        
             
        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)
        
        
    main()

if __name__ == "__main__": 
    main()

            