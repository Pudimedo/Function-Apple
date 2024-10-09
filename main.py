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

        self.lista_de_funcoes = []

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


regiao_de_funcoes = RegiaoDeFuncoes()

regiao_de_funcoes.criar_e_formatar_funcao('f(x) = 2x') #Fica guardado em regiao_de_funcoes.lista_de_funcoes


while True:
    
    #region events

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

    #endregion
    
    tela_principal.fill("white")

    pygame.display.update()

