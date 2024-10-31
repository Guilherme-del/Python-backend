import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# Variáveis de controle para o movimento da nave
posicao_nave = -5
dash_iniciado = False

# Propulsores
cor_propulsor = 0.5  # Intensidade inicial do propulsor

# Paleta de cores homogênea
COR_CORPO = (0.5, 0.5, 0.6)  # Cor principal do corpo da nave
COR_PAINEL = (0.4, 0.4, 0.5)  # Painéis e detalhes
COR_DETALHES = (0.3, 0.3, 0.4)  # Linhas e detalhes extras
COR_COCKPIT = (0.2, 0.2, 0.6)  # Cockpit
COR_ASAS = (0.4, 0.4, 0.5)  # Asas
COR_ESTRELAS = (1, 1, 1)  # Estrelas no fundo

def desenhar_corpo_central_unico(raio_x, raio_y, profundidade, n_lados):
    """Desenha o corpo principal da nave com textura segmentada."""
    glColor3f(*COR_CORPO)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)
    for i in range(n_lados + 1):
        angle = 2 * math.pi * i / n_lados
        x = raio_x * math.cos(angle)
        y = raio_y * math.sin(angle)
        glVertex3f(x, y, profundidade / 2)
    glEnd()

    # Adicionando painéis
    glColor3f(*COR_PAINEL)
    for j in range(6):
        angle1 = 2 * math.pi * j / 6
        angle2 = 2 * math.pi * (j + 1) / 6
        glBegin(GL_QUADS)
        glVertex3f(raio_x * math.cos(angle1), raio_y * math.sin(angle1), profundidade / 2)
        glVertex3f(raio_x * math.cos(angle2), raio_y * math.sin(angle2), profundidade / 2)
        glVertex3f(raio_x * math.cos(angle2), raio_y * math.sin(angle2), -profundidade / 2)
        glVertex3f(raio_x * math.cos(angle1), raio_y * math.sin(angle1), -profundidade / 2)
        glEnd()

def desenhar_cauda():
    """Desenha uma cauda detalhada com camadas adicionais."""
    glColor3f(*COR_PAINEL)
    glBegin(GL_QUADS)
    altura_conexao = 0.15

    glVertex3f(-0.05, -0.02 + altura_conexao, -0.05)
    glVertex3f(0.05, -0.02 + altura_conexao, -0.05)
    glVertex3f(0.05, -0.02 + altura_conexao, -0.5)
    glVertex3f(-0.05, -0.02 + altura_conexao, -0.5)

    glVertex3f(-0.03, -0.02 + altura_conexao, -0.5)
    glVertex3f(0.03, -0.02 + altura_conexao, -0.5)
    glVertex3f(0.03, -0.02 + altura_conexao, -1.0)
    glVertex3f(-0.03, -0.02 + altura_conexao, -1.0)
    glEnd()

    # Detalhes extras
    glColor3f(*COR_DETALHES)
    glBegin(GL_LINES)
    for i in range(1, 5):
        glVertex3f(-0.05 + i * 0.02, -0.02 + altura_conexao, -0.05)
        glVertex3f(-0.05 + i * 0.02, -0.02 + altura_conexao, -1.0)
    glEnd()

def desenhar_asas():
    """Desenha asas detalhadas com segmentos."""
    glColor3f(*COR_ASAS)
    glBegin(GL_TRIANGLES)

    # Asa esquerda
    glVertex3f(-0.6, 0, -0.1)
    glVertex3f(-0.2, 0.1, 0.1)
    glVertex3f(-0.2, -0.1, 0.1)

    # Asa direita
    glVertex3f(0.6, 0, -0.1)
    glVertex3f(0.2, 0.1, 0.1)
    glVertex3f(0.2, -0.1, 0.1)
    glEnd()

    # Linhas de detalhe nas asas
    glColor3f(*COR_DETALHES)
    glBegin(GL_LINES)
    for i in range(-3, 4):
        glVertex3f(-0.6 + i * 0.1, 0, -0.1)
        glVertex3f(-0.2 + i * 0.1, 0, 0.1)
    glEnd()

def desenhar_cockpit():
    """Desenha uma cúpula no topo da nave para representar o cockpit."""
    glColor3f(*COR_COCKPIT)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0.15)
    for i in range(21):
        angle = 2 * math.pi * i / 20
        x = 0.3 * math.cos(angle)
        y = 0.3 * math.sin(angle)
        glVertex3f(x, y, 0.1)
    glEnd()

def desenhar_detalhes():
    """Adiciona pequenos detalhes ao corpo da nave."""
    glColor3f(*COR_DETALHES)
    glBegin(GL_LINES)
    for i in range(-5, 6):
        glVertex3f(i * 0.1, 0, 0.15)
        glVertex3f(i * 0.1, 0, -0.15)
    glEnd()

def gerar_estrelas(qtd_estrelas):
    """Gera uma lista de posições de estrelas."""
    estrelas = []
    for _ in range(qtd_estrelas):
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        z = random.uniform(-20, -5)
        estrelas.append((x, y, z))
    return estrelas

def desenhar_estrelas(estrelas):
    """Desenha as estrelas no fundo."""
    glBegin(GL_POINTS)
    glColor3f(*COR_ESTRELAS)
    for estrela in estrelas:
        glVertex3f(*estrela)
    glEnd()

def main():
    global posicao_nave, dash_iniciado

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    estrelas = gerar_estrelas(150)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        desenhar_estrelas(estrelas)

        glPushMatrix()
        glTranslatef(0.0, 0.0, posicao_nave)
        glRotatef(-90, 1, 0, 0)

        desenhar_corpo_central_unico(1.2, 1.2, 0.2, 50)
        desenhar_asas()
        desenhar_cockpit()
        desenhar_detalhes()
        desenhar_cauda()
        
        glPopMatrix()

        if not dash_iniciado:
            posicao_nave += 0.02
            if posicao_nave >= -2:
                dash_iniciado = True
        else:
            posicao_nave += 0.5

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()