import pygame
import Piloto
import Transito
import Telas   
from Configuracoes import LARGURA, ALTURA, DURACAO


def cria_jogo(quantidade, fase):
    jogo = {"quantidade": quantidade, "fase": fase, "tempo": 0,
            "contagem": 3, "pausado": False, "mudo": False,
            "pilotos": Piloto.cria_pilotos(quantidade),
            "carros": [], "novo_carro": 0}
    for distancia in range(100, 401, 40):
        Transito.cria_carro(jogo["carros"], distancia, (distancia // 40) % 4)
    return jogo


def passo_jogo(jogo, comandos, dt):
    if jogo["pausado"] or jogo["tempo"] >= DURACAO:
        return
    if jogo["contagem"] > 0:
        jogo["contagem"] = max(0, jogo["contagem"] - dt)
        if jogo["contagem"] < 0.000001:
            jogo["contagem"] = 0
            Telas.toca_musica(jogo["fase"])
            Telas.muda_volume(jogo["mudo"])
        return
    # Atualiza o mundo UMA vez. As câmeras só desenham o resultado.
    falta = min(dt, DURACAO - jogo["tempo"])
    while falta > 0.00000001:
        passo = min(falta, 1 / 120)
        Piloto.atualiza_pilotos(jogo["pilotos"], jogo["carros"], comandos, jogo["fase"], passo)
        Transito.atualiza_transito(jogo, passo)
        Transito.verifica_colisoes(jogo["pilotos"], jogo["carros"])
        jogo["tempo"] += passo
        falta -= passo
    if DURACAO - jogo["tempo"] < 0.000001:
        jogo["tempo"] = DURACAO


def principal():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Entrega no Grau | Cópia didática em 3 partes")
    relogio = pygame.time.Clock()
    recursos = Telas.carrega_recursos()
    estado = "menu"
    quantidade = 1
    fase = 0
    mudo = False
    jogo = None
    aberto = True
    while aberto:
        dt = min(relogio.tick(60) / 1000, 0.05)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                aberto = False
            elif evento.type == pygame.WINDOWFOCUSLOST:
                if estado == "corrida":
                    jogo["pausado"] = True
                    Telas.pausa_som(True)
            elif evento.type == pygame.KEYDOWN:
                tecla = evento.key
                if tecla == pygame.K_m:
                    mudo = not mudo
                    if jogo is not None:
                        jogo["mudo"] = mudo
                    Telas.muda_volume(mudo)
                elif estado == "menu":
                    if tecla == pygame.K_1:
                        quantidade = 1
                    elif tecla == pygame.K_2:
                        quantidade = 2
                    elif tecla == pygame.K_LEFT:
                        fase = (fase - 1) % 3
                    elif tecla == pygame.K_RIGHT:
                        fase = (fase + 1) % 3
                    elif tecla in [pygame.K_RETURN, pygame.K_SPACE]:
                        jogo = cria_jogo(quantidade, fase)
                        jogo["mudo"] = mudo
                        estado = "corrida"
                    elif tecla == pygame.K_ESCAPE:
                        aberto = False
                elif estado == "corrida":
                    if tecla in [pygame.K_p, pygame.K_ESCAPE]:
                        jogo["pausado"] = not jogo["pausado"]
                        Telas.pausa_som(jogo["pausado"])
                    elif not jogo["pausado"] and jogo["contagem"] == 0:
                        if tecla == pygame.K_LSHIFT or (quantidade == 1 and tecla == pygame.K_SPACE):
                            Piloto.ativa_nitro(jogo["pilotos"][0])
                        elif tecla == pygame.K_f:
                            Piloto.inicia_fechada(jogo["pilotos"][0], jogo["pilotos"])
                        elif quantidade == 2 and tecla == pygame.K_RSHIFT:
                            Piloto.ativa_nitro(jogo["pilotos"][1])
                        elif quantidade == 2 and tecla == pygame.K_RETURN:
                            Piloto.inicia_fechada(jogo["pilotos"][1], jogo["pilotos"])
                elif estado == "resultado":
                    if tecla == pygame.K_ESCAPE:
                        estado = "menu"
                        if pygame.mixer.get_init() is not None:
                            pygame.mixer.music.stop()
                    elif tecla in [pygame.K_RETURN, pygame.K_n]:
                        if tecla == pygame.K_n:
                            fase = (fase + 1) % 3
                        jogo = cria_jogo(quantidade, fase)
                        jogo["mudo"] = mudo
                        estado = "corrida"
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if estado == "menu":
                    if pygame.Rect(64, 352, 427, 68).collidepoint(evento.pos):
                        jogo = cria_jogo(quantidade, fase)
                        jogo["mudo"] = mudo
                        estado = "corrida"
        if estado == "menu":
            Telas.desenha_menu(tela, quantidade, fase, recursos)
        elif estado == "corrida":
            teclas = pygame.key.get_pressed()
            comandos = []
            if quantidade == 1:
                if teclas[pygame.K_w] or teclas[pygame.K_s] or teclas[pygame.K_a] or teclas[pygame.K_d]:
                    comandos.append(Piloto.le_comando(teclas, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d))
                else:
                    comandos.append(Piloto.le_comando(teclas, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT))
            else:
                comandos.append(Piloto.le_comando(teclas, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d))
                comandos.append(Piloto.le_comando(teclas, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT))
            passo_jogo(jogo, comandos, dt)
            ordem = Transito.classificacao(jogo["pilotos"])
            Telas.desenha_corrida(tela, jogo, recursos, ordem)
            if jogo["tempo"] >= DURACAO:
                Telas.toca_chegada()
                Telas.muda_volume(mudo)
                estado = "resultado"
        else:
            ordem = Transito.classificacao(jogo["pilotos"])
            Telas.desenha_resultado(tela, ordem, recursos)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    principal()