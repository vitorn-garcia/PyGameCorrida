"""Cenários, animações e telas completas, com os dados da versão dos estudantes."""
import math
import pygame
from . import config_visual as config
from .adaptacao import adapta_corrida, nome_musica
from .layouts_v6 import menu_v6, resultado_v6, adiciona_botao
from .desenhos_v6 import (BG, WHITE, MUTED, MINT, text, box, music_bar,
                         equalizer, draw_world)


def cria_contexto(canvas):
    # Este dicionário pertence só ao complemento visual.
    return {"canvas": canvas, "mouse": (-1, -1), "timer": 0,
            "stage_index": 0, "player_count": 1, "buttons": [],
            "menu_scene": pygame.Surface((360, 380)), "menu_bikes": {},
            "demo": {"players": [{"x": .5, "distance": 0, "boost_time": 0}], "riders": [], "traffic": []}}


def desenha_menu(contexto, quantidade, fase, segundos):
    contexto["player_count"] = quantidade
    contexto["stage_index"] = fase
    contexto["timer"] = segundos
    contexto["buttons"] = []
    menu_v6(contexto)


def desenha_corrida(contexto, jogo, ordem, estado):
    superficie = contexto["canvas"]
    superficie.fill(BG)
    contexto["buttons"] = []
    corrida = adapta_corrida(jogo, ordem, estado)
    contexto["race"] = corrida
    fase = corrida["stage"]
    text(superficie, "ENTREGA NO GRAU", (25, 16), 19, WHITE, True)
    text(superficie, fase["name"], (25, 47), 12, fase["accent"], True)
    trecho = corrida["section"]
    equalizer(superficie, 318, 22, jogo["tempo"], trecho[3], fase["accent"], count=15, height=32)
    text(superficie, trecho[2], (441, 18), 17, WHITE, True)
    text(superficie, nome_musica(jogo["fase"]) + "  ·  ENERGIA " + str(int(trecho[3] * 100)) + "%", (442, 45), 10, MUTED)
    restante = max(0, math.ceil(config.DURATION - jogo["tempo"]))
    text(superficie, f"{restante // 60:02d}:{restante % 60:02d}", (1030, 10), 34, WHITE, True, "topright")
    adiciona_botao(contexto, (1050, 19, 125, 39), "PAUSAR", "pause")
    music_bar(superficie, (25, 80, 1150, 7), jogo["tempo"], trecho, fase["accent"])
    largura = config.WIDTH // jogo["quantidade"]
    for i in range(jogo["quantidade"]):
        visao = superficie.subsurface((i * largura, 102, largura, 620))
        draw_world(visao, corrida, corrida["players"][i], jogo["tempo"])
    if jogo["quantidade"] == 2:
        pygame.draw.rect(superficie, BG, (598, 102, 4, 620))
    controles = "SETAS OU WASD: PILOTAR   ·   F: FECHADA   ·   SHIFT / ESPAÇO: NITRO"
    if jogo["quantidade"] == 2:
        controles = "iFOOD: WASD / F / SHIFT ESQ   |   99: SETAS / ENTER / SHIFT DIR"
    text(superficie, controles, (25, 738), 10, MUTED, anchor="midleft")
    som = "SOM OFF" if jogo.get("mudo", False) else "SOM ON"
    text(superficie, som + " [M]     ·     PAUSAR [P / ESC]", (1175, 738), 11, MUTED, anchor="midright")
    if jogo.get("contagem", 0) > 0:
        for i in range(jogo["quantidade"]):
            cx = largura * (i + .5)
            box(superficie, (cx - 112, 285, 224, 171), (16, 25, 37), border=MINT)
            text(superficie, "PREPARE-SE", (cx, 308), 13, MINT, True, "midtop")
            text(superficie, str(math.ceil(jogo["contagem"])), (cx, 319), 88, WHITE, True, "midtop")
            text(superficie, "SEGURE PARA ACELERAR", (cx, 431), 10, MUTED, True, "midtop")
    elif jogo["tempo"] < 1:
        text(superficie, "VAI!", (config.WIDTH // 2, 260), 72, MINT, True, "center")
    if jogo["pausado"]:
        sombra = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
        sombra.fill((4, 9, 18, 190))
        superficie.blit(sombra, (0, 0))
        box(superficie, (375, 235, 450, 283), (20, 30, 44), border=(64, 83, 97))
        text(superficie, "PAUSA", (600, 264), 43, WHITE, True, "midtop")
        text(superficie, "A pista espera por você.", (600, 326), 16, MUTED, anchor="midtop")
        contexto["buttons"] = []
        adiciona_botao(contexto, (409, 373, 382, 51), "CONTINUAR  [P]", "pause", True)
        adiciona_botao(contexto, (409, 440, 382, 46), "VOLTAR AO MENU", "menu")


def desenha_resultado(contexto, jogo, ordem, estado):
    contexto["canvas"].fill(BG)
    contexto["buttons"] = []
    contexto["race"] = adapta_corrida(jogo, ordem, estado)
    contexto["audio"] = {"track_name": "BANDEIRADA / ORIGINAL"}
    resultado_v6(contexto)
