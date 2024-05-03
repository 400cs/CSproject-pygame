import pygame, sys, random
import data.entities as e

pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("redirection")

e.load_particle_images('data/images/particles')
e.set_global_colorkey((0, 0, 0))

particles = []
circle_effects = []
player_pos = [screen.get_width() // 2, screen.get_height() // 2]
player_color = (90, 210, 255)
bg_color = (13, 20, 33)

ball_speedx = 2
ball_speedy = 2


scroll = 0
end_game = False
buttondown = False

while True:
    mx, my = pygame.mouse.get_pos()

    player_pos[0] += ball_speedx
    player_pos[1] += ball_speedy

    if player_pos[0] > SCREEN_WIDTH or player_pos[0] < 0:
        ball_speedx = -ball_speedx
    if player_pos[1] > SCREEN_HEIGHT or player_pos[1] < 0:
        ball_speedy = -ball_speedy

    screen.fill(bg_color)
    particles.append(e.particle(player_pos, 'p', [random.randint(0, 20) / 40 - 0.25, random.randint(0, 10) / 15 - 1], 0.2, random.randint(0, 30) / 10, player_color))

    for i, particle in sorted(enumerate(particles), reverse=True):
        alive = particle.update(1)
        if not alive:
            particles.pop(i)
        else:
            particle.draw(screen, [0, scroll])


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            buttondown = not buttondown
            
            circle_effects.append([[mx, my + scroll], 4, [4, 0.2], [4, 0.3], (255, 255, 255)])

    pygame.display.flip()
    clock.tick(60)