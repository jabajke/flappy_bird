import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

background_image = pygame.image.load('images/background.png')
bird_image = pygame.image.load('images/bird.png')
top_pipe_image = pygame.image.load('images/top_pipe.png')
bottom_pipe_image = pygame.image.load('images/bottom_pipe.png')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

py, sy, ay = HEIGHT // 2, 0, 0
player = pygame.Rect(WIDTH // 3, py, 50, 50)
state = 'start'
timer = 0
frame = 0
pipes = []
bg_list = [pygame.Rect(0, 0, 288, 600)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    key = pygame.key.get_pressed()
    click = key[pygame.K_SPACE]

    if timer > 0:
        timer -= 1
    frame = (frame + 0.2) % 4

    for i in range(len(bg_list) - 1, -1, -1):
        bg = bg_list[i]
        bg.x -= 1
        if bg.right < 0:
            bg_list.remove(bg)
        if bg_list[-1].right < WIDTH:
            bg_list.append(pygame.Rect(bg_list[-1].right, 0, 288, 600))

    for i in range(len(pipes) - 1, -1, -1):
        pipe = pipes[i]
        pipe.x -= 3

        if pipe.right < 0:
            pipes.remove(pipe)

    if state == 'start':
        if click and timer == 0:
            state = 'play'
        py += (HEIGHT // 2 - py) * 0.1
        player.y = py
    elif state == 'play':
        if click:
            ay = -2
        else:
            ay = 0
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        if len(pipes) == 0 or pipes[-1].x < WIDTH - 200:
            pipes.append(pygame.Rect(WIDTH, 0, 50, 100))
            pipes.append(pygame.Rect(WIDTH, 400, 50, 200))

        if player.top < 0 or player.bottom > HEIGHT:
            state = 'fall'

        for pipe in pipes:
            if player.colliderect(pipe):
                state = 'fall'

    elif state == 'fall':
        sy, ay = 0, 0
        timer = 30
        pipes = []
        state = 'start'
    else:
        pass

    screen.fill(pygame.Color('black'))

    for bg in bg_list:
        screen.blit(background_image, bg)

    for pipe in pipes:
        pygame.draw.rect(screen, pygame.Color('green'), pipe)
    image = bird_image.subsurface(34 * int(frame), 0, 34, 24)
    screen.blit(image, player)
    pygame.display.update()
    clock.tick(FPS)
