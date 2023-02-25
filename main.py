import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

py, sy, ay = HEIGHT // 2, 0, 0
player = pygame.Rect(WIDTH // 3, py, 50, 50)
state = 'start'
timer = 0

pipes = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    key = pygame.key.get_pressed()
    click = key[pygame.K_SPACE]

    if timer > 0:
        timer -= 1

    for pipe in pipes:
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
    for pipe in pipes:
        pygame.draw.rect(screen, pygame.Color('green'), pipe)
    pygame.draw.rect(screen, pygame.Color('yellow'), player)
    pygame.display.update()
    clock.tick(FPS)

