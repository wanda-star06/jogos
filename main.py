
import pygame
import sys
import random
import time

pygame.init()

# Definindo as cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# Configurações da tela
LARGURA_TELA = 800
ALTURA_TELA = 600
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("pega_pega")

# Variáveis globais
PONTUACAO = 0
FASE_ATUAL = 1
NUM_INIMIGOS = 2
TEMPO_POR_FASE = 20
TEMPO_ESPERA_ATAQUE = 1500
FPS = 60
CLOCK = pygame.time.Clock()

# Função para desenhar o texto na tela
def desenhar_texto(texto, tamanho, cor, x, y):
    fonte = pygame.font.SysFont("arial", tamanho)
    texto_renderizado = fonte.render(texto, True, cor)
    TELA.blit(texto_renderizado, (x, y))

# Função para exibir a tela de abertura
def tela_abertura():
    TELA.fill(PRETO)
    desenhar_texto("bem vindo ao pega_pega", 48, BRANCO, 100, 200)
    pygame.draw.rect(TELA, BRANCO, (300, 300, 200, 50))
    desenhar_texto("play game", 36, PRETO, 320, 310)
    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if 300 <= x <= 500 and 300 <= y <= 350:
                    return

# Função principal
def jogo():
    global PONTUACAO, FASE_ATUAL, NUM_INIMIGOS

    jogador_posicao = [LARGURA_TELA // 2, ALTURA_TELA // 2]
    equipamento_coletado = False
    ataque_realizado = False
    itens = []

    inimigos = []
    for _ in range(NUM_INIMIGOS):
        inimigos.append([random.randint(50, LARGURA_TELA - 50), random.randint(50, ALTURA_TELA - 50)])

    tempo_inicial = time.time()
    tempo_anterior_item = tempo_inicial

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LSHIFT or evento.key == pygame.K_RSHIFT:
                    if equipamento_coletado and not ataque_realizado:
                        desenhar_texto("Ataque realizado! Inimigo derrotado.", 25, BRANCO, 250, 250)
                        pygame.display.flip()
                        pygame.time.delay(TEMPO_ESPERA_ATAQUE)
                        ataque_realizado = True
                        PONTUACAO += 10

        # Movimentação dos inimigos
        for i in range(NUM_INIMIGOS):
            inimigos[i][0] += random.choice([-1, 1])
            inimigos[i][1] += random.choice([-1, 1])

            # Correção para garantir que os inimigos permaneçam na tela
            inimigos[i][0] = max(0, min(LARGURA_TELA - 20, inimigos[i][0]))
            inimigos[i][1] = max(0, min(ALTURA_TELA - 20, inimigos[i][1]))

            # Colisão do jogador com inimigo
            if (
                jogador_posicao[0] < inimigos[i][0] + 20
                and jogador_posicao[0] + 20 > inimigos[i][0]
                and jogador_posicao[1] < inimigos[i][1] + 20
                and jogador_posicao[1] + 20 > inimigos[i][1]
            ):
                print("Você foi atingido! Game Over.")
                pygame.quit()
                sys.exit()

        # Criação de itens
        tempo_atual = time.time()
        if tempo_atual - tempo_anterior_item > 5:  # Cria um novo item a cada 5 segundos
            novo_item = [random.randint(50, LARGURA_TELA - 50), random.randint(50, ALTURA_TELA - 50)]
            itens.append(novo_item)
            tempo_anterior_item = tempo_atual

        # Colisão do jogador com itens
        for item in itens:
            if (
                jogador_posicao[0] < item[0] + 20
                and jogador_posicao[0] + 20 > item[0]
                and jogador_posicao[1] < item[1] + 20
                and jogador_posicao[1] + 20 > item[1]
            ):
                itens.remove(item)
                equipamento_coletado = True
                desenhar_texto("Item coletado! Agora pressione SHIFT para atacar.", 25, VERMELHO

, 150, 250)

        # Atualização do jogo
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and jogador_posicao[0] > 0:
            jogador_posicao[0] -= 5
        if keys[pygame.K_RIGHT] and jogador_posicao[0] < LARGURA_TELA - 20:
            jogador_posicao[0] += 5
        if keys[pygame.K_UP] and jogador_posicao[1] > 0:
            jogador_posicao[1] -= 5
        if keys[pygame.K_DOWN] and jogador_posicao[1] < ALTURA_TELA - 20:
            jogador_posicao[1] += 5

        # Verifica se o tempo da fase acabou
        tempo_passado = tempo_atual - tempo_inicial

        if tempo_passado >= TEMPO_POR_FASE:
            FASE_ATUAL += 1
            PONTUACAO += 50
            NUM_INIMIGOS += 2
            equipamento_coletado = False
            ataque_realizado = False
            inimigos = []
            for _ in range(NUM_INIMIGOS):
                inimigos.append([random.randint(50, LARGURA_TELA - 50), random.randint(50, ALTURA_TELA - 50)])
            tempo_inicial = time.time()

        # Desenhando elementos
        TELA.fill(PRETO)
        desenhar_texto(f"Fase {FASE_ATUAL}", 40, BRANCO, 300, 50)
        desenhar_texto(f"Pontuação: {PONTUACAO}", 20, BRANCO, 10, 10)

        for i in range(NUM_INIMIGOS):
            pygame.draw.rect(TELA, BRANCO, (inimigos[i][0], inimigos[i][1], 20, 20))

        pygame.draw.circle(TELA, BRANCO, (jogador_posicao[0], jogador_posicao[1]), 20)

        for item in itens:
            pygame.draw.rect(TELA, VERMELHO, (item[0], item[1], 20, 20))

        if not equipamento_coletado:
            desenhar_texto("Passe sobre o item para coletá-lo.", 25, BRANCO, 150, 200)
            pygame.draw.rect(TELA, VERMELHO, (jogador_posicao[0] - 25, jogador_posicao[1] - 25, 50, 50))

        pygame.display.flip()
        CLOCK.tick(FPS)

# Executando o jogo
tela_abertura()
jogo()
