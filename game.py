

import sys,pygame
from random import randint
from pygame.locals import*

pygame.init()
fpsClock = pygame.time.Clock()
screenSize = (640,480)
screen = pygame.display.set_mode(screenSize)
pygame.mixer.init()
pygame.mixer.music.load("music1.mp3")
pygame.mixer.music.play(10)
pygame.display.set_caption("My Game")
red = pygame.Color(255,0,0)
blue = pygame.Color(0,0,255)
green = pygame.Color(0,255,0)
white= pygame.Color(255,255,255)
running = True
mapRead = False
FPS = 60
font = pygame.font.SysFont("comicsansms",32)
clock = pygame.time.Clock()
tileMap = list()
initCounter =0
font1 = pygame.font.SysFont("comicsansms",28)
enemyList = list()
global playerCompleted
playerCompleted= False
global levelMap
gameStarted = False



def loadSpriteSheet(filename,numImgs,transformWidth,transformHeight):
    #return array of sprite imgs
    sheet = pygame.image.load(filename).convert_alpha()
    sheet.set_colorkey(white)
    spriteArr = list()
    locx =0
    imgWidth = sheet.get_width()/numImgs-1
    imgHeight = sheet.get_height()
    
    for i in range(numImgs):
        spriteArr.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(locx,0,imgWidth, imgHeight)),(transformWidth,transformHeight)))
        locx+=imgWidth
    return spriteArr
def loadLevel(level):
    if(level ==1):
        return Map("Map1.txt")
    elif(level==2):
         enemyList =list()
         levelMap.__init__("Map2.txt")
    elif(level==3):
        levelMap.__init__("Map3.txt")
    elif(level==4):
        levelMap.__init__("Map4.txt")
    elif(level==5):       
        player.won= True

def startScreen(mouseClick):
    screen.fill(green)
    text = font1.render("The Adventure!",True,blue)
    screen.blit(text,(200,100))
    startRect = pygame.Rect(200,200,195,50)
    pygame.draw.rect(screen,blue,startRect)
    text = font1.render("Click To Start!",True,red)
    screen.blit(text,startRect)
    mousePos = pygame.mouse.get_pos()
    gameStarted =False
    if( mouseClick and startRect.collidepoint(mousePos)):
        gameStarted = True
    pygame.display.update()
    return gameStarted
    

         
class Player:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,50,50)
        self.currentSpriteSheet = loadSpriteSheet("Images/player_walk_down.png",8, self.rect.width,self.rect.height)
        self.currentSprite = loadSpriteSheet("Images/player_walk_down.png",8, self.rect.width,self.rect.height)[0]
        self.spriteCounter = 0
        self.spaceTimer =0
        self.prevPos = "down"
        self.spacePressed =False
        self.allEnemiesDead =False
        self.health =110
        self.up =False
        self.down = False
        self.left =False
        self.right =False
        self.currentLevel=1
        self.won= False
        self.maxLevel=3
        self.winningTimer =0
        self.wallCollision=False
        self.dead=False
    def update(self,levelMap,gameStarted):
        self.checkCollision(levelMap)
        if(self.spacePressed):
            levelMap.up=False
            levelMap.down=False
            levelMap.left = False
            levelMap.right = False
        if(self.health <=0):
            self.dead =True

    def render(self,up,down,left,right,space):
        ticksPerFrame=3
        self.up=up
        self.down = down
        self.left =left
        self.right=right
        if(self.dead):
            txt =font1.render("You Lost! Restart The Program!",True,blue)
            pygame.mixer.music.stop()
            screen.fill(white)
            screen.blit(txt, (screenSize[0]/2-200, screenSize[1]/2-50))
            return "dead"
        if(initCounter/FPS<7):
            initText = font1.render("Kill the Enemies, Find the Door, Clear the Level!",True,white)
            screen.blit(initText, (player.rect.x-screenSize[0]/2, player.rect.y-180))
        if(self.won):
            self.winningSequence()
        if(up and not self.spacePressed):
            self.spriteCounter+=1
            self.prevPos="up"
            self.currentSpriteSheet =loadSpriteSheet("Images/player_walk_up.png",9, self.rect.width,self.rect.height)
            runTime =len(self.currentSpriteSheet)*ticksPerFrame #four ticks per frame
            if(self.spriteCounter>=runTime):
                self.spriteCounter = 0
            self.currentSprite = self.currentSpriteSheet[int(self.spriteCounter/ticksPerFrame)]
        if(down and not self.spacePressed):
            self.spriteCounter+=1
            self.prevPos="down"
            self.currentSpriteSheet =loadSpriteSheet("Images/player_walk_down.png",8, self.rect.width,self.rect.height)
            runTime =len(self.currentSpriteSheet)*ticksPerFrame #four ticks per frame
            if(self.spriteCounter>=runTime):
                self.spriteCounter = 0
            self.currentSprite = self.currentSpriteSheet[int(self.spriteCounter/ticksPerFrame)]
        if(left and not self.spacePressed):
            self.spriteCounter+=1
            self.prevPos ="left"
            self.currentSpriteSheet =loadSpriteSheet("Images/player_walk_left.png",5, self.rect.width,self.rect.height)
            runTime =len(self.currentSpriteSheet)*ticksPerFrame #four ticks per frame
            if(self.spriteCounter>=runTime):
                self.spriteCounter = 0
            self.currentSprite = self.currentSpriteSheet[int(self.spriteCounter/ticksPerFrame)]
        if(right and not self.spacePressed):
            self.spriteCounter+=1
            self.prevPos="right"
            self.currentSpriteSheet =loadSpriteSheet("Images/player_walk_right.png",5, self.rect.width,self.rect.height)
            runTime =len(self.currentSpriteSheet)*ticksPerFrame #four ticks per frame
            if(self.spriteCounter>=runTime):
                self.spriteCounter = 0
            self.currentSprite = self.currentSpriteSheet[int(self.spriteCounter/ticksPerFrame)]
        if(self.spacePressed):      
            sTicksPerFrame =2
            addedWidth =20
            addedHeight =20
            if(self.spaceTimer ==0):
                self.spriteCounter =0
            if(self.spaceTimer ==len(self.currentSpriteSheet)*sTicksPerFrame):
                self.spaceTimer =0
                self.spacePressed =False
            self.spaceTimer +=1

            if(self.prevPos == "up"):
                self.spriteCounter+=1
                self.currentSpriteSheet =loadSpriteSheet("Images/player_attack_up.png",8, self.rect.width+addedWidth,self.rect.height+addedHeight)
                runTime =len(self.currentSpriteSheet)*sTicksPerFrame #four ticks per frame
                if(self.spriteCounter>=runTime):
                    self.spriteCounter = 0
                self.currentSprite = self.currentSpriteSheet[int(self.spriteCounter/sTicksPerFrame)]
            if(self.prevPos == "down"):
                self.spriteCounter+=1
                self.currentSpriteSheet =loadSpriteSheet("Images/player_attack_down.png",8, self.rect.width+addedWidth,self.rect.height+addedHeight)
                runTime =len(self.currentSpriteSheet)*sTicksPerFrame #four ticks per frame
                if(self.spriteCounter>=runTime):
                    self.spriteCounter = 0
                self.currentSprite = self.currentSpriteSheet[int(self.spriteCounter/sTicksPerFrame)]
            if(self.prevPos == "left"):
                self.spriteCounter+=1
                self.currentSpriteSheet =loadSpriteSheet("Images/player_attack_left1.png",7, self.rect.width+addedWidth,self.rect.height+addedHeight+15)
                runTime =len(self.currentSpriteSheet)*sTicksPerFrame #four ticks per frame
                if(self.spriteCounter>=runTime):
                    self.spriteCounter = 0
                self.currentSprite = self.currentSpriteSheet[int(self.spriteCounter/sTicksPerFrame)]
            if(self.prevPos == "right"):
                self.spriteCounter+=1
                self.currentSpriteSheet =loadSpriteSheet("Images/player_attack_right.png",8, self.rect.width+addedWidth,self.rect.height+addedHeight+15)
                runTime =len(self.currentSpriteSheet)*sTicksPerFrame#four ticks per frame
                if(self.spriteCounter>=runTime):
                    self.spriteCounter = 0
                self.currentSprite = self.currentSpriteSheet[int(self.spriteCounter/sTicksPerFrame)]
        if(not right and not left and not up and not down and not self.spacePressed):
            if(self.prevPos == "up"):
                self.currentSprite = loadSpriteSheet("Images/player_standing_up.png",1,self.rect.width-25,self.rect.height)[0]
            elif(self.prevPos =="down"):
                self.currentSprite = loadSpriteSheet("Images/player_standing_down.png",1,self.rect.width-15,self.rect.height)[0]
            elif(self.prevPos =="left"):
                self.currentSprite = loadSpriteSheet("Images/player_standing_left.png",1,self.rect.width-15,self.rect.height)[0]

            elif(self.prevPos == "right"):
                self.currentSprite = loadSpriteSheet("Images/player_standing_right.png",1,self.rect.width-15,self.rect.height)[0]

        screen.blit(self.currentSprite,self.rect)
        self.displayHealth()
    def displayHealth(self):
        text = font.render(str(int(self.health)),True,green)
        screen.blit(text,(player.rect.x, player.rect.y-50))
    def winningSequence(self):
        if(self.winningTimer ==-5):
            #unimplemented sound
            pygame.mixer.music.stop()
            pygame.mixer.music.load("win.mp3")
            pygame.mixer.music.play(10)
            
        self.winningTimer+=1
        font= pygame.font.SysFont("comicsansms",120)        
        text = font.render("YOU WON!",True,pygame.Color(randint(0,255),randint(0,255),randint(0,255)))
        screen.blit(text, (player.rect.x-screenSize[0]/2, player.rect.y-180))
    def checkCollision(self,levelMap):
        if(self.rect.colliderect(levelMap.endOfLevelRect) and self.allEnemiesDead):
            self.currentLevel+=1
            playerCompleted= True
            loadLevel(self.currentLevel)
        self.wallCollision=False       
        for tile in levelMap.collisionRectList:
            if(self.rect.colliderect(tile)):
                self.wallCollision=True
                if(self.up):
                    levelMap.ypos-=4
                    levelMap.endOfLevelRect.y-=4
                    for tile in levelMap.collisionRectList:
                        tile.y-=4
                if(self.down):
                    levelMap.ypos+=4
                    levelMap.endOfLevelRect.y+=4
                    for tile in levelMap.collisionRectList:
                        tile.y+=4
                if(self.left):
                    levelMap.xpos-=4
                    levelMap.endOfLevelRect.x-=4
                    for tile in levelMap.collisionRectList:
                        tile.x-=4
                if(self.right):
                    levelMap.xpos+=4
                    levelMap.endOfLevelRect.x+=4
                    for tile in levelMap.collisionRectList:
                        tile.x+=4

                



class Enemy:
    def __init__(self,x,y,health,width=80,height=80):
        self.rect = pygame.Rect(x,y, 50,80)
        self.startWidth = width
        self.health = health
        self.isDead =False
        self.prevPos = "down"
        self.spriteCounter= 0
        self.wallCollision =False
        self.up = False
        self.down = False
        self.left = False
        self.right=  False
        self.currentSprite = loadSpriteSheet("Images/enemy_walk_down.png",7,width,height)[0]
        self.walkLeftSpriteSheet = loadSpriteSheet("Images/enemy_walk_right.png",7,width,height)
        self.walkRightSpriteSheet = loadSpriteSheet("Images/enemy_walk_left.png",7,width,height)
        self.walkUpSpriteSheet = loadSpriteSheet("Images/enemy_walk_down.png",7,width,height)
        self.walkDownSpriteSheet = loadSpriteSheet("Images/enemy_walk_up.png",7,width,height)#TODO FIX DIRECTION UP/DOWN
    def update(self,levelMap):
        if(self.health<=0):
            self.isDead =True
            self.rect.x = -100000
        if(not self.isDead):
            if(levelMap.up and levelMap.cameraUp and not player.wallCollision):
                self.rect.y+=4
            elif(levelMap.down and levelMap.cameraDown and not player.wallCollision):
                self.rect.y-=4
            elif(levelMap.left and levelMap.cameraLeft and not player.wallCollision):
                self.rect.x+=4
            elif(levelMap.right and levelMap.cameraRight and not player.wallCollision):
                self.rect.x-=4
            if(player.rect.x>self.rect.x):
                self.prevPos ="left"
                if(not self.left):
                    self.spriteCounter =0
                self.left =True
                self.right = False
                self.up = False
                self.down= False
                self.rect.x+=2
            elif(player.rect.x<self.rect.x):
                self.prevPos = "right"
                if(not self.right):
                    self.spriteCounter =0
                self.right = True
                self.left = False
                self.down = False
                self.rect.x-=2
            elif(player.rect.y>self.rect.y):
                self.prevPos="up"
                if(not self.up):
                    self.spriteCounter =0
                self.up = True
                self.down = False
                self.left = False
                self.right =False
                self.rect.y+=2
            elif(player.rect.y<self.rect.y):
                self.prevPos="down"
                if(not self.down):
                    self.spriteCounter = 0
                self.down=True
                self.up = False
                self.left=False
                self.right =False
                self.rect.y-=2
            if(self.checkCollision(player)and not player.spacePressed):
                player.health -=1 
                self.kickBack()
            elif(self.checkCollision(player)and player.spacePressed):
                self.health -=4
                self.kickBack()
            self.checkWallCollision(levelMap)

    def kickBack(self):
        kickBack = 50
        if(not self.wallCollision):
            if(self.prevPos == "up"):
                self.rect.y -=kickBack
                movedToBlockedSpace = False
                for tile in levelMap.collisionRectList:
                    if(self.rect.colliderect(tile)):
                        movedToBlockedSpace = True
                if(movedToBlockedSpace):
                    self.rect.y+=kickBack
            elif(self.prevPos == "down"):
                self.rect.y+=kickBack
                movedToBlockedSpace = False
                for tile in levelMap.collisionRectList:
                    if(self.rect.colliderect(tile)):
                        movedToBlockedSpace = True
                if(movedToBlockedSpace):
                    self.rect.y-=kickBack
            if(self.prevPos =="left"):
                self.rect.x -=kickBack
                movedToBlockedSpace = False
                for tile in levelMap.collisionRectList:
                    if(self.rect.colliderect(tile)):
                        movedToBlockedSpace = True
                if(movedToBlockedSpace):
                    self.rect.x+=kickBack
            elif(self.prevPos =="right"):
                self.rect.x +=kickBack
                movedToBlockedSpace = False
                for tile in levelMap.collisionRectList:
                    if(self.rect.colliderect(tile)):
                        movedToBlockedSpace = True
                if(movedToBlockedSpace):
                    self.rect.x-=kickBack
    def render(self):
        if(not self.isDead):
            text = font.render(str(int(self.health)),True,red)
            framesPerSec =2
            if(self.up):
                self.spriteCounter+=1
                if(self.spriteCounter> (framesPerSec*len(self.walkUpSpriteSheet))+framesPerSec-1):
                    self.spriteCounter =0
                self.currentSprite = self.walkUpSpriteSheet[int(self.spriteCounter/framesPerSec)-1]
            if(self.down):
                self.spriteCounter+=1
                if(self.spriteCounter> (framesPerSec*len(self.walkDownSpriteSheet))+framesPerSec-1):
                    self.spriteCounter =0
                self.currentSprite = self.walkDownSpriteSheet[int(self.spriteCounter/framesPerSec)-1]
            if(self.left):
                self.spriteCounter+=1
                if(self.spriteCounter> (framesPerSec*len(self.walkLeftSpriteSheet))+framesPerSec-1):
                    self.spriteCounter =0
                self.currentSprite = self.walkLeftSpriteSheet[int(self.spriteCounter/framesPerSec)-1]
            if(self.right):
                self.spriteCounter+=1
                if(self.spriteCounter> (framesPerSec*len(self.walkRightSpriteSheet))+framesPerSec-1):
                    self.spriteCounter =0
                self.currentSprite = self.walkRightSpriteSheet[int(self.spriteCounter/framesPerSec)-1]
            screen.blit(text,(self.rect.x, self.rect.y-50))
            screen.blit(self.currentSprite,self.rect)
    def checkCollision(self,rect):
        if(self.rect.colliderect(rect)):
            return True
    def checkWallCollision(self,levelMap):
        for tile in levelMap.collisionRectList:
            if(self.rect.colliderect(tile)):
                if(self.up):
                    self.rect.y-=2
   
                if(self.down):
                    self.rect.y+=2

                if(self.left):
                    self.rect.x-=2

                if(self.right):
                    self.rect.x+=2


class Map:
    tileSize = (50,50)
    maxBoundX= 0
    maxBoundY = 0
    collisionRectList= list()
    xpos =0
    ypos=0
    endOfLevelRect = pygame.Rect(-50,-50,50,50)
    memMap =None
    leftBoundHit = False
    rightBoundHit =False
    topBoundHit = False
    bottomBoundHit= False
    cameraUp=False
    cameraDown=False
    cameraLeft =False
    cameraRight=False
    def __init__(self, filename):

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.maxBoundX =0
        self.maxBoundY = 0
        self.collisionRectList = list()
        self.endOfLevelRect = pygame.Rect(-50,-50,50,50)
        self.memMap = self.readMap(filename)
        self.xpos=0
        self.ypos=0
        self.leftBoundHit =False
        self.rightBoundHit =False
        self.topBoundHit = False
        self.bottomBoundHit =False
        self.cameraUp=False
        self.cameraDown=False
        self.cameraLeft=False
        self.cameraRight=False

    def readMap(self,filename):
        self.collisionRectList = list()
        maxBoundX=0
        maxBoundY=0
        
        content = open(filename, 'r')
        fileLines = content.readlines()
        returnMap = list()     
        charToImgMap = dict()
        charToImgMap["X"]= pygame.transform.scale(pygame.image.load("Images/stonetile.png").convert_alpha(),self.tileSize)
        charToImgMap["_"]= pygame.transform.scale(pygame.image.load("Images/grasstile.jpg").convert_alpha(),self.tileSize)
        charToImgMap["K"]= pygame.transform.scale(pygame.image.load("Images/trap_door.png").convert_alpha(),self.tileSize)
        charToImgMap["W"]= pygame.transform.scale(pygame.image.load("Images/watertile.png").convert_alpha(),self.tileSize)
        charToImgMap["S"]= pygame.transform.scale(pygame.image.load("Images/sandtile.jpg").convert_alpha(),self.tileSize)        

        for i in range(len(fileLines)):
            returnMap.append(list(fileLines[i]))
            line = list(fileLines[i])
            for j in range(len(line)):                
                if(line[j]!= '\n'):
                    lineChar = line[j]
                    
                    if(line[j]=='X'or line[j]=='W'):
                        self.collisionRectList.append(pygame.Rect(j*self.tileSize[0],i*self.tileSize[1],self.tileSize[0],self.tileSize[1]-5))
                    if(line[j]=='E'):
                        lineChar ='_'
                        enemyList.append(Enemy(j*self.tileSize[0],i*self.tileSize[1], 10))
                    if(line[j]=='e'):
                        lineChar = 'S'
                        enemyList.append(Enemy(j*self.tileSize[0],i*self.tileSize[1], 10))

                    if(line[j]== 'B'):
                        lineChar ='_'
                        enemyList.append(Enemy(j*self.tileSize[0],i*self.tileSize[1], 200,200,200))
                    if(line[j]=='P'):
                        lineChar ='_'
                        self.xpos -= j*self.tileSize[0]-screenSize[0]
                        self.ypos -=i*self.tileSize[1]-screenSize[1]
                    if(line[j] =='K'):
                        self.endOfLevelRect = pygame.Rect(j*self.tileSize[0],i*self.tileSize[1],self.tileSize[0],self.tileSize[1])
                        
                    returnMap[i][j] = charToImgMap[lineChar]

        mapRead = True        
        return returnMap  
    def displayMap(self):
        startx = self.xpos
        starty = self.ypos

        for i in range(len(self.memMap)):
            for j in range(len(self.memMap[i])):
                if(self.memMap[i][j]!= '\n'):
                    if(j>self.maxBoundX):
                        self.maxBoundX = j
                    if(i>self.maxBoundY):
                        self.maxBoundY = i
                    screen.blit(self.memMap[i][j],(startx,starty))
                    startx+=self.tileSize[0]
            startx = self.xpos
            starty+=self.tileSize[1]
    def move(self):
        self.checkBounds()
        self.cameraUp=False
        self.cameraDown=False
        self.cameraLeft =False
        self.cameraRight =False
        if(self.up == True and not self.topBoundHit):
            if not self.bottomBoundHit and player.rect.y> screenSize[1]/2:
                player.rect.y-=4
            else:
                self.cameraUp=True
                player.prevPos = "up"
                self.ypos +=4
                self.endOfLevelRect.y+=4
                for tile in self.collisionRectList:
                    tile.y+=4
        elif(self.up and self.topBoundHit):
            player.rect.y-=4
        if(self.down == True and not self.bottomBoundHit):
            if not self.topBoundHit and player.rect.y<screenSize[1]/2:
                player.rect.y+=4
            else:
                self.cameraDown=True
                player.prevPos = "down"
                self.ypos -=4
                self.endOfLevelRect.y-=4
                for tile in self.collisionRectList:
                    tile.y-=4
        elif(self.down and self.bottomBoundHit):
            player.rect.y+=4
        if(self.left == True and not self.leftBoundHit):
            if not self.rightBoundHit and player.rect.x > screenSize[0]/2:
                player.rect.x-=4
            else:
                self.cameraLeft=True
                player.prevPos ="left"
                self.xpos +=4
                self.endOfLevelRect.x+=4
                for tile in self.collisionRectList:
                    tile.x+=4
        elif(self.left == True and self.leftBoundHit):
            player.rect.x-=4
            
        if(self.right == True and not self.rightBoundHit):
            if not self.leftBoundHit and player.rect.x < screenSize[0]/2:
                player.rect.x+=4
            else:
                self.cameraRight=True
                player.prevPos= "right"
                self.xpos-=4
                self.endOfLevelRect.x-=4
                for tile in self.collisionRectList:
                    tile.x-=4
        elif(self.right== True and self.rightBoundHit):
            player.rect.x+=4
                    

    def checkBounds(self):
        self.leftBoundHit=False
        self.rightBoundHit=False
        self.topBoundHit =False
        self.bottomBoundHit=False
        if(self.xpos>=0):
            self.leftBoundHit = True
        elif(self.xpos<=-1*self.maxBoundX*self.tileSize[0]+(screenSize[0])):
            self.rightBoundHit =True
        if(self.ypos>=0):
            self.topBoundHit =True
        elif(self.ypos<=-1*self.maxBoundY*self.tileSize[1]+screenSize[1]):
            self.bottomBoundHit =True
                           

#load map and characters
levelMap =loadLevel(1)
player = Player(screenSize[0]/2,screenSize[1]/2)
    
def update(levelMap,gameStarted):   #contains game logic changes
    gameStarted =player.update(levelMap,gameStarted)
    levelMap.move()

    player.allEnemiesDead =True
    for enemy in enemyList:
        if enemy.isDead ==False:
            player.allEnemiesDead = False
            enemy.update(levelMap)

        
def render(levelMap):   #displays elements to screen
    levelMap.displayMap()
    d =player.render(levelMap.up,levelMap.down,levelMap.left, levelMap.right, False)
    if (not d =="dead"):
            
        for enemy in enemyList:
            enemy.render()
    pygame.display.update()

while(running):
    mouseClick =False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                levelMap.up = True
                levelMap.down = False
                levelMap.left =False
                levelMap.right = False
            elif event.key == K_DOWN:
                levelMap.up = False
                levelMap.down = True
                levelMap.left =False
                levelMap.right = False
            elif event.key == K_LEFT:
                levelMap.up = False
                levelMap.down = False
                levelMap.left =True
                levelMap.right = False
            elif  event.key == K_RIGHT:
                levelMap.up = False
                levelMap.down = False
                levelMap.left =False
                levelMap.right = True
            elif event.key == K_SPACE:
                player.spacePressed = True
        elif event.type == KEYUP:
            if event.key == K_UP:
                levelMap.up = False
                player.spriteCounter =0
            elif event.key == K_DOWN:
                levelMap.down = False
                player.spriteCounter =0
            elif event.key == K_LEFT:
                levelMap.left = False
                player.spriteCounter =0
            elif  event.key == K_RIGHT:
                levelMap.right = False
                player.spriteCounter =0
            elif event.key == K_SPACE:
                player.spriteCounter = 0
        elif event.type == MOUSEBUTTONDOWN:
            mouseClick =True
    
    if(not gameStarted):
        gameStarted =startScreen(mouseClick)
    else:
        update(levelMap,gameStarted)
        render(levelMap)
        initCounter+=1
    clock.tick(FPS)
