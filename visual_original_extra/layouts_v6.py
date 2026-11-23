"""Layouts visuais da V6. Os botões apenas devolvem ações ao iniciador."""
import math
import pygame
from .config_visual import WIDTH, HEIGHT, STAGES
from .desenhos_v6 import (BG, PANEL, WHITE, MUTED, MINT, text, box, button,
                         draw_world, bike_sprite, poster_text)


def adiciona_botao(contexto, rect, label, action, selected=False, accent=MINT):
    rect = pygame.Rect(rect)
    button(contexto['canvas'], rect, label, selected, accent,
           rect.collidepoint(contexto['mouse']))
    contexto['buttons'].append((rect, action))


def carro_demo(x, distancia, velocidade, cor):
    return {"x": x, "distance": distancia, "speed": velocidade,
            "color": cor, "kind": 0, "target_x": None}

def menu_v6(contexto):
    surface = contexto['canvas']
    cream, gold, asphalt = (245, 240, 220), (255, 203, 46), (24, 25, 27)
    gray = (160, 158, 146)
    surface.fill(asphalt)
    stage = STAGES[contexto['stage_index']]

    # A pista ocupa o fundo; a baixa resolução lembra os arcades de corrida.
    demo = contexto['demo']
    demo['stage'] = stage
    demo['players'][0]['distance'] = contexto['timer'] * 38
    demo['players'][0]['x'] = .5
    demo['riders'] = []
    demo['traffic'] = [carro_demo(lane, demo['players'][0]['distance'] + ((i * 48 - contexto['timer'] * 13) % 240) + 18,
                            90, color)
                    for i, lane, color in [(1, .125, (190, 94, 75)),
                                           (2, .875, (117, 154, 182)),
                                           (3, .375, (224, 194, 116)),
                                           (4, .625, (192, 193, 175))]]
    draw_world(contexto['menu_scene'], demo, demo['players'][0], contexto['timer'], hud=False)
    surface.blit(pygame.transform.scale(contexto['menu_scene'], (720, HEIGHT)), (480, 0))
    # Recorte diagonal, como uma pintura de carenagem, sem painéis flutuantes.
    pygame.draw.polygon(surface, (8, 9, 11), [(0, 0), (717, 0), (547, HEIGHT), (0, HEIGHT)])
    pygame.draw.polygon(surface, asphalt, [(0, 0), (704, 0), (534, HEIGHT), (0, HEIGHT)])
    pygame.draw.line(surface, gold, (704, 0), (534, HEIGHT), 3)
    # Três riscos discretos no asfalto e uma faixa de largada na borda.
    for i in range(3):
        x = 568 + i * 30
        pygame.draw.polygon(surface, (42, 43, 44), [(x, 20), (x + 13, 20), (x - 38, 245), (x - 51, 245)])
    for row in range(38):
        for col in range(2):
            if (row + col) % 2 == 0:
                pygame.draw.rect(surface, cream, (WIDTH - 18 + col * 9, row * 20, 9, 20))
            else:
                pygame.draw.rect(surface, (29, 30, 31), (WIDTH - 18 + col * 9, row * 20, 9, 20))

    # Título com a mesma linguagem dos carros e das motos do jogo.
    pygame.draw.rect(surface, (224, 63, 52), (64, 48, 289, 29))
    text(surface, "CORRIDA DE ENTREGADORES", (77, 54), 13, cream, True)
    poster_text(surface, "ENTREGA", (56, 94), 88, cream)
    poster_text(surface, "NO GRAU", (54, 183), 90, gold)
    text(surface, "iFood", (68, 299), 17, (248, 81, 75), True)
    text(surface, "x", (135, 301), 13, gray)
    text(surface, "99", (159, 299), 17, gold, True)

    # Um botão principal e seletores diretos. Os atalhos continuam iguais.
    start = pygame.Rect(64, 352, 427, 68)
    hovered = start.collidepoint(contexto['mouse'])
    points = [(start.x + 13, start.y), (start.right, start.y),
              (start.right - 13, start.bottom), (start.x, start.bottom)]
    pygame.draw.polygon(surface, (6, 7, 8), [(x + 5, y + 7) for x, y in points])
    pygame.draw.polygon(surface, (255, 220, 86) if hovered else gold, points)
    text(surface, "JOGAR", (88, 363), 32, asphalt, True)
    text(surface, "ENTER", (458, 388), 12, asphalt, True, "midright")
    contexto['buttons'].append((start, "start"))

    text(surface, "JOGADORES", (67, 457), 12, gray, True)
    for count, label, x in ((1, "1 JOGADOR", 64), (2, "2 JOGADORES", 282)):
        rect = pygame.Rect(x, 479, 208, 48)
        selected = contexto['player_count'] == count
        if rect.collidepoint(contexto['mouse']):
            pygame.draw.rect(surface, (39, 40, 41), rect)
        text(surface, label, (rect.x + 3, rect.y + 5), 20, gold if selected else gray, True)
        if selected:
            pygame.draw.line(surface, gold, (rect.x + 3, rect.bottom - 5), (rect.x + 174, rect.bottom - 5), 3)
        contexto['buttons'].append((rect, f"mode:{count}"))

    text(surface, "PISTA", (67, 557), 12, gray, True)
    for direction, rect in ((-1, pygame.Rect(64, 580, 36, 43)),
                            (1, pygame.Rect(458, 580, 36, 43))):
        if rect.collidepoint(contexto['mouse']):
            pygame.draw.rect(surface, (43, 43, 42), rect)
        cx, cy = rect.center
        pygame.draw.polygon(surface, gold, [(cx + direction * 7, cy),
                                            (cx - direction * 5, cy - 8),
                                            (cx - direction * 5, cy + 8)])
        contexto['buttons'].append((rect, f"stage:{(contexto['stage_index'] + direction) % len(STAGES)}"))
    text(surface, ["COSTA VERDE", "DESERTO", "CIDADE NEON"][contexto['stage_index']],
         (116, 584), 25, cream, True)
    text(surface, ["Fácil", "Médio", "Difícil"][contexto['stage_index']] + "  /  90 segundos",
         (116, 623), 12, gray)

    pygame.draw.line(surface, (64, 64, 61), (66, 681), (492, 681))
    text(surface, "1 / 2 jogadores     ← → pista     ESC sair", (67, 699), 12, gray)

    # Os dois protagonistas saem da própria arte do jogo, sem imagem externa.
    for brand, color, center, width, angle in (
            ("ifood", (247, 62, 73), (797, 678), 174, -5),
            ("99", (255, 211, 30), (1026, 696), 174, 5)):
        key = (brand, width, angle)
        if key not in contexto['menu_bikes']:
            sprite = bike_sprite(brand, color)
            sprite = pygame.transform.scale(sprite, (width, int(width * 226 / 144)))
            contexto['menu_bikes'][key] = pygame.transform.rotate(sprite, angle)
        sprite = contexto['menu_bikes'][key]
        surface.blit(sprite, sprite.get_rect(midbottom=center))

def resultado_v6(contexto):
    surface = contexto['canvas']
    race = contexto['race']
    text(surface, "BANDEIRADA  /  " + race['stage']["name"], (70, 39), 12, MINT, True)
    text(surface, "CADA METRO CONTA.", (66, 76), 48, WHITE, True)
    text(surface, "90 segundos de corrida. A maior distância leva a melhor.", (70, 147), 17, MUTED)
    text(surface, "POS.", (95, 208), 12, MUTED, True)
    text(surface, "PILOTO", (198, 208), 12, MUTED, True)
    text(surface, "DISTÂNCIA", (863, 208), 12, MUTED, True, "topright")
    text(surface, "BATIDAS", (1075, 208), 12, MUTED, True, "topright")
    for i, rider in enumerate(race['order']):
        y = 238 + i * 48
        rect = (70, y, 1060, 41)
        box(surface, rect, (30, 47, 56) if rider['human'] else PANEL, radius=7,
            border=rider['color'] if rider['human'] else None)
        text(surface, f"{i + 1:02d}", (95, y + 8), 19, rider['color'] if rider['human'] else MUTED, True)
        text(surface, rider['name'], (198, y + 9), 17, rider['color'] if rider['human'] else WHITE, True)
        text(surface, "VOCÊ" if rider['human'] else "NPC", (470, y + 13), 10, MUTED)
        text(surface, f"{rider['distance'] / 1000:.3f} km", (863, y + 10), 16, WHITE, anchor="topright")
        text(surface, str(rider['crashes']), (1075, y + 10), 16, MUTED, anchor="topright")
    text(surface, contexto['audio']['track_name'], (70, 577), 12, MUTED)
    adiciona_botao(contexto, (70, 621, 330, 57), "CORRER DE NOVO  [ENTER]", "start", True)
    adiciona_botao(contexto, (420, 621, 330, 57), "PRÓXIMA FASE  [N]", "next")
    adiciona_botao(contexto, (770, 621, 360, 57), "MENU  [ESC]", "menu")
    text(surface, "Os carros do trânsito são obstáculos. Os pilotos nomeados disputam a classificação.", (70, 710), 13, MUTED)
