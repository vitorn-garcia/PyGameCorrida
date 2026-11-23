"""Arte da V6: formas do PyGame e logotipos locais, adaptada para dicionários."""
import math
from pathlib import Path
import pygame
from .config_visual import (LANES, DURATION, BIKE_DRAW_WIDTH, CAR_DRAW_WIDTH,
                    BIKE_HALF_LENGTH, CAR_HALF_LENGTH, BOOST_DURATION)

BG = (12, 18, 29)
PANEL = (22, 31, 45)
WHITE = (240, 245, 246)
MUTED = (151, 167, 182)
MINT = (80, 239, 208)
FONTS = {}
POSTER_TEXT = {}


def font(size, bold=False):
    key = (size, bold)
    if key not in FONTS:
        path = Path(__file__).resolve().parent / "assets" / ("bold.ttf" if bold else "regular.ttf")
        FONTS[key] = pygame.font.Font(str(path) if path.exists() else None, size)
    return FONTS[key]


def text(surface, message, position, size=20, color=WHITE, bold=False, anchor="topleft"):
    rendered = font(size, bold).render(str(message), True, color)
    rect = rendered.get_rect(**{anchor: position})
    surface.blit(rendered, rect)
    return rect


def poster_text(surface, message, position, size, color):
    """Letreiro inclinado de arcade, com contorno e sombra impressa."""
    key = (message, size, color)
    if key not in POSTER_TEXT:
        path = Path(__file__).resolve().parent / "assets" / "bold.ttf"
        face = pygame.font.Font(str(path) if path.exists() else None, size)
        face.set_italic(True)
        label = face.render(message, True, color)
        outline = face.render(message, True, (7, 8, 9))
        sticker = pygame.Surface((label.get_width() + 16, label.get_height() + 16), pygame.SRCALPHA)
        sticker.blit(outline, (9, 10))
        for dx, dy in ((0, 2), (2, 0), (4, 2), (2, 4), (0, 0), (4, 0), (0, 4), (4, 4)):
            sticker.blit(outline, (dx, dy))
        sticker.blit(label, (2, 2))
        POSTER_TEXT[key] = sticker
    surface.blit(POSTER_TEXT[key], position)


def box(surface, rect, color=PANEL, radius=12, border=None):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border, rect, 1, border_radius=radius)


def button(surface, rect, label, selected=False, accent=MINT, hovered=False):
    color = accent if selected else ((36, 49, 65) if hovered else PANEL)
    box(surface, rect, color, border=accent if hovered or selected else (53, 67, 82))
    text(surface, label, pygame.Rect(rect).center, 18, BG if selected else WHITE, True, "center")


SPRITES = {}
SKIES = {}
LOGOS = {}


def brand_logo(surface, brand, rect):
    """Mantém a proporção dos arquivos das marcas, sem depender de internet."""
    if brand not in LOGOS:
        path = Path(__file__).resolve().parent / "assets" / "logos" / (brand + ".png")
        LOGOS[brand] = pygame.image.load(str(path)).convert_alpha() if path.is_file() else None
    logo = LOGOS[brand]
    if logo is None:
        return False
    rect = pygame.Rect(rect)
    scale = min(rect.w / logo.get_width(), rect.h / logo.get_height())
    resized = pygame.transform.smoothscale(logo, (max(1, int(logo.get_width() * scale)), max(1, int(logo.get_height() * scale))))
    surface.blit(resized, resized.get_rect(center=rect.center))
    return True


def bike_sprite(brand, color):
    key = (brand, color)
    if key in SPRITES:
        return SPRITES[key]
    s = pygame.Surface((144, 226), pygame.SRCALPHA)
    yellow = brand == "99"
    ink = (23, 27, 33)
    uniform = (255, 211, 30) if yellow else ((27, 28, 30) if brand == "ze" else color)
    pygame.draw.ellipse(s, (0, 0, 0, 85), (24, 207, 98, 16))
    pygame.draw.rect(s, (10, 15, 22), (57, 166, 31, 53), border_radius=12)
    pygame.draw.line(s, (95, 102, 112), (72, 173), (72, 213), 4)
    # Pernas, motor e carenagem vistos por trás.
    pygame.draw.polygon(s, (27, 31, 40), [(37, 126), (59, 137), (52, 190), (35, 194), (28, 163)])
    pygame.draw.polygon(s, (27, 31, 40), [(106, 126), (85, 137), (92, 190), (110, 194), (117, 163)])
    pygame.draw.rect(s, (16, 20, 28), (24, 184, 32, 13), border_radius=5)
    pygame.draw.rect(s, (16, 20, 28), (88, 184, 32, 13), border_radius=5)
    pygame.draw.polygon(s, uniform, [(45, 135), (99, 135), (106, 168), (91, 185), (53, 185), (38, 168)])
    pygame.draw.rect(s, (43, 47, 56), (47, 151, 50, 13), border_radius=4)
    pygame.draw.rect(s, (255, 83, 81), (51, 166, 42, 7), border_radius=3)
    pygame.draw.rect(s, (233, 238, 233), (58, 179, 28, 14), border_radius=2)
    pygame.draw.rect(s, (102, 110, 119), (110, 162, 11, 35), border_radius=4)
    # Jaqueta, braços e capacete.
    pygame.draw.polygon(s, uniform, [(44, 49), (100, 49), (116, 111), (28, 111)])
    for points in ([(42, 54), (27, 62), (12, 105), (29, 112), (47, 81)],
                   [(102, 54), (117, 62), (132, 105), (115, 112), (97, 81)]):
        pygame.draw.polygon(s, uniform, points)
    pygame.draw.line(s, (25, 29, 36), (12, 108), (36, 109), 8)
    pygame.draw.line(s, (25, 29, 36), (109, 109), (133, 108), 8)
    pygame.draw.ellipse(s, (255, 211, 30) if yellow else (242, 243, 232), (47, 7, 50, 51))
    pygame.draw.rect(s, ink, (49, 24, 46, 12), border_radius=5)
    pygame.draw.line(s, uniform, (72, 8), (72, 22), 6)
    # A bag é a face principal do personagem, com marca legível.
    pygame.draw.rect(s, (15, 20, 28), (29, 68, 88, 80), border_radius=9)
    pygame.draw.rect(s, color, (32, 68, 80, 73), border_radius=7)
    light = tuple(min(255, channel + 22) for channel in color)
    pygame.draw.polygon(s, light, [(32, 68), (44, 60), (103, 60), (112, 68)])
    pygame.draw.line(s, (255, 238, 149) if yellow else (255, 137, 139), (40, 76), (104, 76), 2)
    if brand == "ifood":
        text(s, "iFood", (72, 103), 25, WHITE, True, "center")
        pygame.draw.arc(s, WHITE, (54, 107, 37, 17), math.pi, math.pi * 1.85, 3)
    elif yellow:
        text(s, "99", (72, 104), 42, ink, True, "center")
    elif brand in ("ze", "keeta", "rappi"):
        if not brand_logo(s, brand, (36, 81, 72, 44)):
            text(s, {"ze": "Zé", "keeta": "Keeta", "rappi": "Rappi"}[brand], (72, 104), 23, ink if brand != "rappi" else WHITE, True, "center")
    else:
        text(s, "GRAU", (72, 104), 20, WHITE, True, "center")
    pygame.draw.rect(s, (240, 240, 221), (42, 131, 60, 4), border_radius=2)
    SPRITES[key] = s
    return s


def wheelie_amount(boost_time):
    """Levanta no início e baixa no fim do nitro; uma batida zera a pose."""
    if boost_time <= 0:
        return 0.0
    elapsed = BOOST_DURATION - boost_time
    amount = max(0.0, min(1.0, elapsed / .18, boost_time / .22))
    return amount * amount * (3 - 2 * amount)


def wheelie_sprite(brand, color, amount):
    """Pose em três quartos: dianteira no ar, peso sobre a roda traseira."""
    level = round(amount * 10)
    if level <= 0:
        return bike_sprite(brand, color)
    key = ("wheelie", brand, color, level)
    if key in SPRITES:
        return SPRITES[key]
    lift = level / 10
    s = pygame.Surface((144, 256), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0, 0, 0, 85), (28, 238, 88, 15))
    # O pneu traseiro permanece no mesmo ponto da pista durante a animação.
    pygame.draw.rect(s, (10, 15, 22), (57, 196, 31, 53), border_radius=12)
    pygame.draw.line(s, (95, 102, 112), (72, 201), (72, 242), 4)
    # A roda da frente sobe e se revela à direita, presa à suspensão.
    fx, fy = 76 + 53 * lift, 218 - 123 * lift
    fw, fh = 22 + 3 * lift, 43 + 5 * lift
    pygame.draw.ellipse(s, (12, 17, 24), (fx - fw / 2, fy - fh / 2, fw, fh))
    pygame.draw.ellipse(s, (104, 117, 126), (fx - fw / 2 + 5, fy - fh / 2 + 7, fw - 10, fh - 14), 3)
    pygame.draw.line(s, (178, 188, 192), (fx, fy), (fx - 1, fy - fh / 2 + 8), 2)
    for dx in (-4, 4):
        pygame.draw.line(s, (146, 156, 166), (91 + dx, 181 - 34 * lift), (fx + dx, fy), 5)
    # Motor e carenagem inclinados para cima, sem mover a área de contato.
    pygame.draw.polygon(s, (27, 33, 42), [(64, 218), (50, 176),
                        (88, 157 - 17 * lift), (105, 171 - 20 * lift), (91, 204)])
    pygame.draw.polygon(s, color, [(38, 169 - 9 * lift), (82, 162 - 22 * lift),
                        (103, 173 - 24 * lift), (89, 197), (54, 213), (38, 194)])
    pygame.draw.line(s, (148, 156, 164), (72, 221), (90, 175 - 10 * lift), 4)
    pygame.draw.rect(s, (40, 46, 56), (56, 181, 35, 17), border_radius=5)
    pygame.draw.rect(s, (255, 76, 73), (51, 204, 40, 7), border_radius=3)
    pygame.draw.rect(s, (233, 238, 233), (61, 215, 25, 14), border_radius=2)
    # Joelhos dobrados e pés nos apoios; o entregador recua junto com a bag.
    pygame.draw.lines(s, (27, 31, 40), False,
                      [(43, 151 - 8 * lift), (34, 179), (57, 191)], 16)
    pygame.draw.lines(s, (27, 31, 40), False,
                      [(94, 150 - 10 * lift), (104, 178 - 13 * lift), (119, 173 - 12 * lift)], 15)
    pygame.draw.line(s, (14, 18, 26), (47, 192), (66, 192), 9)
    pygame.draw.line(s, (14, 18, 26), (111, 176 - 12 * lift), (129, 174 - 12 * lift), 9)
    # Reutiliza uniforme, capacete e marca do personagem, mantendo a identidade.
    torso = bike_sprite(brand, color).subsurface((0, 0, 144, 147))
    torso = pygame.transform.rotate(torso, 9 * lift)
    s.blit(torso, torso.get_rect(midbottom=(72 - int(13 * lift), 177 - int(10 * lift))))
    # A roda elevada fica visível ao lado do corpo nesta vista em três quartos.
    # Desenhá-la por último evita que a mochila esconda o movimento.
    if lift >= .3:
        pygame.draw.ellipse(s, (10, 14, 21), (fx - fw / 2, fy - fh / 2, fw, fh))
        pygame.draw.ellipse(s, (150, 166, 179), (fx - fw / 2 + 5, fy - fh / 2 + 7, fw - 10, fh - 14), 3)
        pygame.draw.line(s, (116, 131, 145), (fx, fy - fh / 2 + 9), (fx, fy + fh / 2 - 9), 2)
        pygame.draw.circle(s, (218, 224, 229), (round(fx), round(fy)), 3)
    SPRITES[key] = s
    return s


def rear_car(color, kind=0):
    key = ("car", color, kind)
    if key in SPRITES:
        return SPRITES[key]
    s = pygame.Surface((160, 123), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0, 0, 0, 80), (3, 106, 154, 15))
    pygame.draw.rect(s, (13, 18, 25), (15, 85, 22, 31), border_radius=4)
    pygame.draw.rect(s, (13, 18, 25), (123, 85, 22, 31), border_radius=4)
    roof = 14 if kind != 2 else 0
    pygame.draw.polygon(s, color, [(10, 64), (33, roof + 14), (126, roof + 14), (150, 64), (152, 106), (9, 106)])
    pygame.draw.polygon(s, (34, 52, 65), [(37, roof + 23), (121, roof + 23), (134, 63), (25, 63)])
    pygame.draw.line(s, (88, 111, 126), (40, roof + 28), (115, roof + 28), 3)
    pygame.draw.rect(s, tuple(max(0, c - 24) for c in color), (9, 65, 143, 39), border_radius=7)
    pygame.draw.rect(s, (255, 77, 73), (14, 73, 31, 13), border_radius=3)
    pygame.draw.rect(s, (255, 77, 73), (114, 73, 31, 13), border_radius=3)
    pygame.draw.rect(s, (222, 227, 214), (62, 84, 36, 13), border_radius=2)
    pygame.draw.line(s, (32, 37, 45), (16, 103), (144, 103), 5)
    SPRITES[key] = s
    return s


def car_indicator(surface, x, y, width, car, timer):
    if car['target_x'] is None or int(timer * 5) % 2:
        return
    side = 1 if car['target_x'] > car['x'] else -1
    # Posição das setas na traseira do carro; o pisca precede a manobra.
    cx = int(x + side * width * .37)
    cy = int(y - width * .245)
    pygame.draw.rect(surface, (255, 202, 55), (cx - max(2, int(width * .045)), cy, max(4, int(width * .09)), max(3, int(width * .06))))


def sky(surface, theme):
    w, h = surface.get_size()
    key = (w, h, theme)
    if key not in SKIES:
        s = pygame.Surface((w, h))
        palettes = {"coast": ((40, 122, 166), (183, 218, 213)),
                    "desert": ((86, 75, 139), (250, 177, 112)),
                    "city": ((9, 12, 34), (71, 38, 92))}
        top, bottom = palettes[theme]
        horizon = int(h * 0.29)
        for y in range(horizon + 1):
            fraction = y / max(1, horizon)
            color = tuple(int(a + (b - a) * fraction) for a, b in zip(top, bottom))
            pygame.draw.line(s, color, (0, y), (w, y))
        sun = (255, 213, 142) if theme != "city" else (226, 218, 247)
        pygame.draw.circle(s, sun, (int(w * 0.76), int(h * 0.13)), int(h * (0.055 if theme != "desert" else 0.073)))
        if theme == "city":
            for i in range(45):
                pygame.draw.circle(s, (151, 134, 185), ((i * 97 + 31) % w, (i * 31 + 9) % max(1, horizon - 30)), 1)
            for i in range(23):
                bx = int(i * w / 22)
                bh = 22 + (i * 37) % 79
                pygame.draw.rect(s, (18, 19, 45), (bx, horizon - bh, int(w / 20), bh + 3))
                for yy in range(horizon - bh + 7, horizon - 5, 12):
                    pygame.draw.line(s, (111, 69, 134), (bx + 5, yy), (bx + w / 30, yy), 2)
        else:
            mountain = (68, 123, 129) if theme == "coast" else (152, 111, 124)
            points = [(0, horizon)]
            for i in range(13):
                points.append((int(i * w / 12), horizon - 15 - (i * 29) % 42))
            points += [(w, horizon), (0, horizon)]
            pygame.draw.polygon(s, mountain, points)
        SKIES[key] = s
    surface.blit(SKIES[key], (0, 0))


def place(race, viewer):
    return race['order'].index(viewer) + 1


def project(surface, viewer, x, z):
    """Projeção 2D: objetos distantes ficam pequenos junto ao horizonte."""
    w, h = surface.get_size()
    t = 28 / max(19, 28 + z)
    road_width = min(w * 1.35, 1250) * t
    center = w / 2 - (viewer['x'] - 0.5) * road_width * 0.46
    return center + (x - 0.5) * road_width, h * 0.29 + h * 0.69 * t, road_width, t


def roadside(surface, race, viewer):
    theme = race['stage']["theme"]
    base = int(viewer['distance'] // 28) * 28
    for world_s in range(base + 420, base - 1, -28):
        z = world_s - viewer['distance']
        if z < 0:
            continue
        for side in (0, 1):
            lane_x = -0.14 if side == 0 else 1.14
            x, y, road_w, t = project(surface, viewer, lane_x, z)
            size = min(2.5, road_w / 810)
            if x < -150 or x > surface.get_width() + 150:
                continue
            if theme == "coast":
                pygame.draw.line(surface, (93, 73, 50), (x, y), (x - 11 * size, y - 119 * size), max(1, int(8 * size)))
                for dx, dy in ((-60, -12), (-48, 22), (-16, -36), (38, -24), (57, 15)):
                    pygame.draw.line(surface, (29, 105, 76), (x - 11 * size, y - 119 * size),
                                     (x + dx * size, y - 119 * size + dy * size), max(1, int(10 * size)))
            elif theme == "desert":
                pygame.draw.polygon(surface, (124, 85, 79), [(x - 39 * size, y), (x - 17 * size, y - 54 * size),
                                                                          (x + 18 * size, y - 64 * size), (x + 43 * size, y)])
                pygame.draw.line(surface, (70, 109, 78), (x + 50 * size, y), (x + 50 * size, y - 59 * size), max(1, int(8 * size)))
            else:
                height = (100 + world_s % 71) * size
                width = 95 * size
                rect = pygame.Rect(x - width / 2, y - height, width, height)
                pygame.draw.rect(surface, (23, 24, 49), rect)
                pygame.draw.line(surface, (106, 60, 143), rect.topleft, rect.topright, max(1, int(size * 3)))
                for row in range(1, 6):
                    for col in range(1, 4):
                        r = (rect.x + col * width / 4 - size * 4, rect.y + row * height / 7, size * 9, size * 7)
                        pygame.draw.rect(surface, (194, 134, 168) if (row + col) % 3 else (241, 204, 104), r)


def draw_world(surface, race, viewer, timer=0, hud=True):
    w, h = surface.get_size()
    theme = race['stage']["theme"]
    sky(surface, theme)
    horizon = int(h * 0.29)
    ground = {"coast": (61, 121, 90), "desert": (187, 128, 85), "city": (22, 21, 43)}[theme]
    pygame.draw.rect(surface, ground, (0, horizon, w, h - horizon))
    # Faixas de estrada desenhadas em perspectiva, do horizonte até a moto.
    for y in range(horizon + 1, h + 5, 5):
        y1, y2 = y, min(h + 5, y + 5)
        t1 = (y1 - h * 0.29) / (h * 0.69)
        t2 = (y2 - h * 0.29) / (h * 0.69)
        z1, z2 = 28 * (1 / max(.001, t1) - 1), 28 * (1 / max(.001, t2) - 1)
        l1, _, rw1, _ = project(surface, viewer, 0, z1)
        l2, _, rw2, _ = project(surface, viewer, 0, z2)
        world_s = viewer['distance'] + z1
        alternating = int(world_s / 18) % 2
        asphalt = ((42, 40, 58) if alternating else (39, 37, 54)) if theme == "city" else ((62, 64, 70) if alternating else (58, 60, 67))
        pygame.draw.polygon(surface, asphalt, [(l1, y1), (l1 + rw1, y1), (l2 + rw2, y2), (l2, y2)])
        curb = (238, 236, 215) if int(world_s / 8) % 2 else ((164, 86, 213) if theme == "city" else (224, 101, 93))
        for edge in (0, 1):
            x1, x2 = l1 + rw1 * edge, l2 + rw2 * edge
            sign = -1 if edge == 0 else 1
            pygame.draw.polygon(surface, curb, [(x1, y1), (x1 + sign * rw1 * .025, y1), (x2 + sign * rw2 * .025, y2), (x2, y2)])
        if int(world_s / 9) % 2 == 0:
            for lane in (0.25, 0.5, 0.75):
                pygame.draw.polygon(surface, (210, 209, 198), [(l1 + rw1 * (lane - .0025), y1), (l1 + rw1 * (lane + .0025), y1),
                                                                            (l2 + rw2 * (lane + .0025), y2), (l2 + rw2 * (lane - .0025), y2)])
    roadside(surface, race, viewer)
    objects = [(obj['distance'], "car", obj) for obj in race['traffic']]
    objects += [(rider['distance'], "bike", rider) for rider in race['riders']]
    for distance, kind, obj in sorted(objects, key=lambda item: item[0], reverse=True):
        half_length = CAR_HALF_LENGTH if kind == "car" else BIKE_HALF_LENGTH
        z = distance - half_length - (viewer['distance'] - BIKE_HALF_LENGTH)
        if z < -5 or z > 520:
            continue
        x, y, rw, t = project(surface, viewer, obj['x'], z)
        if kind == "car":
            sprite = rear_car(obj['color'], obj['kind'])
            width = max(3, int(rw * CAR_DRAW_WIDTH))
            sprite = pygame.transform.smoothscale(sprite, (width, max(3, int(width * 123 / 160))))
        else:
            lift = wheelie_amount(obj['boost_time'])
            sprite = wheelie_sprite(obj['brand'], obj['color'], lift)
            width = max(4, int(rw * BIKE_DRAW_WIDTH))
            sprite = pygame.transform.smoothscale(sprite, (width, max(6, int(width * sprite.get_height() / sprite.get_width()))))
            if obj['boost_time'] > 0:
                glow = pygame.Surface((w, h), pygame.SRCALPHA)
                for offset in (-13, 13):
                    pygame.draw.polygon(glow, (104, 198, 255, 190), [(x + offset * t - 8 * t, y - 13 * t),
                                                                               (x + offset * t + 8 * t, y - 13 * t),
                                                                               (x + offset * t, y + (22 + math.sin(timer * 40) * 12) * t)])
                surface.blit(glow, (0, 0))
            if obj['lean']:
                sprite = pygame.transform.rotate(sprite, -obj['lean'] * .42)
            if obj['cooldown'] > 0 and int(timer * 15) % 2 == 0:
                sprite.set_alpha(125)
        surface.blit(sprite, sprite.get_rect(midbottom=(int(x), int(y))))
        if kind == "car":
            car_indicator(surface, x, y, width, obj, timer)
        if kind == "bike" and obj is not viewer and z < 100:
            text(surface, obj['name'], (x, y - sprite.get_height() - 5), max(9, int(16 * min(1, t))), obj['color'], True, "midbottom")
    if viewer['boost_time'] > 0:
        # Linhas de velocidade nas bordas reforçam a sensação de arrancada.
        for i in range(12):
            angle = i * math.pi / 6 + timer * .08
            sx, sy = w / 2 + math.cos(angle) * w * .38, h * .47 + math.sin(angle) * h * .40
            ex, ey = w / 2 + math.cos(angle) * w * .62, h * .47 + math.sin(angle) * h * .70
            pygame.draw.line(surface, (156, 213, 243), (sx, sy), (ex, ey), 2)
    if not hud:
        return
    accent = viewer['color']
    box(surface, (16, 14, 134, 76), (16, 22, 35), border=accent)
    text(surface, viewer['name'], (28, 23), 13, accent, True)
    text(surface, f"{place(race, viewer):02d}", (27, 41), 30, WHITE, True)
    text(surface, f"/ {len(race['riders'])}", (85, 56), 15, MUTED)
    box(surface, (w - 151, 14, 135, 76), (16, 22, 35), border=accent)
    text(surface, f"{int(viewer['speed']):03d}", (w - 30, 21), 31, WHITE, True, "topright")
    text(surface, "KM/H", (w - 30, 65), 10, accent, True, "topright")
    # Estado do poder: barra nunca carrega durante a contagem inicial.
    from .config_visual import BOOST_CHARGE
    charge_top = 107 if w < 900 else h - 94
    box(surface, (16, charge_top, 234, 76), (16, 22, 35), border=accent if viewer['boost_ready'] or viewer['boost_time'] > 0 else (63, 69, 85))
    key = "SHIFT ESQ" if race['players'].index(viewer) == 0 else "SHIFT DIR"
    if viewer['boost_time'] > 0:
        label = f"NITRO  {viewer['boost_time']:.1f}s"
    elif viewer['boost_ready']:
        label = "NITRO PRONTO  [" + key + "]"
    else:
        label = f"SEM BATER: {int(viewer['clean_time']):02d} / {BOOST_CHARGE:.0f} s"
    text(surface, label, (28, charge_top + 11), 12, accent, True)
    box(surface, (28, charge_top + 37, 208, 6), (57, 61, 77), radius=3)
    progress = int(208 * viewer['clean_time'] / BOOST_CHARGE)
    if progress:
        box(surface, (28, charge_top + 37, progress, 6), accent, radius=3)
    text(surface, f"{viewer['distance'] / 1000:.2f} km  ·  {viewer['crashes']} batidas", (28, charge_top + 52), 11, MUTED)
    other_humans = [r for r in race['players'] if r is not viewer]
    if other_humans:
        other = other_humans[0]
        gap = other['distance'] - viewer['distance']
        text(surface, f"{other['name']}: {abs(gap):.0f} m " + ("À FRENTE" if gap >= 0 else "ATRÁS"), (w - 18, 110), 11, other['color'], True, "topright")
    if w > 900:
        box(surface, (18, 139, 190, 245), (16, 22, 35))
        text(surface, "ENTREGADORES", (31, 151), 11, MUTED, True)
        for i, rider in enumerate(race['order']):
            text(surface, f"{i + 1:02d}  {rider['name']}", (31, 181 + i * 29), 13, rider['color'], rider['human'])
        box(surface, (w - 210, 143, 192, 149), (16, 22, 35))
        for i, line in enumerate(["↑ / W  ACELERA", "↓ / S   FREIA", "← → / A D  DIREÇÃO", "SHIFT / ESPAÇO  NITRO", "F  FECHADA"]):
            text(surface, line, (w - 198, 156 + i * 25), 11, MUTED, i == 4)
    if viewer['message_time'] > 0:
        message_color = (124, 213, 255) if viewer['boost_time'] > 0 else (255, 220, 169)
        text(surface, viewer['message'], (w / 2, h * .39), 21 if w < 900 else 29, message_color, True, "center")
    if viewer['cooldown'] > .75:
        pygame.draw.rect(surface, (240, 101, 111), (1, 1, w - 2, h - 2), 3)


def music_bar(surface, rect, elapsed, section, accent=MINT):
    x, y, w, h = rect
    box(surface, rect, (35, 46, 61), radius=4)
    width = int(w * elapsed / DURATION)
    if width > 0:
        box(surface, (x, y, width, h), accent, radius=4)
    for fraction in (1/6, 2/6, 3/6, 4/6, 5/6):
        pygame.draw.line(surface, BG, (x + w * fraction, y), (x + w * fraction, y + h), 2)


def equalizer(surface, x, y, seconds, intensity, accent, width=4, count=17, height=30):
    for i in range(count):
        amount = (0.22 + 0.78 * abs(math.sin(seconds * 6 + i * 0.78))) * (0.38 + intensity * 0.62)
        bar_h = max(3, int(height * amount))
        pygame.draw.rect(surface, accent, (x + i * (width + 3), y + height - bar_h, width, bar_h), border_radius=2)
