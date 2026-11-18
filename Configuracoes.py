"""Valores combinados pelos três integrantes. Sem regras escondidas aqui."""
import os

PASTA = os.path.dirname(os.path.abspath(__file__))
LARGURA = 1200
ALTURA = 760
DURACAO = 90
CARGA_NITRO = 15
DURACAO_NITRO = 3
VELOCIDADE_NORMAL = 210
VELOCIDADE_NITRO = 400
FAIXAS = [0.125, 0.375, 0.625, 0.875]
MARCAS = ["ifood", "99", "ze", "keeta", "rappi"]
NOMES = ["iFood", "99", "Zé Delivery", "Keeta", "Rappi"]
CORES = [(247, 62, 73), (255, 211, 30), (255, 207, 0), (255, 210, 31), (255, 90, 70)]
FASES = ["COSTA VERDE", "DESERTO", "CIDADE NEON"]
MUSICAS = ["six_days.mp3", "deserto.mp3", "tokyo_drift.mp3"]
CEUS = [(73, 154, 188), (199, 130, 103), (22, 20, 51)]
CHAO = [(52, 109, 79), (170, 119, 75), (35, 28, 47)]

# Uma energia para cada trecho de 3 segundos. Os dados já foram preparados
# a partir dos áudios enviados; não é preciso analisar som durante a corrida.
ENERGIAS = [[0.25, 0.25, 0.594, 0.781, 0.845, 0.906, 0.77, 1.0, 0.975, 0.76, 0.894, 0.964, 0.765, 0.863, 0.911, 0.906, 0.783, 0.862, 1.0, 0.855, 0.964, 0.928, 0.984, 0.867, 0.997, 0.986, 0.992, 0.87, 1.0, 0.756], [0.357, 0.303, 0.383, 0.25, 0.548, 0.25, 0.676, 0.853, 0.836, 1.0, 0.477, 0.719, 0.601, 0.725, 0.625, 0.98, 0.868, 0.757, 0.897, 0.797, 0.906, 0.47, 1.0, 0.737, 0.81, 1.0, 0.769, 0.997, 0.557, 0.868], [0.25, 0.524, 1.0, 0.997, 1.0, 0.955, 0.814, 0.882, 0.985, 1.0, 0.939, 0.898, 0.828, 1.0, 0.487, 0.442, 0.657, 0.691, 0.762, 0.517, 0.505, 0.629, 0.318, 0.767, 0.25, 0.277, 0.463, 0.27, 0.706, 0.985]]
