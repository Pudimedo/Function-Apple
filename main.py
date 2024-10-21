import pygame
from sys import exit

#region config

pygame.init()

tela_principal = pygame.display.set_mode((1100, 800))

#endregion

class TelaFuncional: #Tela em que ocorre o jogo de verdade, ou seja a tela onde as funções são desenhadas e etc.

    def __init__(self) -> None:

        pass
    
    @staticmethod

    def zoom_in() -> None:
        pass
    def zoom_out() -> None:
        pass
    
class RegiaoDeFuncoes: #Região onde o jogador escrevera as funções matematica.

    def __init__(self) -> None:

        self.contador_de_funcao = 0
        self.dict_de_regioes_de_escrever_funcao = {}
        self.lista_de_funcoes = []
        self.botao_de_adicionar_funcao = pygame.draw.rect(tela_principal, (128,18,255), (2, 2, 50, 50))
        self.botao_esta_pressionado = False
        
    @staticmethod

    def criar_regiao_de_funcao() -> None:
        pygame.draw.rect(tela_principal, (128,128,128), (0,0,300,800), 2)
        pygame.draw.rect(tela_principal, (128,18,255), (2, 2, 50, 50))

    def criar_e_formatar_funcao(self, funcao : str) -> None:

        funcao_separada = funcao.split('=')
        

        parametro = funcao_separada[0][funcao_separada[0].rfind('(') + 1]
        funcao_formatada = ''

        for i, caracter in enumerate(funcao_separada[1]):

            if caracter == parametro and funcao_separada[1][i - 1].isnumeric():
                funcao_formatada += '*'
            
            funcao_formatada += caracter
            

        self.lista_de_funcoes.append(funcao_formatada)
        
    def deletar_funcao(self, alvo : int) -> None:

        self.lista_de_funcoes.pop(alvo)

    def update(self):
        self.mouse = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

        if self.botao_de_adicionar_funcao.collidepoint(self.mouse_pos) and self.mouse[0] and not self.botao_esta_pressionado:
            self.contador_de_funcao += 1
            self.dict_de_regioes_de_escrever_funcao[str(self.contador_de_funcao)] = pygame.draw.rect(tela_principal, (100, 100, 100), (self.dict_de_regioes_de_escrever_funcao[str(self.contador_de_funcao)], )) #acabar isso
            self.botao_esta_pressionado = True

        if not self.mouse[0]:
            self.botao_esta_pressionado = False 


regiao_de_funcoes = RegiaoDeFuncoes()

regiao_de_funcoes.criar_e_formatar_funcao('f(x) = 2x') #Fica guardado em regiao_de_funcoes.lista_de_funcoes


while True:
    tela_principal.fill("white")

    regiao_de_funcoes.criar_regiao_de_funcao()
    regiao_de_funcoes.update()
    
    #region events

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

    #endregion
    
    
    
    pygame.display.update()

