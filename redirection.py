import pygame, sys, random
import data.entities as e
import data.text as text
import numpy as np

def point_line_distance(point, start, end):
    """Calculate the minimum distance between a point and a line segment."""
    # Convert points to numpy arrays for vector operations
    point = np.array(point)
    start = np.array(start)
    end = np.array(end)

    # Vector from start to point and start to end
    line_vec = end - start
    point_vec = point - start

    # Calculate the projection scalar of point_vec onto line_vec
    line_len = np.linalg.norm(line_vec)
    line_unitvec = line_vec / line_len
    proj_length = np.dot(point_vec, line_unitvec)

    # Check if the projection length is within the line segment
    if proj_length < 0:
        # Before start point
        closest_point = start
    elif proj_length > line_len:
        # After end point
        closest_point = end
    else:
        # Projection point on the line
        closest_point = start + proj_length * line_unitvec

    # Distance from the point to the closest point on the line segment
    return np.linalg.norm(point - closest_point)

pygame.init()

clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("redirection")

font = pygame.font.Font('data/fonts/Pixeltype.ttf',50)
e.load_particle_images('data/images/particles')
e.set_global_colorkey((0, 0, 0))

particles = []
circle_effects = []
player_pos = [screen.get_width() // 2, screen.get_height() // 2]
player_color = (90, 210, 255)
bg_color = (13, 20, 33)

ball_speedx = 2
ball_speedy = 2

last_point = [0,0]
current_line = None

scroll = 0
game_score = 0
end_game = False
buttondown = False
last_speed_increase_time = start_time
player_radius = 10

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

    text_surface = font.render("Score: " + str(game_score), False, 'White')
    current_time = pygame.time.get_ticks()
    game_score = (current_time - start_time) // 1000

    if (current_time - last_speed_increase_time) > 10000:  
        ball_speedx *= 1.1  
        ball_speedy *= 1.1
        last_speed_increase_time = current_time


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
            if not buttondown:
                last_point = [mx, my]
            else:
                current_line = (last_point, [mx, my])
            buttondown = not buttondown

    if current_line:
        pygame.draw.line(screen, (255, 255, 255), current_line[0], current_line[1], 5)
        distance = point_line_distance(player_pos, current_line[0], current_line[1])
        if distance <= player_radius:
            print("Collision detected!")
            # Handle collision here (stop movement, bounce, etc.)
            ball_speedx, ball_speedy = -ball_speedx, -ball_speedy  # Example: simple bounce

    if buttondown:
        pygame.draw.line(screen, (90, 140, 170), last_point, [mx, my])

    screen.blit(text_surface, (10, 10))

    pygame.display.flip()
    clock.tick(60)

