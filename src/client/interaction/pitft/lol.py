import pygame, sys, random, pygbutton
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 320 # size of window's width in pixels
WINDOWHEIGHT = 300 # size of windows' height in pixels


#             R    G    B
GRAY      = (201, 204, 204)
DARKRED   = (150,  0 ,  0 )
BLACK     = ( 0,   0 ,  0 )
WHITE     = (255, 255, 255)

BGCOLOR = GRAY # background color on the screen

ENEMY_IMG = pygame.image.load('light_bulb_on.png')
STARTY = -15


AVATAR_IMG = pygame.image.load('light_bulb_on.png')

class Avatar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = AVATAR_IMG
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
    def getLocation(self):
        return pygame.mouse.get_pos()
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self._image = ENEMY_IMG
        self.rect = self._image.get_rect()
        self._x = x
        self._y = y
        self._lastx = self._x
        self._lasty = self._y
        
    def getLocation(self):
        return self._x, self._y
    
    def moveDown(self):
        self._lasty = self._y
        self._y += 3
        self.rect.move_ip(self._lastx - self.rect.centerx, self._lasty - self.rect.centery)
    
def hit(self, group):
    return pygame.sprite.spritecollideany(self, group)

def main():
    global FPSCLOCK, DISPLAYSURF
    
    pygame.init()
    

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    pygame.display.set_caption('AvoiderGame')
    GAMEOVER = False
    GAMESTART = False
    avatar = Avatar()
    enemyGroup = pygame.sprite.Group()
    
    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    textSurfaceObj = fontObj.render('GAME OVER', False, WHITE )
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (200, 150)
    
    gameStartObj = fontObj.render('AVOIDER GAME', False, WHITE )
    gameStartRectObj = gameStartObj.get_rect()
    gameStartRectObj.center = (200, 150)
    
    restartButton = pygbutton.PygButton((150, 180, 70, 30), 'Restart')
    startButton = pygbutton.PygButton((150, 180, 70, 30), 'Start')
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if 'click' in restartButton.handleEvent(event):
                GAMEOVER = False
                enemyGroup = pygame.sprite.Group()
            if 'click' in startButton.handleEvent(event):
                GAMESTART = True
                enemyGroup = pygame.sprite.Group()
        if not GAMEOVER and GAMESTART:
            DISPLAYSURF.fill(BGCOLOR)
            if random.random() < 0.1:
                randomX = random.randrange(0, WINDOWWIDTH)
                enemy = Enemy(randomX, STARTY)
                enemyGroup.add(enemy)
            for e in enemyGroup:
                e.moveDown()
                DISPLAYSURF.blit(e._image, e.getLocation())
            avatar.rect.move_ip(pygame.mouse.get_pos()[0]- avatar.rect.centerx, pygame.mouse.get_pos()[1]- avatar.rect.centery)
            DISPLAYSURF.blit(avatar.image, avatar.getLocation())
            if hit(avatar, enemyGroup):
                GAMEOVER = True
        if GAMEOVER:
            DISPLAYSURF.fill(BLACK)
            DISPLAYSURF.blit(textSurfaceObj, textRectObj)
            restartButton.draw(DISPLAYSURF)
        if not GAMESTART:
            DISPLAYSURF.fill(BLACK)
            DISPLAYSURF.blit(gameStartObj, gameStartRectObj)
            startButton.draw(DISPLAYSURF)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        
    
    
if __name__ == '__main__':
    main()