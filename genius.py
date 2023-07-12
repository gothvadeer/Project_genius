import time
import pygame
import random
from pygame.locals import *

def escolher_cor_aleatoria():
    pisca_vermelho = {'cor': vermelho, 'posicao': (251, 282), 'raio': 130}
    pisca_verde = {'cor': verde, 'posicao': (251, 282), 'raio': 130}
    pisca_azul = {'cor': azul, 'posicao': (251, 282), 'raio': 130}
    pisca_laranja = {'cor': laranja, 'posicao': (251, 282), 'raio': 130}
    cores = [pisca_vermelho, pisca_verde, pisca_azul, pisca_laranja]
    return random.choice(cores)


def piscar_cores(lista_cores):
    for cor in lista_cores:
        if cor['cor'] == verde:
            pygame.draw.circle(interface, cor['cor'], cor['posicao'], cor['raio'], draw_top_right=True)
        elif cor['cor'] == vermelho:
            pygame.draw.circle(interface, cor['cor'], cor['posicao'], cor['raio'], draw_bottom_right=True)
        elif cor['cor'] == azul:
            pygame.draw.circle(interface, cor['cor'], cor['posicao'], cor['raio'], draw_top_left=True)
        elif cor['cor'] == laranja:
            pygame.draw.circle(interface, cor['cor'], cor['posicao'], cor['raio'], draw_bottom_left=True)
        pygame.display.update()
        time.sleep(0.4)
        interface.blit(fundo, (0, 30))
        pygame.display.update()
        time.sleep(0.4)

def obter_resposta(quantidade_cores):
    resposta_usuario = []
    while quantidade_cores > 0:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                quit()
            elif evento.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if botao_azul.collidepoint(mouse):
                    resposta_usuario.append(azul)
                    quantidade_cores -= 1
                elif botao_verde.collidepoint(mouse):
                    resposta_usuario.append(verde)
                    quantidade_cores -= 1
                elif botao_laranja.collidepoint(mouse):
                    resposta_usuario.append(laranja)
                    quantidade_cores -= 1
                elif botao_vermelho.collidepoint(mouse):
                    resposta_usuario.append(vermelho)
                    quantidade_cores -= 1
    return resposta_usuario

def restart():
    texto_jogar_novamente = fonte_botoes.render('RESTART', True, preto)
    interface.blit(fundo, (0, 30))
    botao_jogar_novamente = pygame.draw.rect(interface,branco, (175, 70, 155, 60))
    interface.blit(texto_jogar_novamente, (176, 73))
    pygame.display.update()
    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                quit()
            elif evento.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if botao_jogar_novamente.collidepoint(mouse):
                    interface.blit(fundo, (0, 30))
                    pygame.display.update()
                    return True


pygame.mixer.init()
pygame.mixer.music.load('musica_tema.mp3')
pygame.mixer.music.play()
pygame.init()
interface = pygame.display.set_mode((500, 530)) # tamanho da interface WxH
fonte_botoes = pygame.font.SysFont('Arial', 40)
fonte_contagem = pygame.font.SysFont('Arial', 30)
barra_status = pygame.Surface((interface.get_width(),30))

fundo = pygame.image.load('imagem.png')

preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
laranja = (255, 127, 0)

botao_azul = pygame.draw.circle(interface, azul, center=(251,272), radius=130, draw_top_left=True)
botao_verde = pygame.draw.circle(interface, verde, center=(251,272), radius=130, draw_top_right=True)
botao_laranja = pygame.draw.circle(interface, laranja, center=(251,272), radius=130, draw_bottom_left=True)
botao_vermelho = pygame.draw.circle(interface, vermelho, center=(251,272), radius=130, draw_bottom_right=True)

texto_comeco = fonte_botoes.render('START', True, preto) # texto, suavização e cor
pontos = 0
cores_sequenciais = []
jogando = False

while not jogando:
    interface.blit(fundo, (0, 30)) # escrece o background
    # os numeros são a posição XY inicial e final:
    botao_comecar = pygame.draw.rect(interface, branco, (180, 70, 150, 60))
    interface.blit(texto_comeco, (200, 74))
    pygame.display.update() # atualiza a interface para o usuário
    for evento in pygame.event.get(): # serve para fechar a janela
        if evento.type == QUIT:
            quit()
        elif evento.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos() # pega a posição do mouse
            if botao_comecar.collidepoint(mouse):
                jogando = True

interface.blit(fundo, (0, 30)) # atualiza o fundo para tirar o botão começar
pygame.display.update()

while jogando:
    barra_status.fill(preto)
    pontuacao = fonte_contagem.render('Pontos: '+str(pontos), True, branco)
    barra_status.blit(pontuacao, (0, 0)) # deixa no cantinho da tela
    interface.blit(barra_status, (0, 0))
    pygame.display.update()
    time.sleep(0.5)
    for evento in pygame.event.get():
        if evento.type == QUIT:
            quit()

    cores_sequenciais.append(escolher_cor_aleatoria())
    piscar_cores(cores_sequenciais)
    resposta_jogador = obter_resposta(len(cores_sequenciais))
    sequencia_cores = [cor['cor'] for cor in cores_sequenciais]

    resposta_correta = sequencia_cores == resposta_jogador
    if resposta_correta:
        pontos += 1
    else:
        jogando = restart()
        if jogando:
            pontos = 0
            cores_sequenciais = []

