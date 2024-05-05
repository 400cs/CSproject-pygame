import pygame, sys, random
import data.entities as e
import data.collision as collision
import math

pygame.init()

clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("redirection")

gui_display = pygame.Surface((275, 400))
gui_display.set_colorkey((0, 0, 0))

font = pygame.font.Font('data/fonts/Pixeltype.ttf',50)
e.load_particle_images('data/images/particles')
e.set_global_colorkey((0, 0, 0))

# sounds
bounce_s = pygame.mixer.Sound('data/sfx/jump.wav')
laser_charge_s = pygame.mixer.Sound('data/sfx/laser_charge.wav')
laser_explode_s = pygame.mixer.Sound('data/sfx/laser_explode.wav')
restart_s = pygame.mixer.Sound('data/sfx/collect.mp3')
death_s = pygame.mixer.Sound('data/sfx/roblox-death-sound-sound-effect.mp3')
bounce_s.set_volume(0.7)
laser_charge_s.set_volume(0.05)
restart_s.set_volume(0.7)
death_s.set_volume(0.5)

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
has_collide = False
last_speed_increase_time = start_time
player_radius = 10

particles = []
circle_effects = []
lasers = []
line_effects = []


while True:
    mx, my = pygame.mouse.get_pos()

    player_pos[0] += ball_speedx
    player_pos[1] += ball_speedy

    if player_pos[0] > SCREEN_WIDTH or player_pos[0] < 0 or player_pos[1] > SCREEN_HEIGHT or player_pos[1] < 0:
        if end_game == False:
            death_s.play()
            font.render('press R', False, 'White',)
        end_game = True


    screen.fill(bg_color)
    particles.append(e.particle(player_pos, 'p', [random.randint(0, 20) / 40 - 0.25, random.randint(0, 10) / 15 - 1], 0.2, random.randint(0, 30) / 10, player_color))

    if not end_game:
        text_surface = font.render("Score: " + str(game_score), False, 'White')

    current_time = pygame.time.get_ticks()
    game_score = (current_time - start_time) // 1000

    # ball speed scaling
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
            if event.key == K_r:
                if end_game:
                    restart_s.play()
                    lasers = []
                    game_score = 0
                    end_game = False
                    particles = []
                    last_point = [screen.get_width() // 2, screen.get_height()]
                    scroll = 0
                    player_pos = [screen.get_width() // 2, screen.get_height() // 2]
                    ball_speedx = 2
                    ball_speedy = 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not buttondown:
                last_point = [mx, my]
            buttondown = not buttondown
        if event.type == pygame.MOUSEBUTTONUP:
            current_line = (last_point, [mx, my])
            buttondown = not buttondown
            has_collide = False
        
    
    # Lasers
    if game_score > 10:
        if random.randint(1, 300 * (1 + len(lasers) * 2)) == 1:
            lasers.append([random.randint(0, screen.get_width()), random.randint(90, 150), 20])
    for i, laser in sorted(enumerate(lasers), reverse=True):
        left = laser[0] - laser[1] 
        if left < 0:
            left = 0
        right = laser[0] + laser[1] 
        if right > screen.get_width():
            right = screen.get_width()
        pygame.draw.line(screen, (190, 40, 100), (left, 0), (left, screen.get_height()))
        pygame.draw.line(screen, (190, 40, 100), (right, 0), (right, screen.get_height()))
        center_line = [[laser[0], 0], [laser[0], screen.get_height()]]
        if laser[2] % 12 == 0:
            laser_charge_s.play()
            line_effects.append([[[left, 0], [left, screen.get_height()]], center_line, (190, 40, 100), 20, 30])
            line_effects.append([[[right, 0], [right, screen.get_height()]], center_line, (190, 40, 100), 20, 30])
        laser[2] += 1
        if laser[2] > 180:
            lasers.pop(i)
            laser_explode_s.play()
            if (player_pos[0] > left) and (player_pos[0] < right):
                if player_pos[0] > laser[0]:
                    ball_speedx += 4
                    ball_speedy += 4
                else:
                    ball_speedy -= 4
                    ball_speedx -= 4
                for i in range(30):
                    a = random.randint(0, 359)
                    s = random.randint(20, 50) / 10
                    x_p = math.cos(math.radians(a)) * s
                    y_p = math.sin(math.radians(a)) * s
                    particles.append(e.particle(player_pos, 'p', [x_p, y_p], 0.1, random.randint(0, 20) / 10, (170, 170, 170)))
                    screen_shake = 8
            for i in range(500):
                if random.randint(1, 2) == 1:
                    pos_x = left
                    vel = [4 + random.randint(0, 20) / 10, random.randint(0, 10) / 10 - 3]
                else:
                    pos_x = right
                    vel = [-(4 + random.randint(0, 20) / 10), random.randint(0, 10) / 10 - 3]
                pos_y = random.randint(0, screen.get_height() + 30) + scroll - 30
                particles.append(e.particle([pos_x, pos_y], 'p', vel, 0.2, random.randint(0, 20) / 10, (160, 40, 80)))
    

    if not has_collide:
        if current_line:
            normal = collision.calculate_normal(current_line[0], current_line[1])
            pygame.draw.line(screen, (255, 255, 255), current_line[0], current_line[1], 5)
            pygame.draw.circle(screen, (255, 255, 255), current_line[0], 7, 2)
            pygame.draw.circle(screen, (255, 255, 255), current_line[1], 7, 2)
            distance = collision.point_line_distance(player_pos, current_line[0], current_line[1])
            if distance <= player_radius:
                bounce_s.play()
                ball_velocity = [ball_speedx, ball_speedy]
                reflected_velocity = collision.reflect(ball_velocity, normal)
                ball_speedx, ball_speedy = reflected_velocity[0], reflected_velocity[1]
                # remove line
                has_collide = True


    if buttondown:
        line_length = math.sqrt(((mx - last_point[0])**2 + (my - last_point[1])**2))
        MAX_LINE_LENGTH = 600
        # if line_length > MAX_LINE_LENGTH:
        #     max_point = clamp_line(last_point, [mx, my], MAX_LINE_LENGTH)
        #     print(max_point)
        #     pygame.draw.line(screen, (90, 140, 170), last_point, max_point)
        # else:
        pygame.draw.line(screen, (90, 140, 170), last_point, [mx, my])

    screen.blit(text_surface, (10, 10))

    pygame.display.flip()
    clock.tick(60)