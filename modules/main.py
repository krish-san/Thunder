import pygame
from pygame import mixer
import math
import random #for random enemy value

pygame.init()
#width and height as parameters

screen = pygame.display.set_mode((800, 600))
#bg
bg = pygame.image.load("bgcrt.png")

#bgmusic
mixer.music.load('bgmusic.mp3')
mixer.music.play(-1) #for loop


#tinkerings
pygame.display.set_caption("thunder the idiot")
img = pygame.image.load('spaceship.png')
pygame.display.set_icon(img)
#player
playerimg = pygame.image.load('thunder.png.png')
playerX = 350 #exact centre
playerY = 480 #rendering x and y axis
change_x = 0

#enemy
enemyimg = []
enemyX = []
enemyY = []
change_ex = []
change_ey = []
no_of_enemies = 5
for i in range(no_of_enemies):
    enemyimg.append(pygame.image.load('demon.png'))
    enemyX.append(random.randint(0, 800)) # randomly choses int
    enemyY.append(random.randint(50, 150))
    change_ex.append(1)
    change_ey.append(40)




#flash
# ready not appear , fire moving state
flashimg = pygame.image.load('flash.png')
flashX = 0
flashY = 480
change_fx = 0
change_fy = 5
flash_state = "ready"

#scores
score = 0
font = pygame.font.Font('freesansbold.ttf', 28)
textX = 10
textY = 10

#over text
ovrfnt = pygame.font.Font('freesansbold.ttf', 70)


def scored(x,y):
    sc = font.render("demons killed:" + str(score), True, (255,255,255))
    screen.blit(sc,(x,y))

def game_over():
    ov = ovrfnt.render("GAME OVER IDIOT !", True, (255,0,0))
    screen.blit(ov,(60,250))

def player(x, y):
    screen.blit(playerimg,(x, y))
def enemy(x, y, i):
    screen.blit(enemyimg[i],(x, y))
def fire(x, y):
    global flash_state #need to accces so
    flash_state = "fire"
    screen.blit(flashimg, (x+16, y+10)) #froom where in icon bullet shld come out
#distance kandupidichu short a iruntha killed
def collision(enemyX,enemyY,flashX,flashY):
    distance = math.sqrt((math.pow(enemyX-flashX,2))+(math.pow(enemyY-flashY,2)))
    if distance < 27:
        return True
    return False

#for events
#game loop anything we need consistently shld be inside while loop
run = True
while run:

    # RGB= 0 to 255, now this is BLACK
    screen.fill((0, 0, 0))
    #bg
    screen.blit(bg,(0, 0))#heavy bg so speed kammmi aidum
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keystroke pressed check left or right

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change_x = -3
            if event.key == pygame.K_RIGHT:
                change_x = 3
            if event.key == pygame.K_SPACE:
                if flash_state is "ready":#ready na matum than another bullet fire pannanum
                    bltsnd = mixer.Sound('bltsnd.mp3')
                    bltsnd.play()
                    flashX = playerX
                    fire(flashX, flashY)

        if event.type == pygame.KEYUP: #when released, see in print prompt
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change_x = 0
    #let 5=5+0.1 or 5=5+ -0.1 ie 5=5-0.1
    playerX += change_x

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736: #cover boundary
        playerX = 736

    #enemy movement
    for i in range(no_of_enemies):

        #game over
        if enemyY[i] > 440 :
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += change_ex[i]
        if enemyX[i] <= 0:
            change_ex[i] = 1
            enemyY[i] += change_ey[i]
        elif enemyX[i] >= 736:
            change_ex[i] = -1
            enemyY[i] += change_ey[i]

        # collision
        col = collision(enemyX[i], enemyY[i], flashX, flashY)
        if col:
            killsnd = mixer.Sound('killsnd.mp3')
            killsnd.play()
            flashY = 480
            flash_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0, 800)  # randomly choses int
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    #flash mvememnt
    if flashY <= 0: #restoring
        flashY = 480
        flash_state = "ready"
    if flash_state is "fire":
        fire(flashX,flashY)
        flashY -= change_fy #y axis 5 aala dec aagi bullet mela pogum


    player(playerX, playerY)
    scored(textX,textY)
    pygame.display.update()