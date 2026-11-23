"""Inicialização adicional: reutiliza as funções de jogo dos arquivos existentes.

Este arquivo coordena somente a janela, os eventos e a escolha das telas.
A criação do mundo, o avanço da corrida e a classificação vêm do projeto do grupo.
"""
import importlib
import sys
from pathlib import Path
import pygame
from . import config_visual as config
from . import desenhos_v6
from .adaptacao import contexto_visual
from .camada_visual import cria_contexto, desenha_menu, desenha_corrida, desenha_resultado


def importa_arquivo(pasta, nomes):
    for nome in nomes:
        for arquivo in pasta.iterdir():
            if arquivo.is_file() and arquivo.suffix == ".py" and arquivo.stem.lower() == nome:
                return importlib.import_module(arquivo.stem)
    raise RuntimeError("Não encontrei um dos arquivos do projeto: " + ", ".join(nomes) +
                       ". Coloque o iniciador ao lado dos arquivos atuais do jogo.")


def carrega_projeto(pasta):
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(pasta))
    base = importa_arquivo(pasta, ["main", "principal"])
    pilotos = importa_arquivo(pasta, ["pilotos", "piloto"])
    transito = importa_arquivo(pasta, ["transito"])
    telas = importa_arquivo(pasta, ["telas", "tela"])
    for nome in ["cria_jogo", "passo_jogo"]:
        if not callable(getattr(base, nome, None)):
            raise RuntimeError("O arquivo principal precisa ter a função " + nome +
                               ". Este complemento foi feito para a estrutura do guia e dos trechos enviados.")
    config.DURATION = getattr(base, "DURACAO", 90)
    config.BOOST_CHARGE = getattr(pilotos, "CARGA_NITRO", 15)
    config.BOOST_DURATION = getattr(pilotos, "DURACAO_NITRO", 3)
    desenhos_v6.BOOST_DURATION = config.BOOST_DURATION
    desenhos_v6.DURATION = config.DURATION
    return {"base": base, "pilotos": pilotos, "transito": transito, "telas": telas}


def cria_corrida(projeto, quantidade, fase, mudo):
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
    jogo = projeto["base"].cria_jogo(quantidade, fase)
    jogo["mudo"] = mudo
    # Valida o formato em vez de modificar o conteúdo ou tentar adivinhar campos.
    for chave in ["pilotos", "carros", "tempo", "contagem", "pausado", "quantidade", "fase"]:
        if chave not in jogo:
            raise RuntimeError("O dicionário da corrida não tem o campo esperado: " + chave)
    return jogo


def comandos_atuais(projeto, quantidade):
    teclas = pygame.key.get_pressed()
    le = projeto["pilotos"].le_comando
    comandos = []
    if quantidade == 1:
        if teclas[pygame.K_w] or teclas[pygame.K_s] or teclas[pygame.K_a] or teclas[pygame.K_d]:
            comandos.append(le(teclas, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d))
        else:
            comandos.append(le(teclas, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT))
    else:
        comandos.append(le(teclas, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d))
        comandos.append(le(teclas, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT))
    return comandos


def quadro(projeto, jogo, comandos, dt, contexto, estado_visual):
    # São as funções existentes dos estudantes, chamadas exatamente uma vez.
    projeto["base"].passo_jogo(jogo, comandos, dt)
    ordem = projeto["transito"].classificacao(jogo["pilotos"])
    desenha_corrida(contexto, jogo, ordem, estado_visual)
    return ordem


def executar(pasta):
    projeto = carrega_projeto(Path(pasta))
    pygame.init()
    janela = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Entrega no Grau | Visual original V6 adicional")
    canvas = pygame.Surface((config.WIDTH, config.HEIGHT))
    contexto = cria_contexto(canvas)
    estado_visual = contexto_visual()
    relogio = pygame.time.Clock()
    estado = "menu"
    quantidade, fase = 1, 0
    mudo = False
    jogo = None
    aberto = True
    segundos = 0
    viewport = pygame.Rect(0, 0, config.WIDTH, config.HEIGHT)
    while aberto:
        dt = min(relogio.tick(60) / 1000, .05)
        segundos += dt
        mx, my = pygame.mouse.get_pos()
        contexto["mouse"] = ((mx - viewport.x) * config.WIDTH / viewport.w,
                              (my - viewport.y) * config.HEIGHT / viewport.h)
        for evento in pygame.event.get():
            acao = None
            if evento.type == pygame.QUIT:
                aberto = False
            elif evento.type == pygame.WINDOWFOCUSLOST:
                if estado == "corrida":
                    jogo["pausado"] = True
                    projeto["telas"].pausa_som(True)
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse = ((evento.pos[0] - viewport.x) * config.WIDTH / viewport.w,
                         (evento.pos[1] - viewport.y) * config.HEIGHT / viewport.h)
                if viewport.collidepoint(evento.pos):
                    for retangulo, opcao in contexto["buttons"]:
                        if retangulo.collidepoint(mouse):
                            acao = opcao
                            break
            elif evento.type == pygame.KEYDOWN:
                tecla = evento.key
                if tecla == pygame.K_m:
                    mudo = not mudo
                    if jogo is not None:
                        jogo["mudo"] = mudo
                    projeto["telas"].muda_volume(mudo)
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
                        acao = "start"
                    elif tecla == pygame.K_ESCAPE:
                        aberto = False
                elif estado == "corrida":
                    if tecla in [pygame.K_p, pygame.K_ESCAPE]:
                        acao = "pause"
                    elif not jogo["pausado"] and jogo["contagem"] == 0:
                        if tecla == pygame.K_LSHIFT or (quantidade == 1 and tecla == pygame.K_SPACE):
                            projeto["pilotos"].ativa_nitro(jogo["pilotos"][0])
                        elif tecla == pygame.K_f:
                            projeto["pilotos"].inicia_fechada(jogo["pilotos"][0], jogo["pilotos"])
                        elif quantidade == 2 and tecla == pygame.K_RSHIFT:
                            projeto["pilotos"].ativa_nitro(jogo["pilotos"][1])
                        elif quantidade == 2 and tecla == pygame.K_RETURN:
                            projeto["pilotos"].inicia_fechada(jogo["pilotos"][1], jogo["pilotos"])
                elif estado == "resultado":
                    if tecla == pygame.K_RETURN:
                        acao = "start"
                    elif tecla == pygame.K_n:
                        acao = "next"
                    elif tecla == pygame.K_ESCAPE:
                        acao = "menu"
            if acao is not None:
                if acao in ["start", "next"]:
                    if acao == "next":
                        fase = (fase + 1) % 3
                    jogo = cria_corrida(projeto, quantidade, fase, mudo)
                    estado_visual = contexto_visual()
                    estado = "corrida"
                    contexto["buttons"] = []
                elif acao == "pause" and estado == "corrida":
                    jogo["pausado"] = not jogo["pausado"]
                    projeto["telas"].pausa_som(jogo["pausado"])
                elif acao == "menu":
                    estado = "menu"
                    contexto["buttons"] = []
                    if pygame.mixer.get_init():
                        pygame.mixer.music.stop()
                elif acao.startswith("mode:"):
                    quantidade = int(acao.split(":")[1])
                elif acao.startswith("stage:"):
                    fase = int(acao.split(":")[1])
        if estado == "menu":
            desenha_menu(contexto, quantidade, fase, segundos)
        elif estado == "corrida":
            quadro(projeto, jogo, comandos_atuais(projeto, quantidade), dt, contexto, estado_visual)
            if jogo["tempo"] >= config.DURATION:
                projeto["telas"].toca_chegada()
                projeto["telas"].muda_volume(mudo)
                estado = "resultado"
        else:
            ordem = projeto["transito"].classificacao(jogo["pilotos"])
            desenha_resultado(contexto, jogo, ordem, estado_visual)
        largura, altura = janela.get_size()
        escala = min(largura / config.WIDTH, altura / config.HEIGHT)
        tamanho = (max(1, int(config.WIDTH * escala)), max(1, int(config.HEIGHT * escala)))
        viewport = pygame.Rect((largura - tamanho[0]) // 2, (altura - tamanho[1]) // 2, *tamanho)
        janela.fill((6, 10, 17))
        imagem = canvas
        if tamanho != canvas.get_size():
            imagem = pygame.transform.smoothscale(canvas, tamanho)
        janela.blit(imagem, viewport)
        pygame.display.flip()
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
    pygame.quit()
