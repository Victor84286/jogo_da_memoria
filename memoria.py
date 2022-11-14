"""
Jogo da memória.
"""
import time
import random

from dataclasses import dataclass

import pygame


@dataclass
class Cores:
    """
    Cores para a tela e objetos.

    Cada cor é uma tupla de três elementos, no padrão RGB.
    """
    branco = (255, 255, 255)
    preto = (0, 0, 0)
    azul = (0, 0, 255)


@dataclass
class Bordas:
    """Informações sobre as bordas da tela."""
    margem = 10
    espessura = 3


class Carta:
    """Dados das cartas."""
    virada = False
    largura = 40
    altura = 80

    margem = 50
    espaco_entre_cartas = 20

    def __init__(self, valor, indice):
        self.valor = valor
        self.posx, self.posy = self.define_coordenadas(indice)

    def define_coordenadas(self, indice, cartas_por_linha = 5):
        """
        Estabelece as coordenadas em x e em y de uma carta,
        baseado no seu índice.
        """
        linha = indice // cartas_por_linha
        coluna = indice % cartas_por_linha
        pos_y = self.margem + linha * (self.altura + self.espaco_entre_cartas)
        pos_x = self.margem + coluna * (self.largura + self.espaco_entre_cartas)

        return pos_x, pos_y

    def virar(self):
        """
        Vira uma carta, ou seja, muda o valor lógico da variável self.virada.
        """
        pass

    def foi_clicada(self, coord):
        """
        Retorna True caso a coordenada do clique seja sobre a carta.

        Parâmetros:
        coord -> uma lista no formato [pos_x, pos_y] com as coordenadas
            do mouse.

        Retorna: bool -> um sinal de que o clique do mouse ocorreu dentro
            da área definida pela carta.
        """
        if self.posx <= coord <= self.posx + self.largura:
            if self.posy <= coord <= self.posy + self.altura:
                return True

        return False


class Desenha:
    """Classe para renderização."""
    @staticmethod
    def bordas(tela, largura, altura):
        """
        Desenha as bordas da tela, usando como base a margem e espessura
        definidas na classe Borda.

        Parâmetros:
        tela -> A superfície de tela do jogo.
        largura -> Largura da borda.
        altura -> Altura da borda.
        """
        pygame.draw.rect(tela, Cores.branco, [0, 0] + [largura, Bordas.espessura]) # borda superior
        pygame.draw.rect(tela, Cores.branco, [0, 0] + [Bordas.espessura, altura]) # borda esquerda
        pygame.draw.rect(tela, Cores.branco, [0, altura - Bordas.espessura] + [largura, altura]) # borda inferior
        pygame.draw.rect(tela, Cores.branco, [largura - Bordas.espessura, 0] + [largura, altura]) # borda direita


    def cartas(self, tela, cartas):
        """Desenha as cartas na tela."""
        for carta in cartas:
            if carta.virada:
                self.carta_virada(tela, carta)
            else:
                self.carta_oculta(tela, carta)

    @staticmethod
    def carta_virada(tela, carta):
        """
        Desenha um texto centralizado na carta, representando uma carta virada.

        Parâmetros:
        tela -> A superfície de tela do jogo.
        carta -> Uma instância da classe Carta, com as coordenadas e
            dimensões do objeto.

        Retorna: None
        """
        pygame.draw.rect(tela, Cores.branco, [carta.posx, carta.posy])



    @staticmethod
    def carta_oculta(tela, carta):
        """
        Desenha um retângulo sólido, representando uma carta oculta.

        Parâmetros:
        tela -> A superfície de tela do jogo.
        carta -> Uma instância da classe Carta, com as coordenadas e
            dimensões do objeto.

        Retorna: None
        """

        pygame.draw.rect(tela, Cores.azul, [carta.posx, carta.posy] + [carta.posx + carta.largura, carta.posy + carta.altura])



class Tela:
    """ Informações sobre a tela do jogo."""
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.tela = self.cria_tela()
        self.cartas = self.cria_cartas()

    def cria_tela(self):
        """Cria a tela básica do jogo, e retorna a superfície do jogo."""
        return pygame.display.set_mode((self.largura, self.altura))

    def renderiza(self):
        """Renderiza a tela do jogo."""
        self.tela.fill(Cores.preto)

        Desenha.bordas(self.tela, self.largura, self.altura)
        Desenha().cartas(self.tela, self.cartas)

        pygame.display.update()

    @staticmethod
    def cria_cartas():
        """Cria os parâmetros das cartas na tela."""
        valores = list(range(20 // 2)) * 2
        random.shuffle(valores)
        return [Carta(valor, indice) for (indice, valor) in enumerate(valores)]


def trata_clique(coord, cartas):
    """
    Trata o clique do mouse e muda o estado de uma carta caso o mouse esteja
    sobre ela.
    """
    for carta in cartas:
        if carta.foi_clicada(coord):
            carta.virar()


def trata_eventos(cartas):
    """
    Trata dois tipos de eventos em cada quadro:
    - Caso o evento seja do tipo pygame.QUIT, retorna True;
    - Caso o evento seja do tipo pygame.MOUSEBUTTONUP, execute a função
        trata_clique, passando os parâmetros adequados.

    Parâmetros:
    cartas -> Lista com os objetos da classe Carta.

    Retorna: bool -> True para caso o evento seja de saída do jogo,
        False caso contrário.
    """
    for evento in pygame.event.get():
        # Sai do jogo caso o usuário feche o programa
        if evento.type == pygame.QUIT:
            return True

        if evento.type == pygame.MOUSEBUTTONUP:
            trata_clique(pygame.mouse.get_pos(), cartas)

    return False


def ocultar_cartas_se_necessario(cartas):
    """
    Verifica se, entre as cartas viradas, há cartas que não formam pares.
    Caso sejam encontradas cartas sem pares, aplica uma espera de 0.5s
    (time.sleep(0.5)), e depois vira essas cartas.

    Parâmetros:
    cartas -> Uma lista com objetos da classe Carta
    """



def inicio_jogo():
    """Inicializa a tela do jogo."""
    pygame.init()
    return Tela(380, 480)


def roda_loop(tela):
    """Roda o loop principal do jogo."""
    while True:
        ocultar_cartas_se_necessario(tela.cartas)
        if trata_eventos(tela.cartas):
            break
        tela.renderiza()
        pygame.time.Clock().tick(60)


def encerra_jogo():
    """Encerra o jogo."""
    print("Saindo do jogo!")
    pygame.quit()


def jogo():
    """
    Ponto de entrada do jogo Pong. Inicia o jogo, roda o loop e encerra o jogo.
    """
    roda_loop(inicio_jogo())
    encerra_jogo()


if __name__ == "__main__":
    jogo()