"""Parâmetros da apresentação visual; não altera as regras dos estudantes."""
import json
from pathlib import Path

WIDTH, HEIGHT = 1200, 760
DURATION = 90.0
LANES = [0.125, 0.375, 0.625, 0.875]
BIKE_DRAW_WIDTH = 0.090
CAR_DRAW_WIDTH = 0.118
BIKE_HALF_LENGTH = 1.0
CAR_HALF_LENGTH = 2.3
BOOST_CHARGE = 15.0
BOOST_DURATION = 3.0
STAGES = [
    {"name": "COSTA VERDE", "tag": "01 / AQUECIMENTO", "description": "Brisa do mar. Pé no acelerador.",
     "theme": "coast", "ground": (35, 91, 78), "accent": (80, 239, 208),
     "density": 1.0, "rival_speed": 159, "seed": 18, "track": "coast_rush", "track_name": "ASFALTO QUENTE · 150 BPM", "custom_track": "six_days", "custom_name": "SIX DAYS - REMIX"},
    {"name": "SOL DO DESERTO", "tag": "02 / PRESSÃO", "description": "Asfalto quente e menos espaço.",
     "theme": "desert", "ground": (147, 94, 58), "accent": (255, 192, 92),
     "density": 1.23, "rival_speed": 171, "seed": 37, "track": "desert_rush", "track_name": "GIRO MÁXIMO · 166 BPM", "custom_track": "deserto", "custom_name": "TRILHA DO DESERTO"},
    {"name": "CIDADE NEON", "tag": "03 / LIMITE", "description": "Luzes acesas. Reflexos em dia.",
     "theme": "city", "ground": (22, 28, 49), "accent": (185, 142, 255),
     "density": 1.48, "rival_speed": 181, "seed": 91, "track": "neon_rush", "track_name": "NEON RUSH", "custom_track": "tokyo_drift", "custom_name": "TOKYO DRIFT"},
]

# Cada JSON guarda a energia visual dos trechos da trilha original.
# Estes dados animam a interface; a música continua a cargo de Telas.py/telas.py.
CURVAS_VISUAIS = []
for nome in ["six_days", "deserto", "tokyo_drift"]:
    caminho = Path(__file__).resolve().parent / "assets" / (nome + "_energia.json")
    with open(caminho, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    CURVAS_VISUAIS.append(dados["sections"])


def music_section(seconds, stage_index=0):
    sections = CURVAS_VISUAIS[stage_index]
    for section in sections:
        if seconds < section[1]:
            return section
    return sections[-1]
