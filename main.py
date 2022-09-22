import pygame
import random
import math
from pygame import mixer

#Initialize Pygame
pygame.init()   

#Create pygame window
screen=pygame.display.set_mode((800,600))   

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Background
background=pygame.image.load("bg.png")

#Background music
mixer.music.load("background.wav")
mixer.music.play(-1)

score_value=0
#Score
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10                     

def showscore(x,y):
    score=font.render("Score : "+str(score_value),True,(0,255,255))
    screen.blit(score,(x,y))
    
#Game Over
over=pygame.font.Font('freesansbold.ttf',64)
def game_over():
    over_text=over.render("GAME OVER!",True,(0,255,255))
    screen.blit(over_text,(200,250))

#Player
player_img=pygame.image.load('spaceship.png')
playerX=370
playerY=480
playerX_change=0
def player(x,y):
    screen.blit(player_img,(x,y))
    
#Enemy
enemy_img=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)
def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))
    
#Bullet
#Ready:cannot see bullet, #bullet on screen
bullet_img=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=0.8
bullet_state="ready"
def fire(x,y):
    screen.blit(bullet_img,(x+16,y+10))
    global bullet_state
    bullet_state="fire"
    
#Collision between bullet and enemy
def isCollision(bulletX,bulletY,enemyX,enemyY):
    distance=math.sqrt(math.pow((bulletX-enemyX),2)+math.pow((bulletY-enemyY),2))
    if distance<=27:
        return True
    else:
        return False
    

#Game Loop
running=True
while running:
    screen.fill((0,0,0))    #Always first as screen is drawn first
    screen.blit(background,(0,0))  #Everything gets slow to load this heavy img
    pass
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-1
            if event.key==pygame.K_RIGHT:
                playerX_change=1
            if event.key==pygame.K_SPACE:
                if bullet_state=="ready":
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX=playerX
                    fire(bulletX,bulletY)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0
            
    #Player Boundaries
    playerX+=playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736
       
    #Enemy Movement
    for i in range(num_of_enemies):
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over()
            break      
              
        if enemyX[i]<=0:
            enemyX_change[i]=0.5
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-0.5
            enemyY[i]+=enemyY_change[i]    
        enemy(enemyX[i],enemyY[i],i)
        enemyX[i]+=enemyX_change[i]
        #collision
        collision=isCollision(bulletX,bulletY,enemyX[i],enemyY[i])
        if collision:
            bulletY=480
            bullet_state="ready"
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)
            score_value+=1
            collision_sound=mixer.Sound('explosion.wav')
            collision_sound.play()
            
                
       
               
    #Bullet Movement
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"
    if bullet_state is "fire":
        fire(bulletX,bulletY)
        bulletY-=bulletY_change   
        
      
    player(playerX,playerY)
    showscore(textX,textY)
    
    pygame.display.update()
