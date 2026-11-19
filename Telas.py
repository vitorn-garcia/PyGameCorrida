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

