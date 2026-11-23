"""Lê os dados dos estudantes e produz uma cópia para o desenho da V6.

Nenhuma velocidade, posição, colisão ou regra é atualizada neste arquivo.
"""
from . import config_visual as config


def contexto_visual():
    return {"jogo_id": None, "historico": {}, "tempo_anterior": 0,
            "ultima_corrida": None}


def adapta_corrida(jogo, ordem, estado):
    if estado["jogo_id"] != id(jogo):
        estado["jogo_id"] = id(jogo)
        estado["historico"] = {}
        estado["tempo_anterior"] = jogo["tempo"]
    dt = max(0, jogo["tempo"] - estado["tempo_anterior"])
    corrida = {"stage": config.STAGES[jogo["fase"]], "elapsed": jogo["tempo"],
               "countdown": jogo.get("contagem", 0), "riders": [], "players": [],
               "traffic": [], "order": [], "section": config.music_section(jogo["tempo"], jogo["fase"])}
    mapa = {}
    for piloto in jogo["pilotos"]:
        marca = piloto["marca"]
        anterior = estado["historico"].get(marca)
        inclinacao = 0
        mensagem = ""
        ate = 0
        if anterior is not None:
            inclinacao = anterior["lean"]
            mensagem, ate = anterior["message"], anterior["ate"]
            if dt > 0:
                alvo = 0
                if piloto["x"] - anterior["x"] > 0.00001:
                    alvo = 13
                elif piloto["x"] - anterior["x"] < -0.00001:
                    alvo = -13
                if piloto.get("fechando", 0) > 0:
                    alvo = piloto.get("direcao_fechada", 0) * 18
                inclinacao += (alvo - inclinacao) * min(1, dt * 10)
            if piloto["batidas"] > anterior["crashes"]:
                mensagem, ate = "BATIDA!", jogo["tempo"] + 1
            elif piloto["nitro"] > 0 and anterior["boost"] == 0:
                mensagem, ate = "NITRO!", jogo["tempo"] + 1.2
        elif piloto["nitro"] > 0:
            mensagem, ate = "NITRO!", jogo["tempo"] + 1.2
        visual = {"name": piloto["nome"], "brand": marca, "color": tuple(piloto["cor"]),
                  "human": piloto["humano"], "x": piloto["x"], "distance": piloto["distancia"],
                  "speed": piloto["velocidade"], "boost_time": piloto["nitro"],
                  "clean_time": piloto["sem_bater"], "crashes": piloto["batidas"],
                  "cooldown": piloto.get("protecao", 0), "lean": inclinacao,
                  "boost_ready": piloto["sem_bater"] >= config.BOOST_CHARGE - 0.000001 and piloto["nitro"] <= 0,
                  "message": mensagem, "message_time": max(0, ate - jogo["tempo"])}
        corrida["riders"].append(visual)
        mapa[id(piloto)] = visual
        if piloto["humano"]:
            corrida["players"].append(visual)
        estado["historico"][marca] = {"x": piloto["x"], "lean": inclinacao,
                                          "crashes": piloto["batidas"], "boost": piloto["nitro"],
                                          "message": mensagem, "ate": ate}
    for piloto in ordem:
        corrida["order"].append(mapa[id(piloto)])
    cores = [(201, 92, 75), (219, 190, 105), (100, 148, 177)]
    for carro in jogo["carros"]:
        destino = carro.get("destino")
        alvo = None
        if destino is not None:
            alvo = config.LANES[destino]
        corrida["traffic"].append({"x": carro["x"], "distance": carro["distancia"],
                                   "speed": carro["velocidade"], "kind": carro.get("imagem", 0),
                                   "color": cores[carro.get("imagem", 0) % len(cores)], "target_x": alvo})
    estado["tempo_anterior"] = jogo["tempo"]
    estado["ultima_corrida"] = corrida
    return corrida


def nome_musica(fase):
    return ["SIX DAYS - REMIX / LOCAL", "TRILHA DO DESERTO / LOCAL", "TOKYO DRIFT / LOCAL"][fase]
