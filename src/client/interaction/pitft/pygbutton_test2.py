import pygame, pygbutton, sys
from pygame.locals import *
import platform

FPS = 20
WINDOWWIDTH = 320
WINDOWHEIGHT = 240

WHITE       = (255, 255, 255)

BTN_BULB_ON     = 'light_bulb_on_80.png'
BTN_BULB_OFF    = 'light_bulb_off_80.png'
BTN_FORWARD     = 'forward_80.png'


def main():

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('PygButton Test 2')

    button00    = pygbutton.PygButton((0,   0, 80, 80), '-2')
    button01    = pygbutton.PygButton((0,  80, 80, 80), normal=BTN_BULB_OFF)
    button02    = pygbutton.PygButton((0, 160, 80, 80), normal=BTN_BULB_OFF)

    LIGHT_ON        = False

    #button10    = pygbutton.PygButton((80,   0, 80, 80), '1')
    #button11    = pygbutton.PygButton((80,  80, 80, 80), '2')
    #button12    = pygbutton.PygButton((80, 160, 80, 80), '3')

    #button20    = pygbutton.PygButton((160,   0, 80, 80), '1')
    #button21    = pygbutton.PygButton((160,  80, 80, 80), '2')
    #button22    = pygbutton.PygButton((160, 160, 80, 80), '3')

    #button30    = pygbutton.PygButton((240,   0, 80, 80), '1')
    #button31    = pygbutton.PygButton((240,  80, 80, 80), '2')
    button32    = pygbutton.PygButton((240, 160, 80, 80), normal=BTN_FORWARD)
    #buttonToggleVis = pygbutton.PygButton((50,  50, 200, 30), 'Toggle Button Visibility')

    #visMode = True

    while True: # main game loop

        #buttonHello.visible = visMode

        for event in pygame.event.get(): # event handling loop

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
                pygame.quit()
                sys.exit()

            #events = buttonToggleVis.handleEvent(event)
            #if 'click' in events:
            #    visMode = not visMode

            #button1.handleEvent(event)
            #button2.handleEvent(event)
            #button3.handleEvent(event)

            events = button00.handleEvent(event)
            if 'click' in events:
                button00.caption = str(int(button00.caption)+1)

            events = button01.handleEvent(event)
            if 'click' in events:
                if LIGHT_ON:
                    button01.setSurfaces(BTN_BULB_OFF)
                    LIGHT_ON = False
                else:
                    button01.setSurfaces(BTN_BULB_ON)
                    LIGHT_ON = True
                #button01._update()

            button02.handleEvent(event)

            #button10.handleEvent(event)
            #button11.handleEvent(event)
            #button12.handleEvent(event)

            #button20.handleEvent(event)
            #button21.handleEvent(event)
            #button22.handleEvent(event)

            #button30.handleEvent(event)
            #button31.handleEvent(event)
            button32.handleEvent(event)

        DISPLAYSURFACE.fill(WHITE)

        #buttonToggleVis.draw(DISPLAYSURFACE)
        button00.draw(DISPLAYSURFACE)
        button01.draw(DISPLAYSURFACE)
        button02.draw(DISPLAYSURFACE)

        #button10.draw(DISPLAYSURFACE)
        #button11.draw(DISPLAYSURFACE)
        #button12.draw(DISPLAYSURFACE)

        #button20.draw(DISPLAYSURFACE)
        #button21.draw(DISPLAYSURFACE)
        #button22.draw(DISPLAYSURFACE)

        #button30.draw(DISPLAYSURFACE)
        #button31.draw(DISPLAYSURFACE)
        button32.draw(DISPLAYSURFACE)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
