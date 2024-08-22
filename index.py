import pygame, pymunk
from sys import exit

width = 800
height = 800

def create_ball(space):
    body = pymunk.Body(1,100,body_type = pymunk.Body.DYNAMIC)
    body.position = (400, 0)
    shape = pymunk.Circle(body,80)
    space.add(body,shape)
    return shape

def draw_ball(balls):
    for ball in balls:
        pos_x = int(ball.body.position.x)
        pos_y = int(ball.body.position.y)
        pygame.draw.circle(screen, (0,0,0), (pos_x,pos_y),80)

pygame.init()

clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0,200)
balls = []
balls.append(create_ball(space))

screen = pygame.display.set_mode((width, height))


base_font = pygame.font.Font(None,30)
user_text = ''

input_rect = pygame.Rect(5,5,140,30)
color = pygame.Color("lightskyblue3")

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:

                user_text += event.unicode

    screen.fill("white")    

    draw_ball(balls)
    space.step(1/50)

    pygame.draw.rect(screen,color,input_rect, 2)

    text_surface = base_font.render(user_text,True,(0,0,0))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    input_rect.w = max(100, text_surface.get_width() + 10)


    pygame.display.update()
    clock.tick(120)