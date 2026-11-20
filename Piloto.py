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


def move_jogador(piloto, comando, dt):
    acelerador = comando[0]
    direcao = comando[1]
    limite = VELOCIDADE_NORMAL
    aceleracao = -11
    if acelerador > 0:
        aceleracao = 29
    if acelerador < 0:
        aceleracao = -72
    if piloto["nitro"] > 0:
        limite = VELOCIDADE_NITRO
        if acelerador > 0:
            aceleracao = 160
    piloto["velocidade"] += aceleracao * dt
    if piloto["velocidade"] < 0:
        piloto["velocidade"] = 0
    if piloto["velocidade"] > limite:
        piloto["velocidade"] = limite
    piloto["x"] += direcao * (0.39 + piloto["velocidade"] / 700) * dt


def escolhe_faixa(piloto, carros):
    melhor_faixa = piloto["alvo"]
    maior_espaco = -1
    for faixa in FAIXAS:
        espaco = 300
        for carro in carros:
            diferenca = carro["distancia"] - piloto["distancia"]
            if abs(carro["x"] - faixa) < 0.14 and diferenca > -8:
                if abs(diferenca) < espaco:
                    espaco = abs(diferenca)
        if espaco > maior_espaco:
            maior_espaco = espaco
            melhor_faixa = faixa
    return melhor_faixa


def move_bot(piloto, carros, fase, dt):
    limite = piloto["limite_bot"] + fase * 10
    for carro in carros:
        diferenca = carro["distancia"] - piloto["distancia"]
        if -3 < diferenca < 35 and abs(carro["x"] - piloto["x"]) < 0.13:
            piloto["alvo"] = escolhe_faixa(piloto, carros)
            if 0 < diferenca < 12:
                limite = 75
    if piloto["x"] < piloto["alvo"]:
        piloto["x"] = min(piloto["alvo"], piloto["x"] + 0.45 * dt)
    if piloto["x"] > piloto["alvo"]:
        piloto["x"] = max(piloto["alvo"], piloto["x"] - 0.45 * dt)
    if piloto["velocidade"] < limite:
        piloto["velocidade"] = min(limite, piloto["velocidade"] + 26 * dt)
    if piloto["velocidade"] > limite:
        piloto["velocidade"] = max(limite, piloto["velocidade"] - 55 * dt)


def atualiza_pilotos(pilotos, carros, comandos, fase, dt):
    for i in range(len(pilotos)):
        piloto = pilotos[i]
        # Os contadores são tempos restantes, em segundos.
        for campo in ["nitro", "protecao", "recarga_fechada", "espera_trafego"]:
            piloto[campo] = max(0, piloto[campo] - dt)
            if piloto[campo] < 0.000001:
                piloto[campo] = 0
        piloto["sem_bater"] = min(CARGA_NITRO, piloto["sem_bater"] + dt)
        if CARGA_NITRO - piloto["sem_bater"] < 0.000001:
            piloto["sem_bater"] = CARGA_NITRO
        if piloto["humano"]:
            move_jogador(piloto, comandos[i], dt)
        else:
            move_bot(piloto, carros, fase, dt)
        if piloto["fechando"] > 0:
            piloto["x"] += piloto["direcao_fechada"] * 0.52 * dt
            piloto["fechando"] = max(0, piloto["fechando"] - dt)
        piloto["x"] = max(0.04, min(0.96, piloto["x"]))
        piloto["distancia"] += piloto["velocidade"] / 3.6 * dt

