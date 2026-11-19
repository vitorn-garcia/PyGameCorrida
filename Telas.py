"""PARTE 3: desenho, perspectiva, menus, tela dividida, música e grau."""
import os
import pygame 
from Configuracoes import PASTA, MARCAS, FAIXAS, FASES, MUSICAS, CEUS, CHAO, CARGA_NITRO, DURACAO

def carrega_recursos():
    recursos = {}
    nomes = ["titulo", "carro0", "carro1", "carro2"]
    for marca in MARCAS:
        nomes.append(marca)
        nomes.append(marca + "_grau")
    for nome in nomes:
        caminho = os.path.join(PASTA, "imagens", nome + ".png")
        recursos[nome] = pygame.image.load(caminho).convert_alpha()
    arquivo_fonte = os.path.join(PASTA, "imagens", "bold.ttf")
    recursos["pequena"] = pygame.font.Font(arquivo_fonte, 16)
    recursos["media"] = pygame.font.Font(arquivo_fonte, 22)
    recursos["grande"] = pygame.font.Font(arquivo_fonte, 36)
    return recursos

def escreve(tela, mensagem, x, y, fonte, cor):
    imagem = fonte.render(str(mensagem), True, cor)
    tela.blit(imagem, (x, y))


def projeta(x, distancia, observador, largura, altura):
    relativa = distancia - observador["distancia"]
    escala = 28 / (28 + relativa)
    largura_pista = min(largura * 1.35, 1250) * escala
    centro = largura / 2 - (observador["x"] - 0.5) * largura_pista * 0.46
    tela_x = centro + (x - 0.5) * largura_pista
    tela_y = altura * 0.29 + altura * 0.69 * escala
    return [tela_x, tela_y, largura_pista]

def desenha_pista(tela, observador, fase):
    largura = tela.get_width()
    altura = tela.get_height()
    horizonte = int(altura * 0.29)
    tela.fill(CEUS[fase])
    pygame.draw.rect(tela, CHAO[fase], (0, horizonte, largura, altura))
    pontos = []
    for x, distancia in [(0, 1200), (1, 1200), (1, 0), (0, 0)]:
        ponto = projeta(x, observador["distancia"] + distancia, observador, largura, altura)
        pontos.append((ponto[0], ponto[1]))
    pygame.draw.polygon(tela, (58, 60, 67), pontos)
    pygame.draw.lines(tela, (235, 224, 197), True, pontos, 3)
    deslocamento = observador["distancia"] % 16
    for i in range(24):
        distancia = i * 16 - deslocamento
        if distancia >= 0:
            for x in [0.25, 0.5, 0.75]:
                a = projeta(x, observador["distancia"] + distancia, observador, largura, altura)
                b = projeta(x, observador["distancia"] + distancia + 6, observador, largura, altura)
                pygame.draw.line(tela, (226, 222, 202), (a[0], a[1]), (b[0], b[1]), 2)