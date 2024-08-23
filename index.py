import pygame
from sys import exit

width = 800
height = 800

def format_func(func : list) -> str:

    parameter = func[0][func[0].rfind('(') + 1]
    formated_func = '' #funcao formatada
    for i, letter in enumerate(func[1]):

        if letter == parameter and func[1][i - 1].isnumeric():
            formated_func += '*'
        
        formated_func += letter
    
    return formated_func

#region config

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))

base_font = pygame.font.Font(None,30)
user_text = ''
warning_text = ''
enter_pressed = False

input_rect = pygame.Rect(5,5,140,30)
color = pygame.Color("lightskyblue3")

#endregion

while True:
    
    #region events

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:

            if not enter_pressed:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]

                elif event.key == pygame.K_RETURN:
                    if user_text != '':
                        enter_pressed = True
                        warning_text = 'Clique R para reiniciar'

                else:
                    user_text += event.unicode

            elif event.key == pygame.K_r:
                user_text = ''
                warning_text = ''
                enter_pressed = False
    #endregion
    
    screen.fill("white")    

    pygame.draw.rect(screen,color,input_rect, 2)

    text_surface = base_font.render(user_text,True,(0,0,0))
    warning_surface = base_font.render(warning_text,True, (0,0,0))

    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    screen.blit(warning_surface, (input_rect.w + 10, input_rect.y + 5))

    input_rect.w = max(100, text_surface.get_width() + 10)


    pygame.display.update()