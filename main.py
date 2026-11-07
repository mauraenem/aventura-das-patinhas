import pygame
from pathlib import Path

# 1. Inicializar o Pygame
pygame.init()
# Localizar a pasta do jogo
PASTA_PROJETO = Path(__file__).resolve().parent

# Carregar o efeito sonoro do petisco
som_petisco = pygame.mixer.Sound(
    str(PASTA_PROJETO / "sons" / "petisco.mp3")
)

# Volume de 50%
som_petisco.set_volume(0.5)
# Som de latido na escolha da cachorrinha
som_latido = pygame.mixer.Sound(
    str(PASTA_PROJETO / "sons" / "latido.mp3")
)

som_latido.set_volume(0.5)
# Sons de vitoria e derrota
som_vitoria = pygame.mixer.Sound(
    str(PASTA_PROJETO / "sons" / "vitoria.mp3")
)

som_derrota = pygame.mixer.Sound(
    str(PASTA_PROJETO / "sons" / "derrota.mp3")
)

som_vitoria.set_volume(0.5)
som_derrota.set_volume(0.5)

# 2. Janela e configuracoes
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Aventura das Patinhas - Em Busca dos Petiscos")
relogio = pygame.time.Clock()

# 3. Cores
VERDE = (100, 180, 100)
PRETO = (30, 30, 30)
BEGE = (245, 215, 180)
VERMELHO = (220, 70, 70)
BRANCO = (255, 255, 255)
TINA_PELO = (105, 70, 48)
TINA_LISTRAS = (48, 34, 28)
NEM_PELO = (215, 177, 125)
NEM_LISTRAS = (150, 112, 77)

# 4. Dados do jogo
TEMPO_LIMITE = 30
velocidade = 5
raio = 30
posicao_x, posicao_y = 400, 300
POSICOES_PETISCOS = [(100, 100), (650, 120), (200, 450), (600, 400), (400, 180)]
petiscos = POSICOES_PETISCOS.copy()
pontos = 0
inicio_jogo = 0
estado_jogo = "menu"  # menu, selecao, jogando, vitoria, derrota
cachorrinha_escolhida = "Tina"
casinha = pygame.Rect(680, 450, 100, 100)

# 5. Fontes
fonte = pygame.font.SysFont("Arial", 28)
fonte_titulo = pygame.font.SysFont("Arial", 42, bold=True)
fonte_menu = pygame.font.SysFont("Arial", 30, bold=True)
fonte_instrucoes = pygame.font.SysFont("Arial", 22)


def escrever(texto, fonte_usada, cor, centro):
    imagem = fonte_usada.render(texto, True, cor)
    tela.blit(imagem, imagem.get_rect(center=centro))


def desenhar_cachorrinha(x, y, nome=None):
    """Desenha a Tina (escura) ou a Nem (clara)."""
    if nome is None:
        nome = cachorrinha_escolhida

    if nome == "Tina":
        cor_pelo, cor_listras = TINA_PELO, TINA_LISTRAS
    else:
        cor_pelo, cor_listras = NEM_PELO, NEM_LISTRAS

    x, y = int(x), int(y)
    # Orelhas
    pygame.draw.ellipse(tela, cor_listras, (x - 30, y - 40, 22, 40))
    pygame.draw.ellipse(tela, cor_listras, (x + 8, y - 40, 22, 40))
    # Cabeca
    pygame.draw.circle(tela, cor_pelo, (x, y), raio)
    # Pequenas listras tigradas
    pygame.draw.line(tela, cor_listras, (x - 18, y - 20), (x - 9, y - 12), 4)
    pygame.draw.line(tela, cor_listras, (x + 18, y - 20), (x + 9, y - 12), 4)
    pygame.draw.line(tela, cor_listras, (x - 4, y - 27), (x, y - 18), 3)
    # Olhos, focinho, nariz e coleira
    pygame.draw.circle(tela, PRETO, (x - 12, y - 5), 4)
    pygame.draw.circle(tela, PRETO, (x + 12, y - 5), 4)
    pygame.draw.ellipse(tela, BEGE, (x - 15, y + 5, 30, 20))
    pygame.draw.circle(tela, PRETO, (x, y + 12), 5)
    pygame.draw.rect(tela, VERMELHO, (x - 20, y + 26, 40, 6))


def desenhar_petisco(x, y):
    cor = (160, 90, 40)
    pygame.draw.circle(tela, cor, (x, y), 10)
    for deslocamento_x in (-12, 12):
        for deslocamento_y in (-7, 7):
            pygame.draw.circle(tela, cor, (x + deslocamento_x, y + deslocamento_y), 6)


def desenhar_casinha():
    pygame.draw.rect(tela, (230, 190, 130), casinha)
    pygame.draw.polygon(tela, (170, 65, 45), [
        (casinha.x - 10, casinha.y),
        (casinha.centerx, casinha.y - 45),
        (casinha.right + 10, casinha.y)
    ])
    pygame.draw.rect(tela, (90, 55, 30),
                     (casinha.x + 35, casinha.y + 45, 30, 55))


def desenhar_menu():
    tela.fill(VERDE)
    escrever("AVENTURA DAS PATINHAS", fonte_titulo, PRETO, (400, 130))
    escrever("Em Busca dos Petiscos", fonte_menu, PRETO, (400, 200))

    pygame.draw.rect(tela, (40, 120, 60), (280, 270, 240, 60), border_radius=12)
    escrever("ENTER - JOGAR", fonte_menu, BRANCO, (400, 300))

    pygame.draw.rect(tela, (170, 60, 60), (280, 350, 240, 60), border_radius=12)
    escrever("ESC - SAIR", fonte_menu, BRANCO, (400, 380))
    escrever("SETAS - Movimentar a cachorrinha", fonte_instrucoes, PRETO, (400, 470))
    escrever("Colete 5 petiscos e volte para a casinha!", fonte_instrucoes, PRETO, (400, 510))


def desenhar_selecao():
    tela.fill(VERDE)
    escrever("ESCOLHA SUA CACHORRINHA", fonte_titulo, PRETO, (400, 110))
    desenhar_cachorrinha(240, 265, "Tina")
    desenhar_cachorrinha(560, 265, "Nem")
    escrever("1 - TINA", fonte_menu, PRETO, (240, 340))
    escrever("Tigrada escura", fonte_instrucoes, PRETO, (240, 380))
    escrever("2 - NEM", fonte_menu, PRETO, (560, 340))
    escrever("Tigrada clara", fonte_instrucoes, PRETO, (560, 380))
    escrever("ESC - Voltar ao menu", fonte_instrucoes, PRETO, (400, 490))


def reiniciar_jogo():
    global posicao_x, posicao_y, petiscos, pontos, inicio_jogo, estado_jogo
    posicao_x, posicao_y = 400, 300
    petiscos = POSICOES_PETISCOS.copy()
    pontos = 0
    inicio_jogo = pygame.time.get_ticks()
    estado_jogo = "jogando"


def desenhar_partida(tempo_restante):
    tela.fill(VERDE)
    desenhar_cachorrinha(posicao_x, posicao_y)
    for petisco in petiscos:
        desenhar_petisco(petisco[0], petisco[1])
    desenhar_casinha()

    texto_pontos = fonte.render(f"Pontos: {pontos}", True, PRETO)
    tela.blit(texto_pontos, (20, 20))
    texto_tempo = fonte.render(f"Tempo: {tempo_restante}s", True, PRETO)
    tela.blit(texto_tempo, (620, 20))

    if estado_jogo in ("vitoria", "derrota"):
        if estado_jogo == "vitoria":
            mensagem = "VITORIA! Todos os petiscos coletados!"
        else:
            mensagem = "TEMPO ESGOTADO! Voce perdeu!"

        pygame.draw.rect(tela, (40, 80, 45), (50, 245, 700, 130), border_radius=12)
        escrever(mensagem, fonte_menu, BRANCO, (400, 285))
        escrever("R - Jogar novamente     M - Menu", fonte_instrucoes,
                 BRANCO, (400, 340))


# 6. Loop principal
jogo_rodando = True
tempo_restante = TEMPO_LIMITE

while jogo_rodando:
    # Eventos: teclas pressionadas uma vez e fechar janela
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_rodando = False

        elif evento.type == pygame.KEYDOWN:
            if estado_jogo == "menu":
                if evento.key == pygame.K_RETURN:
                    estado_jogo = "selecao"
                elif evento.key == pygame.K_ESCAPE:
                    jogo_rodando = False

            elif estado_jogo == "selecao":
                if evento.key == pygame.K_1:
                    cachorrinha_escolhida = "Tina"
                    som_latido.play()
                    reiniciar_jogo()
                elif evento.key == pygame.K_2:
                    cachorrinha_escolhida = "Nem"
                    som_latido.play()
                    reiniciar_jogo()
                elif evento.key == pygame.K_ESCAPE:
                    estado_jogo = "menu"

            elif estado_jogo in ("vitoria", "derrota"):
                if evento.key == pygame.K_r:
                    reiniciar_jogo()
                elif evento.key == pygame.K_m:
                    estado_jogo = "menu"

    # Movimento e regras so funcionam durante a partida
    if estado_jogo == "jogando":
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            posicao_x -= velocidade
        if teclas[pygame.K_RIGHT]:
            posicao_x += velocidade
        if teclas[pygame.K_UP]:
            posicao_y -= velocidade
        if teclas[pygame.K_DOWN]:
            posicao_y += velocidade

        posicao_x = max(raio, min(posicao_x, LARGURA - raio))
        posicao_y = max(raio + 10, min(posicao_y, ALTURA - raio - 10))

        tempo_passado = (pygame.time.get_ticks() - inicio_jogo) // 1000
        tempo_restante = max(0, TEMPO_LIMITE - tempo_passado)

        if tempo_restante == 0:
            estado_jogo = "derrota"
            som_derrota.play()
        else:
            # A copia evita modificar a lista que esta sendo percorrida
            for petisco in petiscos[:]:
                petisco_x, petisco_y = petisco
                distancia = ((posicao_x - petisco_x) ** 2 +
                             (posicao_y - petisco_y) ** 2) ** 0.5
                if distancia < raio + 10:
                    petiscos.remove(petisco)
                    pontos += 10
                    som_petisco.play()

            if not petiscos:
                jogador_rect = pygame.Rect(posicao_x - raio, posicao_y - raio,
                                           raio * 2, raio * 2)
                if jogador_rect.colliderect(casinha):
                    estado_jogo = "vitoria"
                    som_vitoria.play()

    # Cada estado desenha apenas sua propria tela
    if estado_jogo == "menu":
        desenhar_menu()
    elif estado_jogo == "selecao":
        desenhar_selecao()
    else:
        desenhar_partida(tempo_restante)

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
