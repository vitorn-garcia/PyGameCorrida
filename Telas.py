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
