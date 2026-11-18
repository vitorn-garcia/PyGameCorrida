from Configuracoes import FAIXAS, MARCAS, NOMES, CORES
from Configuracoes import CARGA_NITRO, DURACAO_NITRO, VELOCIDADE_NORMAL, VELOCIDADE_NITRO

def cria_pilotos(quantidade):
    pilotos = []
    posicoes = [0.375, 0.625, 0.125, 0.625, 0.875]
    distancias = [0, 0, 13, 24, 35]
    for i in range(5):
        piloto = {"nome": NOMES[i], "marca": MARCAS[i], "cor": CORES[i],
                  "tipo": "moto", "humano": i < quantidade,
                  "x": posicoes[i], "distancia": distancias[i], "velocidade": 0,
                  "alvo": posicoes[i], "limite_bot": 158 + i * 4,
                  "sem_bater": 0, "nitro": 0, "protecao": 0, "batidas": 0,
                  "fechando": 0, "direcao_fechada": 0, "recarga_fechada": 0,
                  "linha": -1, "tempo_linha": 0, "espera_trafego": 0}
        pilotos.append(piloto)
    return pilotos


def le_comando(teclas, cima, baixo, esquerda, direita):
    acelerador = 0
    direcao = 0
    if teclas[cima]:
        acelerador += 1
    if teclas[baixo]:
        acelerador -= 1
    if teclas[direita]:
        direcao += 1
    if teclas[esquerda]:
        direcao -= 1
    return [acelerador, direcao]


def ativa_nitro(piloto):
    if piloto["sem_bater"] >= CARGA_NITRO and piloto["nitro"] == 0:
        piloto["nitro"] = DURACAO_NITRO
        piloto["sem_bater"] = 0
        piloto["velocidade"] = VELOCIDADE_NITRO
        return True
    return False


def inicia_fechada(piloto, pilotos):
    if piloto["recarga_fechada"] > 0 or piloto["protecao"] > 0:
        return False
    for outro in pilotos:
        if outro is not piloto:
            perto = abs(outro["distancia"] - piloto["distancia"]) < 2
            ao_lado = abs(outro["x"] - piloto["x"]) < 0.19
            if perto and ao_lado and outro["protecao"] == 0:
                piloto["direcao_fechada"] = -1
                if outro["x"] >= piloto["x"]:
                    piloto["direcao_fechada"] = 1
                piloto["fechando"] = 0.24
                piloto["recarga_fechada"] = 4
                return True
    return False
