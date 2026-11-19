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