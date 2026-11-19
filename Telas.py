"""PARTE 3: desenho, perspectiva, menus, tela dividida, música e grau."""
import os
import pygame 
from Configuracoes import PASTA, MARCAS, FAIXAS, FASES, MUSICAS, CEUS, CHAO, CARGA_NITRO, DURACAO

def carrega_recursos():
    recursos = {}
    nomes = ["titulo", "carro0", "carro1", "carro2"]
    for marca in MARCAS:
        nomes.append(marca)
        nomes.append(marca + "_grau")
    for nome in nomes:
        caminho = os.path.join(PASTA, "imagens", nome + ".png")
        recursos[nome] = pygame.image.load(caminho).convert_alpha()
    arquivo_fonte = os.path.join(PASTA, "imagens", "bold.ttf")
    recursos["pequena"] = pygame.font.Font(arquivo_fonte, 16)
    recursos["media"] = pygame.font.Font(arquivo_fonte, 22)
    recursos["grande"] = pygame.font.Font(arquivo_fonte, 36)
    return recursos

def escreve(tela, mensagem, x, y, fonte, cor):
    imagem = fonte.render(str(mensagem), True, cor)
    tela.blit(imagem, (x, y))


def projeta(x, distancia, observador, largura, altura):
    relativa = distancia - observador["distancia"]
    escala = 28 / (28 + relativa)
    largura_pista = min(largura * 1.35, 1250) * escala
    centro = largura / 2 - (observador["x"] - 0.5) * largura_pista * 0.46
    tela_x = centro + (x - 0.5) * largura_pista
    tela_y = altura * 0.29 + altura * 0.69 * escala
    return [tela_x, tela_y, largura_pista]

def desenha_pista(tela, observador, fase):
    largura = tela.get_width()
    altura = tela.get_height()
    horizonte = int(altura * 0.29)
    tela.fill(CEUS[fase])
    pygame.draw.rect(tela, CHAO[fase], (0, horizonte, largura, altura))
    pontos = []
    for x, distancia in [(0, 1200), (1, 1200), (1, 0), (0, 0)]:
        ponto = projeta(x, observador["distancia"] + distancia, observador, largura, altura)
        pontos.append((ponto[0], ponto[1]))
    pygame.draw.polygon(tela, (58, 60, 67), pontos)
    pygame.draw.lines(tela, (235, 224, 197), True, pontos, 3)
    deslocamento = observador["distancia"] % 16
    for i in range(24):
        distancia = i * 16 - deslocamento
        if distancia >= 0:
            for x in [0.25, 0.5, 0.75]:
                a = projeta(x, observador["distancia"] + distancia, observador, largura, altura)
                b = projeta(x, observador["distancia"] + distancia + 6, observador, largura, altura)
                pygame.draw.line(tela, (226, 222, 202), (a[0], a[1]), (b[0], b[1]), 2)

def distancia_para_desenho(objeto):
    return objeto["distancia"]


def desenha_visao(tela, jogo, observador, recursos, ordem):
    largura = tela.get_width()
    altura = tela.get_height()
    desenha_pista(tela, observador, jogo["fase"])
    objetos = jogo["carros"] + jogo["pilotos"]
    # Desenhe o fundo primeiro e a frente depois: uma moto próxima cobre a distante.
    objetos.sort(key=distancia_para_desenho, reverse=True)
    for objeto in objetos:
        relativa = objeto["distancia"] - observador["distancia"]
        if -4 < relativa < 520:
            ponto = projeta(objeto["x"], objeto["distancia"], observador, largura, altura)
            if objeto["tipo"] == "carro":
                nome = "carro" + str(objeto["imagem"])
                tamanho = int(ponto[2] * 0.118)
            else:
                nome = objeto["marca"]
                if objeto["nitro"] > 0:
                    nome += "_grau"
                tamanho = int(ponto[2] * 0.09)
            imagem = recursos[nome]
            tamanho = max(3, tamanho)
            altura_imagem = max(3, int(tamanho * imagem.get_height() / imagem.get_width()))
            imagem = pygame.transform.scale(imagem, (tamanho, altura_imagem))
            retangulo = imagem.get_rect(midbottom=(int(ponto[0]), int(ponto[1])))
            tela.blit(imagem, retangulo)
            if objeto["tipo"] == "carro" and objeto["destino"] is not None:
                if int(jogo["tempo"] * 5) % 2 == 0:
                    lado = -1
                    if FAIXAS[objeto["destino"]] > objeto["x"]:
                        lado = 1
                    pygame.draw.circle(tela, (255, 190, 45),
                                       (int(ponto[0] + lado * tamanho * 0.35), int(ponto[1] - tamanho * 0.24)), max(2, tamanho // 22))
    # A posição é pela distância no mundo, não pela altura do desenho na tela.
    posicao = ordem.index(observador) + 1
    pygame.draw.rect(tela, (19, 23, 31), (12, 12, 205, 104))
    escreve(tela, observador["nome"] + "   " + str(posicao) + "/5", 24, 20, recursos["media"], observador["cor"])
    escreve(tela, str(int(observador["velocidade"])) + " km/h", 24, 49, recursos["media"], (245, 240, 220))
    carga = str(int(observador["sem_bater"])) + "/" + str(CARGA_NITRO) + " s sem bater"
    if observador["sem_bater"] >= CARGA_NITRO:
        carga = "NITRO PRONTO"
    if observador["nitro"] > 0:
        carga = "NITRO / GRAU"
    escreve(tela, carga, 24, 81, recursos["pequena"], observador["cor"])
    pygame.draw.rect(tela, (58, 62, 73), (24, 107, 170, 4))
    pygame.draw.rect(tela, observador["cor"], (24, 107, int(170 * observador["sem_bater"] / CARGA_NITRO), 4))

def desenha_corrida(tela, jogo, recursos, ordem):
    tela.fill((18, 20, 24))
    escreve(tela, FASES[jogo["fase"]], 24, 15, recursos["media"], (255, 203, 46))
    escreve(tela, str(max(0, int(DURACAO - jogo["tempo"]))) + " segundos", 930, 15, recursos["media"], (245, 240, 220))
    largura = tela.get_width() // jogo["quantidade"]
    for i in range(jogo["quantidade"]):
        visao = tela.subsurface((i * largura, 60, largura - 2, 650))
        desenha_visao(visao, jogo, jogo["pilotos"][i], recursos, ordem)
    escreve(tela, "iFood: WASD / Shift esq / F     99: setas / Shift dir / Enter     P: pausa   M: som", 24, 727, recursos["pequena"], (200, 198, 184))
    if jogo["contagem"] > 0:
        escreve(tela, "LARGADA EM " + str(int(jogo["contagem"]) + 1), 450, 280, recursos["grande"], (255, 203, 46))
    if jogo["pausado"]:
        pygame.draw.rect(tela, (20, 21, 25), (420, 280, 360, 115))
        escreve(tela, "PAUSA", 530, 295, recursos["grande"], (255, 203, 46))
        escreve(tela, "P ou ESC para continuar", 455, 353, recursos["pequena"], (245, 240, 220))


def desenha_menu(tela, quantidade, fase, recursos):
    tela.fill((24, 25, 27))
    observador = {"x": 0.5, "distancia": 0}
    direita = tela.subsurface((520, 0, 680, 760))
    desenha_pista(direita, observador, fase)
    pygame.draw.polygon(tela, (24, 25, 27), [(0, 0), (705, 0), (535, 760), (0, 760)])
    pygame.draw.line(tela, (255, 203, 46), (705, 0), (535, 760), 3)
    tela.blit(recursos["titulo"], (55, 80))
    pygame.draw.polygon(tela, (255, 203, 46), [(77, 352), (491, 352), (478, 420), (64, 420)])
    escreve(tela, "JOGAR / ENTER", 88, 370, recursos["grande"], (24, 25, 27))
    escreve(tela, str(quantidade) + " JOGADOR(ES)   [1 / 2]", 68, 480, recursos["media"], (245, 240, 220))
    escreve(tela, "< " + FASES[fase] + " >", 68, 580, recursos["media"], (255, 203, 46))
    escreve(tela, "Setas: pista    Enter: jogar    Esc: sair", 68, 700, recursos["pequena"], (170, 168, 155))
    for marca, x in [("ifood", 730), ("99", 960)]:
        imagem = pygame.transform.scale(recursos[marca], (170, 267))
        tela.blit(imagem, (x, 420))


def desenha_resultado(tela, ordem, recursos):
    tela.fill((24, 25, 27))
    escreve(tela, "RESULTADO", 70, 55, recursos["grande"], (255, 203, 46))
    for i in range(len(ordem)):
        piloto = ordem[i]
        linha = str(i + 1) + ". " + piloto["nome"]
        linha += "    " + str(int(piloto["distancia"])) + " m"
        linha += "    Batidas: " + str(piloto["batidas"])
        escreve(tela, linha, 90, 160 + i * 75, recursos["media"], piloto["cor"])
    escreve(tela, "Enter: repetir    N: próxima fase    Esc: menu", 90, 630, recursos["media"], (245, 240, 220))

def toca_musica(fase):
    if pygame.mixer.get_init() is not None:
        pygame.mixer.music.load(os.path.join(PASTA, "musicas", MUSICAS[fase]))
        pygame.mixer.music.play(-1)


def toca_chegada():
    if pygame.mixer.get_init() is not None:
        pygame.mixer.music.load(os.path.join(PASTA, "musicas", "chegada_original.ogg"))
        pygame.mixer.music.play()


def pausa_som(pausado):
    if pygame.mixer.get_init() is not None:
        if pausado:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()


def muda_volume(mudo):
    if pygame.mixer.get_init() is not None:
        if mudo:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(0.72)
