"""PARTE 2: carros, fechadas do trânsito, contato e classificação."""
import random
from configuracoes import FAIXAS, ENERGIAS


def energia_musica(tempo, fase):
    indice = int(tempo / 3)
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
    if carro["destino"] is not None:
        return False
    esquerda = min(carro["x"], FAIXAS[destino]) - 0.11
    direita = max(carro["x"], FAIXAS[destino]) + 0.11
    for outro in carros:
        if outro is not carro:
            ocupa_caminho = esquerda < outro["x"] < direita
            if outro["destino"] is not None:
                if esquerda < FAIXAS[outro["destino"]] < direita:
                    ocupa_caminho = True
            if ocupa_caminho and abs(outro["distancia"] - carro["distancia"]) < 45:
                return False
    carro["destino"] = destino
    carro["sinal"] = 0.9
    return True


def atualiza_carros(carros, dt):
    for carro in carros:
        carro["espera_troca"] -= dt
        if carro["espera_troca"] <= 0 and carro["destino"] is None:
            carro["espera_troca"] = random.randint(5, 10)
            destino = carro["faixa"] + random.choice([-1, 1])
            if 0 <= destino < 4:
                pede_troca(carro, destino, carros)
        novo_x = carro["x"]
        if carro["destino"] is not None:
            carro["sinal"] = max(0, carro["sinal"] - dt)
            if carro["sinal"] == 0:
                alvo = FAIXAS[carro["destino"]]
                if novo_x < alvo:
                    novo_x = min(alvo, novo_x + 0.085 * dt)
                else:
                    novo_x = max(alvo, novo_x - 0.085 * dt)
                for outro in carros:
                    if outro is not carro:
                        perto = abs(outro["distancia"] - carro["distancia"]) < 8
                        sobrepoe = abs(outro["x"] - novo_x) < 0.11
                        if perto and sobrepoe:
                            novo_x = carro["x"]
            carro["x"] = novo_x
            if abs(carro["x"] - FAIXAS[carro["destino"]]) < 0.001:
                carro["faixa"] = carro["destino"]
                carro["destino"] = None
        carro["velocidade"] = min(carro["cruzeiro"], carro["velocidade"] + 12 * dt)
        nova_distancia = carro["distancia"] + carro["velocidade"] / 3.6 * dt
        for outro in carros:
            if outro is not carro and outro["distancia"] > carro["distancia"]:
                if abs(outro["x"] - carro["x"]) < 0.112:
                    limite = max(carro["distancia"], outro["distancia"] - 7.4)
                    nova_distancia = min(nova_distancia, limite)
        carro["velocidade"] = (nova_distancia - carro["distancia"]) / dt * 3.6
        carro["distancia"] = nova_distancia


def pressiona_linha(piloto, carros, dt):
    linha = -1
    for i in range(3):
        if abs(piloto["x"] - (i + 1) * 0.25) < 0.037:
            linha = i
    if linha >= 0 and linha == piloto["linha"]:
        piloto["tempo_linha"] += dt
    else:
        piloto["tempo_linha"] = 0
    piloto["linha"] = linha
    if linha < 0 or piloto["tempo_linha"] < 3.2:
        return
    if piloto["velocidade"] <= 95 or piloto["espera_trafego"] > 0:
        return
    # Cria um carro à frente para atravessar a divisória. Não há dano remoto.
    origem = random.choice([linha, linha + 1])
    destino = linha
    if origem == linha:
        destino = linha + 1
    aproximacao = (piloto["velocidade"] - 72) / 3.6
    distancia = piloto["distancia"] + max(68, aproximacao * 2.4 + 4)
    carro = cria_carro(carros, distancia, origem)
    piloto["espera_trafego"] = 0.5
    if carro is not None:
        carro["velocidade"] = 72
        carro["cruzeiro"] = 72
        if pede_troca(carro, destino, carros):
            piloto["espera_trafego"] = 6



def atualiza_transito(jogo, dt):
    carros = jogo["carros"]
    atualiza_carros(carros, dt)
    for piloto in jogo["pilotos"]:
        if piloto["humano"]:
            pressiona_linha(piloto, carros, dt)
    jogo["novo_carro"] -= dt
    if jogo["novo_carro"] <= 0:
        energia = energia_musica(jogo["tempo"], jogo["fase"])
        jogo["novo_carro"] = (2.6 - 1.65 * energia) / (1 + jogo["fase"] * 0.2)
        for i in range(jogo["quantidade"]):
            frente = jogo["pilotos"][i]["distancia"] + random.randint(150, 200)
            cria_carro(carros, frente, random.randint(0, 3))
    menor_distancia = jogo["pilotos"][0]["distancia"]
    for piloto in jogo["pilotos"]:
        menor_distancia = min(menor_distancia, piloto["distancia"])
    mantidos = []
    for carro in carros:
        if carro["distancia"] > menor_distancia - 140:
            mantidos.append(carro)
    jogo["carros"] = mantidos


def registra_batida(piloto, fator):
    piloto["velocidade"] *= fator
    piloto["sem_bater"] = 0
    piloto["nitro"] = 0
    piloto["fechando"] = 0
    piloto["protecao"] = 1.1
    piloto["batidas"] += 1


def verifica_colisoes(pilotos, carros):
    for piloto in pilotos:
        if piloto["protecao"] == 0:
            for carro in carros:
                lateral = abs(piloto["x"] - carro["x"]) < 0.09
                longitudinal = abs(piloto["distancia"] - carro["distancia"]) < 3.3
                if lateral and longitudinal:
                    registra_batida(piloto, 0.4)
                    break
    for i in range(len(pilotos)):
        for j in range(i + 1, len(pilotos)):
            a = pilotos[i]
            b = pilotos[j]
            lateral = abs(a["x"] - b["x"]) < 0.075
            longitudinal = abs(a["distancia"] - b["distancia"]) < 2
            if lateral and longitudinal and a["protecao"] == 0 and b["protecao"] == 0:
                fator_a = 0.8
                fator_b = 0.8
                if a["fechando"] > 0:
                    fator_a = 0.93
                    fator_b = 0.67
                elif b["fechando"] > 0:
                    fator_a = 0.67
                    fator_b = 0.93
                direcao = 1
                if b["x"] < a["x"]:
                    direcao = -1
                a["x"] = max(0.04, min(0.96, a["x"] - direcao * 0.04))
                b["x"] = max(0.04, min(0.96, b["x"] + direcao * 0.04))
                registra_batida(a, fator_a)
                registra_batida(b, fator_b)

def classificacao(pilotos):
    # Seleciona o mais distante, guarda e repete. São só cinco pilotos.
    restantes = pilotos[:]
    ordem = []
    while len(restantes) > 0:
        maior = restantes[0]
        for piloto in restantes:
            if piloto["distancia"] > maior["distancia"]:
                maior = piloto
        ordem.append(maior)
        restantes.remove(maior)
    return ordem