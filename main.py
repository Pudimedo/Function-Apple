import pygame
from sys import exit
import random

#region Classes

class Container:
    # Classe base para criar contêineres que servem como áreas na tela do Pygame

    def __init__(self, x_pos: int, y_pos: int, largura: int, altura: int, borda: int, cor: tuple, origem: tuple = (0,0)) -> None:
        # Inicializa o contêiner com posição, largura, altura, borda, cor, e uma origem opcional
        
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.largura = largura
        self.altura = altura
        self.borda = borda
        self.x_origem = origem[0]
        self.y_origem = origem[1]
        self.cor = cor
        self.container = pygame.Rect(self.x_pos, self.y_pos, self.largura, self.altura)
        self.containers_filhos = []  # Lista para armazenar contêineres filhos

    
    def desenhar_container(self) -> None:
        # Desenha o contêiner na tela com uma borda e cor especificada

        self.container = pygame.Rect(self.x_pos, self.y_pos, self.largura, self.altura) 
        pygame.draw.rect(tela_principal, self.cor, self.container, self.borda)

    def update(self) -> None:
        
        # Atualiza o contêiner e verifica se há botões ou filhos para gerenciar

        self.desenhar_container()

        # Adiciona o botão de adicionar filhos se ainda não houver nenhum filho
        if len(self.containers_filhos) == 0:
            self.containers_filhos.append(botao_de_adicionar_container_de_funcao)

        # Verifica o clique no botão, limitando a quantidade de filhos a 10
        elif len(self.containers_filhos) <= 9:
            botao_de_adicionar_container_de_funcao.checar_clique()

        # Atualiza a posição e a aparência de cada contêiner filho
        for indice, filho in enumerate(self.containers_filhos):
            filho.update()
            filho.index = indice
            filho.y_pos = indice * 70 + 1


class Botao(Container):
    # Subclasse de Container que representa um botão clicável

    def __init__(self, x_pos: int, y_pos: int, largura: int, altura: int, borda: int, cor: tuple, acao, origem: tuple = (0, 0)) -> None:
        # Inicializa o botão com uma ação que será executada ao clicar

        super().__init__(x_pos, y_pos, largura, altura, borda, cor, origem)
        self.acao = acao
        self.mouse_foi_pressionado = False

    def desenhar_container(self) -> None:
        # Desenha o símbolo de "+" para o botão, além de seu retângulo

        x, y = self.x_pos + self.largura // 2, self.y_pos + self.altura // 2
        pygame.draw.line(tela_principal, (0,0,0), (x - 35 // 2, y), (x + 35 // 2, y), 5)
        pygame.draw.line(tela_principal, (0,0,0), (x, y - 35 // 2), (x, y + 35 // 2), 5)

        return super().desenhar_container()

    def checar_clique(self):
        # Verifica se o botão foi clicado e executa a ação associada

        if self.container.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            if pygame.mouse.get_pressed()[0]:
                self.mouse_foi_pressionado = True
            elif self.mouse_foi_pressionado:
                self.acao()  # Executa a ação atribuída ao botão
                self.mouse_foi_pressionado = False
    
    def update(self) -> None:
        # Atualiza o botão (redesenha na tela)
        
        self.desenhar_container()


class ContainerDeFuncao(Container):
    # Classe para contêineres específicos que executam uma função quando interagem com o teclado e o mouse

    def __init__(self, x_pos: int, y_pos: int, largura: int, altura: int, borda: int, cor: tuple, index: int, origem: tuple = (0, 0)) -> None:
        # Inicializa o contêiner com um índice, cor e outras propriedades de contêiner

        super().__init__(x_pos, y_pos, largura, altura, borda, cor, origem)
        self.x_origem = self.x_pos - 70
        self.index = index
        self.mouse_foi_pressionado = False
        self.pode_escrever = False  # Define se o contêiner pode receber entrada de texto
        self.texto_padrao_de_funcao = 'y = '
        self.texto = ''
        
    def desenhar_container(self) -> None:
        # Desenha o contêiner com um botão de exclusão "X"

        self.y_origem = self.y_pos
        x, y = self.largura - 35, self.y_origem + 35

        # Desenha o botão de excluir com o "X"
        self.botao_de_excluir_container_de_funcao = pygame.draw.rect(tela_principal, (128,128,128), (self.largura - 70, self.y_pos, 70, 70))
        self.linha1 = pygame.draw.line(tela_principal, (0,0,0), (x - 35 // 2, y - 35 // 2), (x + 35 // 2, y + 35 // 2), 5)
        self.linha2 = pygame.draw.line(tela_principal, (0,0,0), (x + 35 // 2, y - 35 // 2), (x - 35 // 2, y + 35 // 2), 5)

        return super().desenhar_container()
    
    def escrever(self, evento) -> None:
        # Método chamado para lidar com a entrada de texto no contêiner

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]

            elif evento.key == pygame.K_RETURN:
                self.pode_escrever = False
                self.containers_filhos.pop()

            else:
                self.texto += evento.unicode
        

    def checar_clique(self, container: pygame.Rect) -> bool:
        # Verifica se um contêiner foi clicado

        if container.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.mouse_foi_pressionado = True
            elif self.mouse_foi_pressionado:
                self.mouse_foi_pressionado = False
                return True        

        return False
    
    def update(self) -> None:
        # Atualiza o contêiner, gerenciando cliques e filhos

        self.desenhar_container()
        
        # Verifica se o botão de excluir foi clicado para remover o contêiner
        if self.checar_clique(self.botao_de_excluir_container_de_funcao):
            self.pode_escrever = False
            self.containers_filhos = []
            container_de_funcoes.containers_filhos.pop(self.index)

        # Adiciona um contêiner filho se o contêiner principal for clicado
        elif self.checar_clique(self.container):
            if len(self.containers_filhos) == 0:
                self.containers_filhos.append(Container(self.x_pos, self.y_pos, self.largura - 70, self.altura, 2, (0, 150, 255)))
                self.pode_escrever = True

        # Remove o último filho se clicar fora do contêiner
        elif self.checar_clique(ContainerTela):
            self.pode_escrever = False
            if len(self.containers_filhos) > 0:
                self.containers_filhos.pop()

        # Atualiza cada filho na lista de contêineres filhos
        for filho in self.containers_filhos:
            filho.index = self.index
            filho.container = self.container
            filho.update()


class ContainerDeGrafico(Container):
    def __init__(self, x_pos: int, y_pos: int, largura: int, altura: int, borda: int, cor: tuple, origem: tuple = (0, 0)) -> None:
        super().__init__(x_pos, y_pos, largura, altura, borda, cor, origem)

        self.tamanho_da_tela_de_calculo = (30, 21)


        self.superficie_de_grafico = pygame.Surface((1000, 700))
        self.largura_da_superficie_de_grafico = self.superficie_de_grafico.get_width()
        self.altura_da_superficie_de_grafico = self.superficie_de_grafico.get_height()
        self.centro_da_superficie = (self.largura_da_superficie_de_grafico // 2, self.altura_da_superficie_de_grafico // 2)

        self.proporcao_da_tela = (self.largura_da_superficie_de_grafico // self.tamanho_da_tela_de_calculo[0])

        

    def desenhar_eixos(self) -> None:

        eixo_x = ((self.x_pos, self.altura/2), (self.x_pos + self.largura, self.altura/2))
        eixo_y = ((self.x_pos + self.largura / 2, self.y_pos), (self.x_pos + self.largura / 2, self.altura))


        for i, unidade_x in enumerate(range(0, self.largura, (self.largura_da_superficie_de_grafico // self.tamanho_da_tela_de_calculo[0]))):

            pygame.draw.line(tela_principal, (0,0,0), (6 + unidade_x + self.x_pos, self.centro_da_superficie[1] - 10), (6 + unidade_x + self.x_pos, self.centro_da_superficie[1] + 10))

            tela_principal.blit(font_grafico.render(str(int(i - self.tamanho_da_tela_de_calculo[0] // 2)), True, (0,0,0)), (unidade_x + self.x_pos - 2, self.centro_da_superficie[1] + 10))


        for i, unidade_y in enumerate(range(0, self.altura, (self.altura_da_superficie_de_grafico // self.tamanho_da_tela_de_calculo[1]))):

            pygame.draw.line(tela_principal, (0,0,0), (self.x_pos + self.centro_da_superficie[0] - 10 + 1, unidade_y - 12), (self.x_pos + self.centro_da_superficie[0] + 10 + 1, unidade_y - 12))

            if self.tamanho_da_tela_de_calculo[1] // 2 - i != 0:

                tela_principal.blit(font_grafico.render(str(int(self.tamanho_da_tela_de_calculo[1] // 2 - i)), True, (0,0,0)), (self.x_pos + self.centro_da_superficie[0] + 17, unidade_y + 15))


        pygame.draw.line(tela_principal, (0,0,0), eixo_x[0], eixo_x[1], 2)
        pygame.draw.line(tela_principal, (0,0,0), eixo_y[0], eixo_y[1], 2)



    def formatar_texto_de_funcao(self, texto: str) -> None:

        self.texto_formatado = ''

        for indice, caracter in enumerate(texto):

            if caracter.lower() == 'x' and texto[indice - 1].isnumeric() and indice != 0:
                self.texto_formatado += '*x'

            else:
                self.texto_formatado += caracter

        if '{' in self.texto_formatado:

            self.equacao = self.texto_formatado.split('{')[0]
        
        else:
            self.texto_formatado += ' {x}'
            self.equacao = self.texto_formatado.split('{')[0]


        

    def desenhar_grafico(self, texto: str) -> None:

        self.formatar_texto_de_funcao(texto) 
        if '}' in self.texto_formatado:
            self.segmento = self.texto_formatado.split('{')[1].removesuffix('}')
        
        else:
            return
            
        coordenadas = []

        for aux in range(self.largura_da_superficie_de_grafico):
            aux -= self.largura_da_superficie_de_grafico // 2            

            x = aux / self.proporcao_da_tela

            if eval(self.segmento):
                if '/' in self.equacao and x == 0:
                    pass
                else:
                    coordenadas.append((self.centro_da_superficie[0] + x * self.proporcao_da_tela, self.centro_da_superficie[1] - eval(self.equacao) * self.proporcao_da_tela))
        
        pygame.draw.lines(self.superficie_de_grafico, (255, 0, 0), False, coordenadas, 3)

        



    def update(self) -> None:

        self.superficie_de_grafico.fill('white')

        self.containers_filhos = container_de_funcoes.containers_filhos

        for funcao in self.containers_filhos:

            if isinstance(funcao, ContainerDeFuncao):
                try:
                    self.desenhar_grafico(funcao.texto)

                except:
                    pass

        tela_principal.blit(self.superficie_de_grafico, (self.x_pos + 1, self.y_pos + 1))

        self.desenhar_container()
        self.desenhar_eixos()

                
#endregion

#region Funções

def criar_container_filho():
    # Função para adicionar um novo ContainerDeFuncao como filho
    container_de_funcoes.containers_filhos.append(ContainerDeFuncao(0, 70, container_de_funcoes.largura, 70, 2, (0,0,0), 0))

#endregion

#region Configuração do Pygame

pygame.init()

# Configuração da tela principal
altura = 700
largura = 1400
tela_principal = pygame.display.set_mode((largura, altura))
ContainerTela = pygame.Rect(0, 0, largura, altura)
font_base = pygame.font.Font(None, 40)
font_grafico = pygame.font.Font(None, 20)

# Contêineres principais
container_de_funcoes = Container(0, 0, 400, altura, 2, (0,0,0), (200 - 35, 1))
container_de_grafico = ContainerDeGrafico(container_de_funcoes.largura - 2, 0, largura - container_de_funcoes.largura + 2, altura, 2, (0,0,0), (container_de_funcoes.largura + (largura - container_de_funcoes.largura) / 2, altura/2))
botao_de_adicionar_container_de_funcao = Botao(container_de_funcoes.x_origem, container_de_funcoes.y_origem, 70, 70, 2, (0,0,0), criar_container_filho)


#endregion


# Loop principal do jogo
while True:
    tela_principal.fill('white')  # Limpa a tela a cada quadro

    # Verifica eventos como fechar a janela e pressionar teclas
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Se um filho do ContainerDeFuncao existir e puder escrever ele permite a escrita mudando a variavel de texto do container
        for filho in container_de_funcoes.containers_filhos:
            if isinstance(filho, ContainerDeFuncao) and filho.pode_escrever:

                filho.escrever(evento)
                
    # Atualiza o texto do container
    for filho in container_de_funcoes.containers_filhos:
        if isinstance(filho, ContainerDeFuncao):

            superficie_de_texto = font_base.render(filho.texto_padrao_de_funcao + filho.texto, True, (0,0,0))
            tela_principal.blit(superficie_de_texto, (filho.container.left + 10, filho.container.centery - 18))
    
    
    # Atualiza e desenha contêineres na tela
    container_de_funcoes.update()
    container_de_grafico.update()
    pygame.display.update()