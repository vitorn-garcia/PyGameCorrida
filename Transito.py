"""PARTE 2: carros, fechadas do trânsito, contato e classificação."""
import random
from configuracoes import FAIXAS, ENERGIAS

def energia_musica(tempo, fase):
    indice = int(tempo/3)
    indice = min(indice, len(ENERGIAS[fase]) - 1)
    return ENERGIAS[fase][indice]

def cria_carro(carros, distancia, faixa):
    for outro in carros:
        esquerda = outro["x"]
        direita = outro["x"]
        if outro["destino"] is not None:
            esquerda = min(esquerda, FAIXAS[outro["destino"]])
            direita = max(direita, FAIXAS[outro["destino"]])
        if esquerda - 0.11 < FAIXAS[faixa] < direita + 0.11:
            if abs(outro["distancia"] - distancia) < 12:
                return None
    velocidade = random.randint(65, 118)
    carro = {"tipo": "carro", "imagem": random.randint(0, 2),
             "x": FAIXAS[faixa], "faixa": faixa, "distancia": distancia,
             "velocidade": velocidade, "cruzeiro": velocidade,
             "destino": None, "sinal": 0, "espera_troca": random.randint(4, 9)}
    carros.append(carro)
    return carro


def pede_troca(carro, destino, carros):
    if carro['destino'] is not in None:
        return False
    esquerda = min(carro['x'], FAIXAS[destino]) - 0.11
    direita = max(carro['x'], FAIXAS[destino]) + 0.11
    for outro in carros:
        if outro not in carro:
            ocupa_caminho = esquerda < outro['x'] < direita
            if outro["destino"] is not None:
                if esquerda < FAIXAS[outro["destino"]] < direita:
                    ocupa_caminho = True
            if ocupa_caminho and abs(outro["distancia"] - carro["distancia"]) < 45:
                return False
    carro["destino"] = destino
    carro["sinal"] = 0.9
    return True
