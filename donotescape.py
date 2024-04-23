import pygame, sys
pygame.init()

size = width, height = 1500, 1000
speed = [2, 2]
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.gif")
ballrect = ball.get_rect()

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
c = pygame.draw.circle(screen, white, player_pos, 5, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
    
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(black)

    pygame.draw.circle(screen, white, player_pos, 8, 0)
    
    screen.blit(ball, ballrect)
    pygame.display.flip()