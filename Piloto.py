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


