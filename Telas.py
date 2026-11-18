"""PARTE 3: desenho, perspectiva, menus, tela dividida, música e grau."""
import os
import pygame 
from Configuracoes import PASTA, MARCAS, FAIXAS, FASES, MUSICAS, CEUS, CHAO, CARGA_NITRO, DURACAO

def carrega_recursos():
    recursos = {}
    nomes = ['titulo','carro0', "carro1", "carro2"]
    for marca in MARCAS:
        nomes.append (marca)
        nomes.append (marca + '_grau')
